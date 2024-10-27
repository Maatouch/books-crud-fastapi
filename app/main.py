from fastapi import FastAPI, HTTPException, Depends
from app.config import get_database
from app.crud import get_books, get_book_by_id, create_book, update_book, delete_book
from app.schemas import BookSchema, BookResponseSchema
from app.models import BookModel

app = FastAPI()

@app.get("/books", response_model=list[BookResponseSchema])
async def read_books(db=Depends(get_database)):
    return await get_books(db)

@app.get("/books/{book_id}", response_model=BookResponseSchema)
async def read_book(book_id: int, db=Depends(get_database)):
    book = await get_book_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", response_model=BookResponseSchema)
async def create_new_book(book: BookSchema, db=Depends(get_database)):
    created_book = await create_book(db, book.dict(exclude_unset=True))
    return created_book

@app.put("/books/{book_id}", response_model=bool)
async def update_existing_book(book_id: int, book: BookSchema, db=Depends(get_database)):
    success = await update_book(db, book_id, book.dict())
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return success

@app.delete("/books/{book_id}", response_model=bool)
async def delete_existing_book(book_id: int, db=Depends(get_database)):
    success = await delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return success