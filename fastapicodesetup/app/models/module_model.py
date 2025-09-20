from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base_model import TimestampMixin

class ModuleModel(TimestampMixin, Base):
    __tablename__ = "modules"

    module_id = Column(Integer, primary_key=True, index=True)
    module_name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Relationships
    submodules = relationship("SubModuleModel", back_populates="module", cascade="all, delete-orphan")
    role_permissions = relationship("RolePermission", back_populates="module", cascade="all, delete-orphan")
