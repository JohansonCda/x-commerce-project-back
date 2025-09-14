from typing import Dict, Any
from flask_jwt_extended import get_jwt_identity, get_jwt
from datetime import datetime
from app.services.auth_services import AuthService


class TokenController:
    """Controller for handling token operations"""
    
    @staticmethod
    def refresh_access_token() -> tuple[Dict[str, Any], int]:
        """
        Refresh access token using a valid refresh token
        
        Returns:
            tuple: (response_data, status_code)
        """
        try:
            # Get user identity from refresh token
            current_user_id = get_jwt_identity()
            
            if not current_user_id:
                return {
                    'error': 'invalid_refresh_token',
                    'message': 'Invalid refresh token provided'
                }, 401
            
            # Get additional claims from the current refresh token
            refresh_token_claims = get_jwt()
            
            # Extract user information from refresh token claims
            username = refresh_token_claims.get('username', 'unknown')
            role = refresh_token_claims.get('role', 'user')
            
            # Convert string user_id back to int if needed
            user_id = int(current_user_id) if current_user_id.isdigit() else current_user_id
            
            # Create additional claims for the new access token
            additional_claims = {
                'username': username,
                'role': role,
                'refreshed_at': datetime.utcnow().isoformat()
            }
            
            # Generate new access token with updated claims
            new_access_token = AuthService.create_access_token(
                user_id=user_id,
                additional_claims=additional_claims
            )
            
            return {
                'access_token': new_access_token,
                'token_type': 'Bearer',
                'expires_in': 3600,  # 1 hour in seconds
                'user': {
                    'id': current_user_id,
                    'username': username,
                    'role': role
                },
                'message': 'Access token refreshed successfully'
            }, 200
            
        except Exception as e:
            return {
                'error': 'token_refresh_failed',
                'message': f'Failed to refresh token: {str(e)}'
            }, 500
    
    @staticmethod
    def revoke_token() -> tuple[Dict[str, Any], int]:
        """
        Revoke/blacklist current token (logout functionality)
        
        Note: In a production environment, you would implement token blacklisting
        by storing the token JTI (JWT ID) in a database or cache (Redis)
        
        Returns:
            tuple: (response_data, status_code)
        """
        try:
            # Get token information
            token_claims = get_jwt()
            jti = token_claims.get('jti')  # JWT ID
            token_type = token_claims.get('type', 'access')
            user_id = get_jwt_identity()
            
            # Here you would typically add the JTI to a blacklist
            # For example:
            # BlacklistService.add_token_to_blacklist(jti, token_type)
            
            return {
                'message': 'Token revoked successfully',
                'revoked_token_id': jti,
                'token_type': token_type,
                'user_id': user_id,
                'revoked_at': datetime.utcnow().isoformat()
            }, 200
            
        except Exception as e:
            return {
                'error': 'token_revocation_failed',
                'message': f'Failed to revoke token: {str(e)}'
            }, 500
    
    @staticmethod
    def validate_token() -> tuple[Dict[str, Any], int]:
        """
        Validate current token and return token information
        
        Returns:
            tuple: (response_data, status_code)
        """
        try:
            # Get token information
            token_claims = get_jwt()
            user_id = get_jwt_identity()
            
            # Extract token metadata
            issued_at = datetime.fromtimestamp(token_claims.get('iat', 0))
            expires_at = datetime.fromtimestamp(token_claims.get('exp', 0))
            token_type = token_claims.get('type', 'access')
            
            # Calculate time until expiration
            time_until_expiry = expires_at - datetime.utcnow()
            seconds_until_expiry = max(0, int(time_until_expiry.total_seconds()))
            
            return {
                'valid': True,
                'user_id': user_id,
                'username': token_claims.get('username', 'unknown'),
                'role': token_claims.get('role', 'user'),
                'token_type': token_type,
                'issued_at': issued_at.isoformat(),
                'expires_at': expires_at.isoformat(),
                'seconds_until_expiry': seconds_until_expiry,
                'is_fresh': token_claims.get('fresh', False),
                'jti': token_claims.get('jti'),
                'message': 'Token is valid'
            }, 200
            
        except Exception as e:
            return {
                'valid': False,
                'error': 'token_validation_failed',
                'message': f'Token validation failed: {str(e)}'
            }, 401
    
    @staticmethod
    def generate_new_token_pair(user_id: int, username: str, role: str) -> tuple[Dict[str, Any], int]:
        """
        Generate a new pair of access and refresh tokens
        
        Args:
            user_id: User identifier
            username: Username
            role: User role
            
        Returns:
            tuple: (response_data, status_code)
        """
        try:
            additional_claims = {
                'username': username,
                'role': role,
                'issued_at': datetime.utcnow().isoformat()
            }
            
            # Generate both tokens
            tokens = AuthService.generate_tokens(user_id, additional_claims)
            
            return {
                **tokens,
                'user': {
                    'id': user_id,
                    'username': username,
                    'role': role
                },
                'expires_in': 3600,  # Access token expiry in seconds
                'refresh_expires_in': 2592000,  # Refresh token expiry in seconds (30 days)
                'message': 'Token pair generated successfully'
            }, 200
            
        except Exception as e:
            return {
                'error': 'token_generation_failed',
                'message': f'Failed to generate tokens: {str(e)}'
            }, 500
