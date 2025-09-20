from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base_model import TimestampMixin


class Permission(TimestampMixin, Base):
    __tablename__ = "permissions"

    permission_id = Column(Integer, primary_key=True, index=True)
    permission_name = Column(String(50), unique=True, nullable=False)

    # Relationships (for role-module-submodule mapping, if needed later)
    role_permissions = relationship("RolePermission", back_populates="permission", cascade="all, delete-orphan")
