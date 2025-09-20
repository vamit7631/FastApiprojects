from datetime import datetime
from pydantic import BaseModel, field_validator
from app.schemas.user_schema import User
from pydantic import BaseModel, EmailStr, constr
import re
class SignIn(BaseModel):
    email: str
    password: str


class Payload(BaseModel):
    id: int
    email: str
    firstname: str
    lastname: str
    role: str

class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

    @field_validator("new_password")
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