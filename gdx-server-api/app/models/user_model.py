from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.core.database import Base
from app.models.base_model import TimestampMixin
from sqlalchemy.orm import relationship
class User(TimestampMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50), index=True, nullable=False)
    lastname = Column(String(50), index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password = Column(String(200), index=True, nullable=False)
    otp = Column(String, nullable=True)
    otp_expiration = Column(DateTime(timezone=True), nullable=True)

    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    organisation_id = Column(Integer, ForeignKey("organisation.organisation_id"), nullable=True)

    role = relationship("RoleModel", back_populates="users")
    organisation = relationship("Organisation", back_populates="users")