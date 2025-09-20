from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.constants import StatusCodes
from app.core.database import get_postgres_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import create_user, find_all_user
from app.core.responsehandler import response
from app.core.exceptions import HTTPException
from typing import List


router = APIRouter(prefix = "/users", tags=["user"])

@router.post("/", status_code=StatusCodes.CREATED, response_model=UserResponse)
async def create_user_api(user: UserCreate, db: AsyncSession = Depends(get_postgres_db)):
    result = await create_user(db, user)
    if result["statuscode"] != 201:
        raise HTTPException(status_code=result['statuscode'], detail=result['message'])
    return response(status_code=result['statuscode'], detail=result["data"])     

@router.get("/", status_code=StatusCodes.SUCCESS, response_model=List[UserResponse])
async def find_all_user_api(db: AsyncSession = Depends(get_postgres_db)):
    result = await find_all_user(db)
    if result["statuscode"] != 200:
        raise HTTPException(status_code=result['statuscode'], detail=result['message'])
    return response(status_code=result['statuscode'], detail=result["data"])    

