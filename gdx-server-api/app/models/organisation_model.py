from sqlalchemy import Column, Integer, String
from app.core.database import Base
from app.models.base_model import TimestampMixin
from sqlalchemy.orm import relationship

class Organisation(TimestampMixin, Base):
    __tablename__ = "organisation"

    organisation_id = Column(Integer, primary_key=True, index=True)
    organisation_email = Column(String(120), unique=True, index=True, nullable=False)
    organisation_name = Column(String(50), index=True, nullable=False)
    address1 = Column(String(100), nullable=False)
    address2 = Column(String(50), index=True, nullable=False)
    city = Column(String(50), index=True, nullable=False)
    state = Column(String(50), index=True, nullable=False)
    country = Column(String(50), index=True, nullable=False)
    pincode = Column(String(50), index=True, nullable=False)

    users = relationship("User", back_populates="organisation")