from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decode_token

security = HTTPBearer()


def require_role(role: str):
    def _role_checker(creds: HTTPAuthorizationCredentials = Depends(security)):
        try:
            payload = decode_token(creds.credentials)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")
        if payload.get('role') != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return payload
    return _role_checker


def require_any_role(roles: list[str]):
    def _checker(creds: HTTPAuthorizationCredentials = Depends(security)):
        try:
            payload = decode_token(creds.credentials)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")
        if payload.get('role') not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return payload
    return _checker
