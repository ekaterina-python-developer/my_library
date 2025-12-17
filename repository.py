from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.books import BooksModel
from schemas.books import SBookAdd


class BookRepository:
    @classmethod
    async def add_one(cls, data: SBookAdd, session: AsyncSession) -> BooksModel:
        book_dict = data.model_dump()
        book = BooksModel(**book_dict)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    @classmethod
    async def find_all(cls, session: AsyncSession):
        query = select(BooksModel)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_book(cls, session: AsyncSession, id: int):
        query = select(BooksModel).where(BooksModel.id == id)
        result = await session.execute(query)
        return result.scalars().first()
