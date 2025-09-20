from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.constants import StatusCodes
from app.core.database import get_postgres_db
from app.schemas.module_schema import moduleSchema, submoduleSchema
from app.services.module_service import create_module, create_submodule, find_all_Modules
# from app.schemas.role_schema import roleSchema, roleBaseSchema
# from app.services.role_service import create_role, find_all_roles, find_role_by_id
from app.core.responsehandler import response
from app.core.exceptions import HTTPException
from typing import List
from app.core.security import JWTBearer
from app.core.security import role_required

router = APIRouter(prefix = "/modules", tags=["module"])

@router.post("/", status_code=StatusCodes.CREATED, response_model=moduleSchema)
async def create_module_api(modules: moduleSchema, db: AsyncSession = Depends(get_postgres_db), user=Depends(role_required(["SuperAdmin"]))):
    result = await create_module(db, modules)
    if result["statuscode"] != 201:
        raise HTTPException(status_code=result['statuscode'], detail=result['message'])
    return response(status_code=result['statuscode'], detail=result["data"]) 


@router.post("/sub-modules", status_code=StatusCodes.CREATED, response_model=submoduleSchema)
async def create_submodule_api(modules: submoduleSchema, db: AsyncSession = Depends(get_postgres_db), user=Depends(role_required(["SuperAdmin"]))):
    result = await create_submodule(db, modules)
    if result["statuscode"] != 201:
        raise HTTPException(status_code=result['statuscode'], detail=result['message'])
    return response(status_code=result['statuscode'], detail=result["data"])   


@router.get("/", status_code=StatusCodes.SUCCESS, response_model=List[moduleSchema])
async def find_all_modules_api(db: AsyncSession = Depends(get_postgres_db)):
    result = await find_all_Modules(db)
    if result["statuscode"] != 200:
        raise HTTPException(status_code=result['statuscode'], detail=result['message'])
    return response(status_code=result['statuscode'], detail=result["data"])  