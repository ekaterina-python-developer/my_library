from typing import Annotated

from fastapi import Depends

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

DATABASE_URL = "sqlite+aiosqlite:///library.db"
engine = create_async_engine(DATABASE_URL)
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(MappedAsDataclass, DeclarativeBase):
    pass
async def get_db():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]
