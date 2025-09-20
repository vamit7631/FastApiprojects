from pydantic import BaseModel, EmailStr, field_validator
from app.schemas.base_schema import ModelBaseInfo
import re

class UserBase(BaseModel):
    firstname: str
    lastname: str
    username: str    
    email: EmailStr

class UserCreate(UserBase):
    role_id: int
    organisation_id: int
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        # Length check
        if len(v) < 8 or len(v) > 14:
            raise ValueError("Password must be between 8 and 14 characters long")

        # At least one uppercase
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")

        # At least one lowercase
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")

        # At least one digit
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")

        # At least one special character
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")

        return v

class User(ModelBaseInfo, UserBase): ...

class UserResponse(UserBase):
    id: int

    model_config = {"from_attributes": True}
