from sqlalchemy.future import select
from app.models.organisation_model import Organisation
from app.schemas.organisation_schema import OrganisationBaseSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.core.constants import StatusCodes
from typing import List


async def create_organisation(db: AsyncSession, organisation: OrganisationBaseSchema):
    result = await db.execute(select(Organisation).filter(Organisation.organisation_email == organisation.organisation_email))
    existing_org = result.scalars().first()
    if existing_org:
        return {
            "message" : "Email Already Exist",
            "statuscode" : StatusCodes.CONFLICT
        }
    
    neworganisation = Organisation(organisation_email = organisation.organisation_email, organisation_name = organisation.organisation_name, address1 = organisation.address1, address2 = organisation.address2, city = organisation.city, state = organisation.state, country = organisation.country, pincode = organisation.pincode)
    db.add(neworganisation)
    await db.commit()
    await db.refresh(neworganisation)
    return {
            "data": organisation,
            "statuscode" : StatusCodes.CREATED
        }




async def find_all_Organisation(db: AsyncSession) -> List[Organisation]:
    stmt = select(Organisation)
    result = await db.execute(stmt)
    list_all_organisation = result.scalars().all()
    return {
            "data": list_all_organisation,
            "statuscode" : StatusCodes.SUCCESS
        }


async def find_organisation_by_id(db: AsyncSession, organisation_id: int):
    result = await db.execute(
        select(Organisation).filter(Organisation.organisation_id == organisation_id)
    )
    organisation = result.scalars().first()
    if not organisation:
        return {
            "message": "Organisation not found",
            "statuscode": StatusCodes.NOT_FOUND
        }
    
    return {
        "data": organisation,
        "statuscode": StatusCodes.SUCCESS
    }


async def delete_organisation_by_id(db: AsyncSession, organisation_id: int):
    result = await db.execute(
        select(Organisation).filter(Organisation.organisation_id == organisation_id)
    )
    organisation = result.scalars().first()
    if not organisation:
        return {
            "message": "Organisation not found",
            "statuscode": StatusCodes.NOT_FOUND
        }
    
    await db.delete(organisation)
    await db.commit()

    return {
        "data": organisation,
        "statuscode": StatusCodes.SUCCESS
    }


async def update_organisation_by_id(db: AsyncSession, organisation_id: int, organisation_data: OrganisationBaseSchema):
    result = await db.execute(
        select(Organisation).filter(Organisation.organisation_id == organisation_id)
    )
    organisation = result.scalars().first()

    if not organisation:
        return {
            "message": "Organisation not found",
            "statuscode": StatusCodes.NOT_FOUND
        }

    # Update fields
    organisation.organisation_email = organisation_data.organisation_email
    organisation.organisation_name = organisation_data.organisation_name
    organisation.address1 = organisation_data.address1
    organisation.address2 = organisation_data.address2
    organisation.city = organisation_data.city
    organisation.state = organisation_data.state
    organisation.country = organisation_data.country
    organisation.pincode = organisation_data.pincode

    await db.commit()
    await db.refresh(organisation)

    return {
        "data": organisation,
        "statuscode": StatusCodes.SUCCESS
    }
