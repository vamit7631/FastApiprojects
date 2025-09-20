from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.constants import StatusCodes
from app.core.database import get_postgres_db
from app.schemas.permission_schema import PermssionSchema
from app.services.permission_service import create_permission
from app.core.responsehandler import response
from app.core.exceptions import HTTPException
from typing import List
from app.core.security import role_required

router = APIRouter(prefix = "/permission", tags=["permission"])

@router.post("/", status_code=StatusCodes.CREATED, response_model=PermssionSchema)
async def create_permission_api(user: PermssionSchema, db: AsyncSession = Depends(get_postgres_db)):
    result = await create_permission(db, user)
    if result["statuscode"] != 201:
        raise HTTPException(status_code=result['statuscode'], detail=result['message'])
    return response(status_code=result['statuscode'], detail=result["data"]) 