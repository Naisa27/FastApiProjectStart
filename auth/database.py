from datetime import datetime
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from models.models import role

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column( Integer,primary_key=True)
    email: Mapped[str] = mapped_column( String( length=255 ),nullable=False)
    username: Mapped[str] = mapped_column( String( length=255 ),nullable=False)
    registered_at: Mapped[datetime] = mapped_column( TIMESTAMP,default=datetime.utcnow)
    role_id: Mapped[int] = mapped_column( Integer,ForeignKey(role.c.id))
    hashed_password: Mapped[str] = mapped_column(String(length=1024),nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean,default=True,nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean,default=False,nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean,default=False,nullable=False)


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)