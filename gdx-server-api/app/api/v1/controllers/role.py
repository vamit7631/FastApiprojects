from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.constants import StatusCodes
from app.core.database import get_postgres_db
from app.schemas.role_schema import roleSchema, roleBaseSchema
from app.services.role_service import create_role, find_all_roles, find_role_by_id
from app.core.responsehandler import response
from app.core.exceptions import HTTPException
from typing import List
from app.core.security import JWTBearer


router = APIRouter(prefix = "/roles", tags=["role"])

@router.post("/", status_code=StatusCodes.CREATED, response_model=roleBaseSchema)
async def create_role_api(user: roleSchema, db: AsyncSession = Depends(get_postgres_db), token: str = Depends(JWTBearer())):
    result = await create_role(db, user)
    if result["statuscode"] != 201:
        raise HTTPException(status_code=result['statuscode'], detail=result['message'])
    return response(status_code=result['statuscode'], detail=result["data"])     


@router.get("/", status_code=StatusCodes.SUCCESS, response_model=List[roleBaseSchema])
async def find_all_organisation_api(db: AsyncSession = Depends(get_postgres_db), token: str = Depends(JWTBearer())):
    result = await find_all_roles(db)
    if result["statuscode"] != 200:
        raise HTTPException(status_code=result['statuscode'], detail=result['message'])
    return response(status_code=result['statuscode'], detail=result["data"])    


@router.get("/{role_id}", status_code=StatusCodes.SUCCESS, response_model=roleBaseSchema)
async def find_role_by_id_api(role_id: int, db: AsyncSession = Depends(get_postgres_db)):
    result = await find_role_by_id(db, role_id)
    if result["statuscode"] != 200:
        raise HTTPException(status_code=result['statuscode'], detail=result['message'])
    return response(status_code=result['statuscode'], detail=result["data"])