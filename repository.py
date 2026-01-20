from sqlalchemy import delete, select, update
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

    @classmethod
    async def delete_one(cls, session: AsyncSession, id: int):
        query = delete(BooksModel).where(BooksModel.id == id)
        await session.execute(query)
        await session.commit()

    @classmethod
    async def update_one_complete(cls, session: AsyncSession, data: SBookAdd, id: int):
        # Исключаем поля, которые не были переданы, если это PUT (PATCH может передавать не все поля)
        book_data = data.model_dump()

        # 1. Создаем запрос на обновление
        # .returning(BooksModel) позволяет получить обновленный объект сразу после UPDATE
        stmt = (
            update(BooksModel)
            .where(BooksModel.id == id)
            .values(**book_data)
            # <-- Это ключевой момент для получения обновленного объекта
            .returning(BooksModel)
        )

        # 2. Выполняем запрос
        result = await session.execute(stmt)
        # Получаем один обновленный объект или None
        updated_book = result.scalar_one_or_none()

        # 3. Коммитим изменения
        await session.commit()

        # Возвращаем обновленный объект (или None, если не найден)
        return updated_book

    # @classmethod
    # async def update_one_partial(cls, session: AsyncSession, data: SBookPatch, id: int):
    #     book_data = data.model_dump(exclude_unset=True)
    #     if not book_data:
    #         query = select(BooksModel).where(BooksModel.id == id)
    #         result = await session.execute(query)
    #         book = result.scalars().first()
    #         if not book:
    #             return None
    #         return book
    #     stmt = (
    #         update(BooksModel)
    #         .where(BooksModel.id == id)
    #         .values(**book_data)
    #         .returning(BooksModel)
    #     )
    #     result = await session.execute(stmt)
    #     updated_book = result.scalar_one_or_none()
    #     await session.commit()
    #     return updated_book
