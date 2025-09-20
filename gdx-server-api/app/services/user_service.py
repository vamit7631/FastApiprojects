from sqlalchemy.future import select
from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.core.constants import StatusCodes
from typing import List
from app.core.security import get_password_hash


async def create_user(db: AsyncSession, user: UserCreate):
    result = await db.execute(select(User).filter(User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        return {
            "message" : "Email Already Exist",
            "statuscode" : StatusCodes.CONFLICT
        }
    
    
    result = await db.execute(select(User).filter(User.username == user.username))
    existing_username = result.scalars().first()
    if existing_username:
        return {
            "message" : "Username Already Exists",
            "statuscode" : StatusCodes.CONFLICT
        }

    password = user.password
    hashed_password = get_password_hash(password)


    newuser = User(firstname = user.firstname, lastname = user.lastname, username = user.username, email = user.email, password = hashed_password , role_id = user.role_id, organisation_id = user.organisation_id)

    db.add(newuser)
    await db.commit()
    await db.refresh(newuser)
    return {
            "data": newuser,
            "statuscode" : StatusCodes.CREATED
        }


async def find_all_user(db: AsyncSession) -> List[User]:
    stmt = select(User)
    result = await db.execute(stmt)
    list_all_users = result.scalars().all()
    return {
            "status" : True,
            "message" : "Fetched Successfully!",
            "data": list_all_users,
            "statuscode" : StatusCodes.SUCCESS
        }
