from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base_model import TimestampMixin
from app.models.module_model import ModuleModel
from app.models.role_permissions_model import RolePermission


class SubModuleModel(TimestampMixin, Base):
    __tablename__ = "sub_modules"

    sub_module_id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.module_id", ondelete="CASCADE"), nullable=False)
    sub_module_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    module = relationship(ModuleModel, back_populates="submodules")
    role_permissions = relationship(RolePermission, back_populates="submodule", cascade="all, delete-orphan")

    __table_args__ = (
        # Ensures each sub_module_name is unique within its module
        {'sqlite_autoincrement': True},
    )
