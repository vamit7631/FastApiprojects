from datetime import datetime
from pydantic import BaseModel

class moduleSchema(BaseModel):
    module_name: str
    description: str

class submoduleSchema(BaseModel):
    module_id: int
    sub_module_name: str
    description: str
