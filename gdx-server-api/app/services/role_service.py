from sqlalchemy.future import select
from app.models.role_model import RoleModel
from app.schemas.role_schema import roleSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.core.constants import StatusCodes
from typing import List


async def create_role(db: AsyncSession, role: roleSchema):
    result = RoleModel(role_name=role.role_name, description=role.description)
    db.add(result)
    await db.commit()
    await db.refresh(result)

    return {
        "data": role,
        "statuscode": StatusCodes.CREATED
    }


async def find_all_roles(db: AsyncSession) -> List[RoleModel]:
    stmt = select(RoleModel)
    result = await db.execute(stmt)
    list_all_roles = result.scalars().all()
    return {
            "data": list_all_roles,
            "statuscode" : StatusCodes.SUCCESS
        }


async def find_role_by_id(db: AsyncSession, role_id: int):
    result = await db.execute(
        select(RoleModel).filter(RoleModel.role_id == role_id)
    )
    roles = result.scalars().first()
    if not roles:
        return {
            "message": "Role not found",
            "statuscode": StatusCodes.NOT_FOUND
        }
    
    return {
        "data": roles,
        "statuscode": StatusCodes.SUCCESS
    }

