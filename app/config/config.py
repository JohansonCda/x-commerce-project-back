
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

class Config:
    # JWT Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "tu-clave-secreta-muy-segura-aqui-12345")
    
    # Database configuration (optional for JWT-only functionality)
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set.")
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    BASE_DIR = Path(__file__).resolve().parent
    UPLOAD_FOLDER_REL = os.environ.get("UPLOAD_FOLDER", "/image/product/")
    UPLOAD_FOLDER = (BASE_DIR / ".." / ".." / UPLOAD_FOLDER_REL.strip("/\\")).resolve()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
