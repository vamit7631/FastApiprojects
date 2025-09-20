from datetime import datetime, timedelta
from typing import Tuple, Optional, List
from fastapi import Request, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import configs
from app.core.exceptions import AuthError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def create_access_token(subject: dict, expires_delta: Optional[timedelta] = None) -> Tuple[str, str]:
    expire = datetime.now() + (expires_delta or timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {"exp": expire, **subject}
    encoded_jwt = jwt.encode(payload, configs.SECRET_KEY, algorithm=ALGORITHM)
    expiration_datetime = expire.strftime(configs.DATETIME_FORMAT)
    return encoded_jwt, expiration_datetime


def verify_password(plain_password: str, hashed_password: str) -> bool:
    result = pwd_context.verify(plain_password, hashed_password)
    return result


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def decode_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, configs.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise AuthError(detail="Invalid or expired token.")


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise AuthError(detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise AuthError(detail="Invalid or expired token.")
            return credentials.credentials
        raise AuthError(detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        try:
            decode_jwt(jwt_token)
            return True
        except Exception:
            return False


def role_required(allowed_roles: List[str]):
    """Dependency to enforce role-based access."""
    def wrapper(token: str = Depends(JWTBearer())):
        payload = decode_jwt(token)  
        user_role = payload.get("role")

        if user_role not in allowed_roles:
            raise AuthError(detail="You do not have permission to access this resource.")

        return payload  

    return wrapper