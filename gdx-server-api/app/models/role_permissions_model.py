from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base_model import TimestampMixin

class RolePermission(TimestampMixin, Base):
    __tablename__ = "role_permissions"

    role_permission_id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.role_id", ondelete="CASCADE"), nullable=False)
    sub_module_id = Column(Integer, ForeignKey("sub_modules.sub_module_id", ondelete="CASCADE"), nullable=True)
    module_id = Column(Integer, ForeignKey("modules.module_id", ondelete="CASCADE"), nullable=True)
    permission_id = Column(Integer, ForeignKey("permissions.permission_id", ondelete="CASCADE"), nullable=False)

    # Relationships using string references
    role = relationship("RoleModel", back_populates="role_permissions")
    submodule = relationship("SubModuleModel", back_populates="role_permissions")
    module = relationship("ModuleModel", back_populates="role_permissions")
    permission = relationship("Permission", back_populates="role_permissions")

    __table_args__ = (
        UniqueConstraint("role_id", "sub_module_id", "permission_id", name="uq_role_module_submodule_permission"),
        CheckConstraint("(sub_module_id IS NOT NULL) OR (module_id IS NOT NULL)", name="check_module_or_submodule"),
    )