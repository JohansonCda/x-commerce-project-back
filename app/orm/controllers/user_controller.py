from datetime import datetime
from typing import List
import re
from ..database import db
from .base_controller import BaseController
from ..models.user import User
from ..schemas.user_schema import UserRead, UserCreate, UserUpdate

class UserController(BaseController[User, UserCreate, UserRead, UserUpdate]):
    def __init__(self):
        super().__init__(User, UserCreate, UserRead, UserUpdate)

    def get_by_full_name(self, full_name: str, enabled: bool = True) -> List[UserRead]:
        """Get users by full name"""
        objs = (
            db.session.query(self.model)
            .filter(
                self.model.full_name == full_name,
                self.model.enable == enabled
            )
            .all()
        )
        return [UserRead.model_validate(obj) for obj in objs]
    
    def get_by_email(self, email: str, enabled: bool = True) -> List[UserRead]:
        """Get users by email"""
        objs = (
            db.session.query(self.model)
            .filter(
                self.model.email == email,
                self.model.enable == enabled
            )
            .all()
        )
        return [UserRead.model_validate(obj) for obj in objs]
    
    def get_by_username(self, username: str, enabled: bool = True) -> List[UserRead]:
        """Get users by username"""
        objs = (
            db.session.query(self.model)
            .filter(
                self.model.username == username,
                self.model.enable == enabled
            )
            .all()
        )
        return [UserRead.model_validate(obj) for obj in objs]
    
    def get_by_role(self, role: bool, enabled: bool = True) -> List[UserRead]:
        """Get users by role"""
        objs = (
            db.session.query(self.model)
            .filter(
                self.model.is_admin == role,
                self.model.enable == enabled
            )
            .all()
        )
        return [UserRead.model_validate(obj) for obj in objs]
    
    def get_by_register_date(self, start_date: datetime, end_date: datetime, enabled: bool = True) -> List[UserRead]:
        """Get users by register date"""
        objs = (
            db.session.query(self.model)
            .filter(
                self.model.register >= start_date,
                self.model.register <= end_date,
                self.model.enable == enabled
            )
            .all()
        )
        return [UserRead.model_validate(obj) for obj in objs]

    def get_all_enable(self, enabled: bool = True) -> List[UserRead]:
        """Get all users, optionally filtered by enabled status"""
        query = db.session.query(self.model)
        if enabled is not None:
            query = query.filter(self.model.enable == enabled)
        objs = query.all()
        return [UserRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: UserCreate):
        """Validation hook called automatically from BaseController.create()"""
        # Email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, obj_in.email):
            raise ValueError("Invalid email format")
        
        # Check if email already exists
        existing_email = (
            db.session.query(self.model)
            .filter(self.model.email == obj_in.email)
            .first()
        )
        if existing_email:
            raise ValueError(f"Email '{obj_in.email}' is already registered")
        
        # Check if username already exists
        existing_username = (
            db.session.query(self.model)
            .filter(self.model.username == obj_in.username)
            .first()
        )
        if existing_username:
            raise ValueError(f"Username '{obj_in.username}' is already taken")
