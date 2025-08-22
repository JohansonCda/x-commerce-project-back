from typing import List
from ..database import db
from .base_controller import BaseController
from ..models.status import Status
from ..schemas.status_schema import StatusCreate, StatusUpdate, StatusRead

class StatusController(BaseController[Status, StatusCreate, StatusRead, StatusUpdate]):
    def __init__(self):
        super().__init__(Status, StatusCreate, StatusRead, StatusUpdate)

    def get_by_name(self, name: str, enabled: bool = True) -> List[StatusRead]:
        """Get statuses by name"""
        objs = (
            db.session.query(self.model)
            .filter(
                self.model.name == name,
                self.model.enable == enabled
            )
            .all()
        )
        return [StatusRead.model_validate(obj) for obj in objs]

    def get_all_enable(self, enabled: bool = True) -> List[StatusRead]:
        """Get all statuses, optionally filtered by enabled status"""
        query = db.session.query(self.model)
        if enabled is not None:
            query = query.filter(self.model.enable == enabled)
        objs = query.all()
        return [StatusRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: StatusCreate):
        pass
