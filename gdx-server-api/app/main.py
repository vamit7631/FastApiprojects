import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import configs
from app.api.v1.routes import routers as v1_routers
from app.core.exceptions import global_exception_handler, integrity_error_handler, http_exception_handler, auth_error_handler, AuthError
from sqlalchemy.exc import IntegrityError
from alembic import command
from alembic.config import Config
import os

app = FastAPI(
    title= configs.APP_NAME,
    version=configs.APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],    
    allow_headers=["*"],   
)

app.include_router(v1_routers, prefix=configs.API_V1_STR)

app.add_exception_handler(Exception, global_exception_handler)       # catch-all
app.add_exception_handler(IntegrityError, integrity_error_handler)  # db constraint errors
app.add_exception_handler(AuthError, auth_error_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

@app.get("/")
def root():
    return {"message": "GDX Application is Running!"}
