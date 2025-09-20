from datetime import datetime
from pydantic import BaseModel

class roleSchema(BaseModel):
    role_name: str
    description: str

class roleBaseSchema(roleSchema, BaseModel):
    pass
