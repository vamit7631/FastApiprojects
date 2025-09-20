from sqlalchemy import Column, Integer, String
from app.core.database import Base
from app.models.role_permissions_model import RolePermission
from app.models.base_model import TimestampMixin
from sqlalchemy.orm import relationship

class RoleModel(TimestampMixin, Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), index=True, nullable=False)
    description = Column(String(150), index=True, nullable=True)

    users = relationship("User", back_populates="role")
    role_permissions = relationship(RolePermission, back_populates="role", cascade="all, delete-orphan")