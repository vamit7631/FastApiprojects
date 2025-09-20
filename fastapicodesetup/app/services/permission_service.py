from sqlalchemy.future import select
from app.models.role_permissions_model import RolePermission
from app.schemas.permission_schema import PermssionSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.core.constants import StatusCodes
from typing import List


async def create_permission(db: AsyncSession, role_permission: PermssionSchema):    
    new_permission = RolePermission(
        role_id=role_permission.role_id,
        permission_id=role_permission.permission_id,
        module_id=role_permission.module_id,
        sub_module_id=role_permission.sub_module_id
    )


    db.add(new_permission)
    await db.commit()
    await db.refresh(new_permission)
    return {
            "data": new_permission,
            "statuscode" : StatusCodes.CREATED
        }
