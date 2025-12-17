from fastapi import APIRouter, HTTPException, status

from database import SessionDep
from repository import BookRepository
from schemas.books import SBook, SBookAdd

router = APIRouter(prefix="/books", tags=["Книги"])


@router.post("", response_model=SBook)
async def create_book(
    book: SBookAdd,
    session: SessionDep,
):
    book_model = await BookRepository.add_one(book, session)
    return book_model


@router.get("", response_model=list[SBook])
async def get_books(
    session: SessionDep,
):
    books = await BookRepository.find_all(session)
    return books


@router.get("/{id}", response_model=SBook)
async def get_book(
    session: SessionDep,
    id: int
):
    book = await BookRepository.find_book(session, id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book
