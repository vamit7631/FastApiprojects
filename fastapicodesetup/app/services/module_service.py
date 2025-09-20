from sqlalchemy.future import select
from app.models.module_model import ModuleModel
from app.models.sub_module_model import SubModuleModel
from app.schemas.module_schema import moduleSchema, submoduleSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.constants import StatusCodes
from typing import List


async def create_module(db: AsyncSession, module: moduleSchema):
    result = ModuleModel(module_name=module.module_name, description=module.description)
    db.add(result)
    await db.commit()
    await db.refresh(result)

    return {
        "data": module,
        "statuscode": StatusCodes.CREATED
    }

async def create_submodule(db: AsyncSession, submodule: submoduleSchema):
    result = SubModuleModel(module_id=submodule.module_id, sub_module_name=submodule.sub_module_name, description=submodule.description)
    db.add(result)
    await db.commit()
    await db.refresh(result)

    return {
        "data": submodule,
        "statuscode": StatusCodes.CREATED
    }


async def find_all_Modules(db: AsyncSession) -> List[ModuleModel]:
    stmt = select(ModuleModel).options(
        selectinload(ModuleModel.submodules)
    )
    result = await db.execute(stmt)
    list_all_modules = result.scalars().unique().all()
    return {
            "data": list_all_modules,
            "statuscode" : StatusCodes.SUCCESS
        }
