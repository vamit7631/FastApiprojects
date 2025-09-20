from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class PermssionSchema(BaseModel):
    role_id: int
    module_id: Optional[int] = None
    sub_module_id: Optional[int] = None
    permission_id: int


# class OrganisationBaseSchema(OrganisationSchema, BaseModel):
#     pass
