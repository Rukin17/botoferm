from typing import AsyncGenerator

from sqlalchemy import MetaData

from src.config import my_config
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base



engine = create_async_engine(my_config.async_db_url, future=True, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()
metadata = MetaData()

async def get_db() -> AsyncGenerator:
    db: AsyncSession = async_session()
    try:
        yield db
    finally:
        await db.close()
