from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.schemas.auth_schema import SignIn, Payload, ForgotPassword, ResetPassword
from app.models.user_model import User
from app.models.role_model import RoleModel
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.common import generate_otp, send_mail, render_template_with_subject
from app.core.constants import StatusCodes
from datetime import timedelta
from app.core.config import configs
from app.core.responsehandler import response, _clean_strings
from datetime import datetime, timezone, timedelta

async def sign_in(userinfo: SignIn, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == userinfo.email))
    user = result.scalars().first()

    if not user:
        return {
            "message" : "Invalid Email or Password!",
            "statuscode" : StatusCodes.UNAUTHORIZED
        }
    
    if not verify_password(userinfo.password, user.password):
        return {
            "message" : "Invalid Email or Password!",
            "statuscode" : StatusCodes.UNAUTHORIZED
        }


    userpermission = await db.execute(select(RoleModel).where(RoleModel.role_id == user.role_id))
    useraccess = userpermission.scalars().first()

    payload = Payload(
        id=user.id,
        email=user.email,
        firstname=user.firstname,
        lastname=user.lastname,
        role=useraccess.role_name
    )

    clean_payload = _clean_strings(payload.model_dump())
    token_lifespan = timedelta(minutes= int(configs.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token, expiration_datetime  = create_access_token(clean_payload, token_lifespan)
    final_result = {
        "access_token": access_token,
        "expiration": expiration_datetime,
        "userinfo": {
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "username": user.username,
            "email": user.email
        }
    }

    return {
            "data": final_result,
            "statuscode" : StatusCodes.SUCCESS
        }



async def forget_password(user_email: ForgotPassword, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == user_email.email))
    user = result.scalars().first()
    if not user:
        return {
            "message" : "Invalid Email or Password!",
            "statuscode" : StatusCodes.UNAUTHORIZED
        }
    
    otp = generate_otp()

    user.otp = otp

    user.otp_expiration = datetime.now(timezone.utc) + timedelta(minutes=10)  # OTP valid for 10 mins
    db.add(user)
    await db.commit()
    await db.refresh(user)
    context = {
        "firstname": user.firstname,
        "otp": otp
    }
    subject, body = render_template_with_subject("forget_password.html", context)
    send_mail(user.email, subject, body, html=True)

    return {
        "data": user.otp,
        "statuscode": StatusCodes.SUCCESS
    }

async def reset_password(user_details: ResetPassword, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == user_details.email))
    user = result.scalars().first()
    if not user:
        return {
            "message" : "Invalid Email or Password!",
            "statuscode" : StatusCodes.UNAUTHORIZED
        }
    
    if user.otp != user_details.otp:
        return {
            "message" : "Invalid OTP!",
            "statuscode" : StatusCodes.BAD_REQUEST
        }

    if not user.otp_expiration or user.otp_expiration < datetime.now(timezone.utc):
        return {
            "message" : "OTP has expired!",
            "statuscode" : StatusCodes.BAD_REQUEST
        }
    
    user.password = get_password_hash(user_details.new_password)
    user.otp = None
    user.otp_expiration = None

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {
        "message": "Password Updated Successfully!",
        "statuscode" : StatusCodes.SUCCESS
    }    
