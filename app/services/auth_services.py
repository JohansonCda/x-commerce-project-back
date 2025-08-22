from typing import Optional, Dict, Any
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta

class AuthService:
    @staticmethod
    def generate_tokens(user_id: int, additional_claims: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """Generate access and refresh tokens for a user"""
        # Convert user_id to string as required by JWT
        user_id_str = str(user_id)
        
        access_token = create_access_token(
            identity=user_id_str,
            additional_claims=additional_claims or {}
        )
        refresh_token = create_refresh_token(identity=user_id_str)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer'
        }

    @staticmethod
    def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
        """Create a new access token"""
        # Convert user_id to string as required by JWT
        user_id_str = str(user_id)
        
        return create_access_token(
            identity=user_id_str,
            expires_delta=expires_delta
        )