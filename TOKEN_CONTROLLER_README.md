# 🔐 TokenController Documentation

## Overview
El `TokenController` es un controlador especializado para manejar todas las operaciones relacionadas con tokens JWT de manera más robusta y escalable.

## Features

### 🔄 **Refresh Token Enhanced**
- Mantiene los claims del usuario (username, role)
- Agrega metadata de cuándo se refrescó el token
- Mejor manejo de errores
- Respuesta más detallada

### ✅ **Token Validation**
- Valida tokens y devuelve información detallada
- Calcula tiempo restante hasta expiración
- Muestra metadata del token (issued_at, expires_at, etc.)
- Información del usuario embebida

### 🚫 **Token Revocation**
- Preparado para implementar blacklist de tokens
- Tracking de tokens revocados
- Información detallada de revocación

### 📊 **Token Information**
- Endpoint dedicado para obtener info del token
- Útil para debugging y monitoreo
- Información completa del estado del token

## API Endpoints

### Auth Endpoints (Updated)
- `POST /api/auth/refresh` - Enhanced refresh using TokenController
- `POST /api/auth/logout` - Enhanced logout with token tracking

### New Token Endpoints
- `POST /api/token/refresh` - Dedicated refresh endpoint
- `GET /api/token/validate` - Validate current token
- `GET /api/token/info` - Get token information (alias for validate)
- `POST /api/token/revoke` - Revoke/blacklist token

## Usage Examples

### 1. Enhanced Refresh Token
```bash
POST /api/auth/refresh
Authorization: Bearer [refresh_token]

Response:
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "id": "1",
    "username": "admin",
    "role": "admin"
  },
  "message": "Access token refreshed successfully"
}
```

### 2. Token Validation
```bash
GET /api/token/validate
Authorization: Bearer [access_token]

Response:
{
  "valid": true,
  "user_id": "1",
  "username": "admin",
  "role": "admin",
  "token_type": "access",
  "issued_at": "2025-09-11T10:00:00",
  "expires_at": "2025-09-11T11:00:00",
  "seconds_until_expiry": 3420,
  "is_fresh": false,
  "jti": "abc123...",
  "message": "Token is valid"
}
```

### 3. Token Revocation
```bash
POST /api/token/revoke
Authorization: Bearer [access_token]

Response:
{
  "message": "Token revoked successfully",
  "revoked_token_id": "abc123...",
  "token_type": "access",
  "user_id": "1",
  "revoked_at": "2025-09-11T10:30:00"
}
```

## Implementation Details

### TokenController Methods

#### `refresh_access_token()`
- Extrae información del refresh token
- Mantiene claims del usuario
- Agrega timestamp de refresh
- Genera nuevo access token con metadata actualizada

#### `validate_token()`
- Valida token actual
- Calcula tiempo de expiración
- Devuelve información completa del token
- Útil para frontend y debugging

#### `revoke_token()`
- Extrae JTI (JWT ID) del token
- Prepara estructura para blacklist
- Tracking de revocación
- Información detallada de logout

#### `generate_new_token_pair()`
- Método auxiliar para generar pares de tokens
- Útil para casos especiales
- Claims personalizables

## Benefits

### 🔧 **For Developers**
- Código más organizado y mantenible
- Lógica centralizada de tokens
- Mejor debugging y logging
- Fácil extensión para nuevas features

### 🚀 **For Frontend**
- Respuestas más informativas
- Mejor manejo de estados de token
- Información de expiración en tiempo real
- Tracking de sesiones

### 🛡️ **For Security**
- Preparado para token blacklisting
- Tracking de operaciones de token
- Metadata de auditoría
- Mejor control de sesiones

## Future Enhancements

### 📝 **Token Blacklist**
```python
# Implementación futura
class TokenBlacklistService:
    @staticmethod
    def add_to_blacklist(jti: str, token_type: str):
        # Agregar a Redis o base de datos
        pass
    
    @staticmethod
    def is_blacklisted(jti: str) -> bool:
        # Verificar si está en blacklist
        pass
```

### 📊 **Session Management**
```python
# Tracking de sesiones activas
class SessionManager:
    @staticmethod
    def track_active_session(user_id: str, jti: str):
        # Tracking de sesiones por usuario
        pass
    
    @staticmethod
    def revoke_all_sessions(user_id: str):
        # Revocar todas las sesiones de un usuario
        pass
```

### 🔔 **Token Events**
```python
# Sistema de eventos para tokens
class TokenEvents:
    @staticmethod
    def on_token_refresh(user_id: str, old_jti: str, new_jti: str):
        # Log de refresh
        pass
    
    @staticmethod
    def on_token_revoke(user_id: str, jti: str):
        # Log de revocación
        pass
```

## Testing

Run the test suite:
```bash
python test_token_controller.py
```

Expected output:
- ✅ Enhanced token refresh with metadata
- ✅ Token validation and info endpoints  
- ✅ Token revocation with tracking
- ✅ Improved error handling
- ✅ Detailed response data
