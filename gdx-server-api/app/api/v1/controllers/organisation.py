from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.constants import StatusCodes
from app.core.database import get_postgres_db
from app.schemas.organisation_schema import OrganisationSchema, OrganisationBaseSchema
from app.services.organisation_service import create_organisation, find_all_Organisation, find_organisation_by_id, delete_organisation_by_id, update_organisation_by_id
from app.core.responsehandler import response
from app.core.exceptions import HTTPException
from typing import List
from app.core.security import role_required

router = APIRouter(prefix = "/organisation", tags=["organisation"])

@router.post("/", status_code=StatusCodes.CREATED, response_model=OrganisationBaseSchema)
async def create_organisation_api(user: OrganisationSchema, db: AsyncSession = Depends(get_postgres_db)):
    result = await create_organisation(db, user)
    if result["statuscode"] != 201:
        raise HTTPException(status_code=result['statuscode'], detail=result['message'])
    return response(status_code=result['statuscode'], detail=result["data"])     

@router.get("/", status_code=StatusCodes.SUCCESS, response_model=List[OrganisationBaseSchema])
async def find_all_organisation_api(db: AsyncSession = Depends(get_postgres_db), user=Depends(role_required(["User"]))):
    result = await find_all_Organisation(db)
    if result["statuscode"] != 200:
        raise HTTPException(status_code=result['statuscode'], detail=result['message'])
    return response(status_code=result['statuscode'], detail=result["data"])    


@router.get("/{organisation_id}", status_code=StatusCodes.SUCCESS, response_model=OrganisationBaseSchema)
async def find_organisation_by_id_api(organisation_id: int, db: AsyncSession = Depends(get_postgres_db)):
    result = await find_organisation_by_id(db, organisation_id)
    if result["statuscode"] != 200:
        raise HTTPException(status_code=result['statuscode'], detail=result['message'])
    return response(status_code=result['statuscode'], detail=result["data"])


@router.delete("/{organisation_id}", status_code=StatusCodes.SUCCESS, response_model=OrganisationBaseSchema)
async def delete_organisation_by_id_api(organisation_id: int, db: AsyncSession = Depends(get_postgres_db)):
    result = await delete_organisation_by_id(db, organisation_id)
    if result["statuscode"] != 200:
        raise HTTPException(status_code=result['statuscode'], detail=result['message'])
    return response(status_code=result['statuscode'], detail=result["data"])


@router.put("/{organisation_id}", status_code=StatusCodes.SUCCESS, response_model=OrganisationBaseSchema)
async def update_organisation_api(organisation_id: int, organisation: OrganisationBaseSchema, db: AsyncSession = Depends(get_postgres_db)):
    result = await update_organisation_by_id(db, organisation_id, organisation)
    if result["statuscode"] != 200:
        raise HTTPException(status_code=result['statuscode'], detail=result['message'])
    return response(status_code=result['statuscode'], detail=result["data"])