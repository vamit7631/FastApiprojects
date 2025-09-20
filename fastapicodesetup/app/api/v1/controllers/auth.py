from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi.encoders import jsonable_encoder
from app.core.constants import StatusCodes
from app.core.database import get_postgres_db
from app.schemas.auth_schema import SignIn,ForgotPassword, ResetPassword
from app.services.auth_service import sign_in, forget_password, reset_password
# from app.schemas.user_schema import User
from app.core.responsehandler import response
from app.core.exceptions import HTTPException
# from typing import List


router = APIRouter(prefix = "/auth", tags=["auth"])

@router.post("/sign-in", status_code=StatusCodes.SUCCESS)
async def sign_in_api(user_info: SignIn, db: AsyncSession = Depends(get_postgres_db)):
    result =  await sign_in(user_info, db)
    if result["statuscode"] != 200:
        raise HTTPException(status_code=result['statuscode'], detail=result['message'])
    return response(status_code=result['statuscode'], detail=result["data"])    

@router.post("/forgot-password", status_code=StatusCodes.SUCCESS)
async def sign_in_api(user_email: ForgotPassword, db: AsyncSession = Depends(get_postgres_db)):
    result =  await forget_password(user_email, db)
    if result["statuscode"] != 200:
        raise HTTPException(status_code=result['statuscode'], detail=result['message'])
    return response(status_code=result['statuscode'], detail=result["data"])    


@router.post("/reset-password", status_code=StatusCodes.SUCCESS)
async def sign_in_api(user_detail: ResetPassword, db: AsyncSession = Depends(get_postgres_db)):
    result =  await reset_password(user_detail, db)
    if result["statuscode"] != 200:
        raise HTTPException(status_code=result['statuscode'], detail=result['message'])
    return response(status_code=result['statuscode'], detail=result["message"])    