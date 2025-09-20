from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
import asyncio

# Your DB connection URL here
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/gdxDB"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Import your User model here (adjust import path)
from app.models.user_model import User

async def verify_user_password(email: str, plain_password: str):
    # Setup async DB engine and session
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()

        if not user:
            print(f"No user found with email: {email}")
            return

        print(f"Stored hashed password for user {email}:\n{user.password}")
        print(f"Length of stored hash: {len(user.password)}")

        # Check if hash looks like a bcrypt hash
        if not (user.password.startswith("$2b$") or user.password.startswith("$2a$")) or len(user.password) != 60:
            print("Warning: Stored password does not look like a valid bcrypt hash.")

        # Verify password
        is_valid = pwd_context.verify(plain_password, user.password)
        if is_valid:
            print("Password verification success!")
        else:
            print("Password verification failed!")

if __name__ == "__main__":
    email_to_test = "vamit7631@gmail.com"
    plain_password_to_test = "Welcome@1"

    asyncio.run(verify_user_password(email_to_test, plain_password_to_test))