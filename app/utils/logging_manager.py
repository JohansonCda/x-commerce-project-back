import logging
import os
import uuid
from typing import Optional, Dict, Any
from logging.handlers import RotatingFileHandler
from flask import has_request_context, request, g
from dotenv import load_dotenv

class RequestFormatter(logging.Formatter):
    """Custom formatter to add request context to logs."""
    def format(self, record):
        if has_request_context():
            record.request_id = getattr(g, 'request_id', '-')
            record.remote_addr = request.remote_addr
            record.method = request.method
            record.path = request.path
            record.user = getattr(g, 'user_id', '-')
        else:
            record.request_id = '-'
            record.remote_addr = '-'
            record.method = '-'
            record.path = '-'
            record.user = '-'
        return super().format(record)

class LoggingManager:
    """Centralized logging with file rotation and request context."""
    def __init__(self, service_name: str = "xcommerce_api", log_file: str = None):
        load_dotenv()
        self.service_name = service_name
        self.log_file = log_file or os.getenv('LOG_FILE_PATH', 'application.log')
        self.log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        self._initialize_logging()

    def _initialize_logging(self):
        self.logger = logging.getLogger(self.service_name)
        self.logger.setLevel(self.log_level)
        self.logger.handlers.clear()

        formatter = RequestFormatter(
            '%(asctime)s %(levelname)s %(request_id)s %(remote_addr)s %(method)s %(path)s %(user)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        try:
            file_handler = RotatingFileHandler(self.log_file, maxBytes=2*1024*1024, backupCount=5)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(self.log_level)
            self.logger.addHandler(file_handler)
        except Exception as e:
            print(f"Failed to configure file logging: {e}")

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(self.log_level)
        self.logger.addHandler(console_handler)

    def log(self, level: str, message: str, component: Optional[str] = None, extra: Optional[Dict[str, Any]] = None):
        extra = extra or {}
        if component:
            extra['component'] = component
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(message, extra=extra)

    def info(self, message: str, component: Optional[str] = None, **kwargs):
        self.log('info', message, component, kwargs)

    def warning(self, message: str, component: Optional[str] = None, **kwargs):
        self.log('warning', message, component, kwargs)

    def error(self, message: str, component: Optional[str] = None, **kwargs):
        self.log('error', message, component, kwargs)

    def debug(self, message: str, component: Optional[str] = None, **kwargs):
        self.log('debug', message, component, kwargs)

    def exception(self, message: str, component: Optional[str] = None, **kwargs):
        self.log('exception', message, component, kwargs)

def register_flask_logging_hooks(app):
    @app.before_request
    def add_request_id():
        g.request_id = str(uuid.uuid4())
        # Agregar cuando se agregue lo de usuarios
        # g.user_id = current_user.id


    @app.after_request
    def log_request(response):
        logger = logging.getLogger('xcommerce_api')
        req_data = None
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                req_data = request.get_json(silent=True)
            except Exception:
                req_data = None
        else:
            req_data = request.args.to_dict()

        log_msg = f"{request.method} {request.path} {response.status_code}"
        log_extra = {
            'component': 'request',
            'user_id': getattr(g, 'user_id', '-'),
            'request_data': req_data
        }
        if 400 <= response.status_code < 500:
            logger.warning(log_msg, extra=log_extra)
        elif response.status_code >= 500:
            logger.error(log_msg, extra=log_extra)
        else:
            logger.info(log_msg, extra=log_extra)
        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger = logging.getLogger('xcommerce_api')
        req_data = None
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                req_data = request.get_json(silent=True)
            except Exception:
                req_data = None
        else:
            req_data = request.args.to_dict()
        logger.exception(
            f"Exception in {request.method} {request.path}",
            extra={
                'component': 'exception',
                'user_id': getattr(g, 'user_id', '-'),
                'request_data': req_data
            }
        )
        return {"message": "Internal server error"}, 500

logging_manager = LoggingManager()
log = logging_manager.log
info = logging_manager.info
warning = logging_manager.warning
error = logging_manager.error
debug = logging_manager.debug
exception = logging_manager.exception
