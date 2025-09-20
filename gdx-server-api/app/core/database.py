from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import configs

Base = declarative_base()

# Postgres Engine
postgres_engine = create_async_engine(configs.POSTGRES_URL, echo=True, future=True)
PostgresSessionLocal = sessionmaker(postgres_engine, class_=AsyncSession, expire_on_commit=False)

async def get_postgres_db():
    async with PostgresSessionLocal() as session:
        yield session