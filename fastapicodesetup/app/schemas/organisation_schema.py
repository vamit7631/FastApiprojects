from datetime import datetime
from pydantic import BaseModel

class OrganisationSchema(BaseModel):
    organisation_email: str
    organisation_name: str
    address1: str
    address2: str
    city: str
    state: str
    country: str
    pincode: str


class OrganisationBaseSchema(OrganisationSchema, BaseModel):
    pass
