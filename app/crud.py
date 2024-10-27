from app.models import BookModel
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

async def get_books(db: AsyncIOMotorDatabase) -> List[BookModel]:
    books = []
    async for book in db["books"].find():
        book["id"] = str(book["id"])
        books.append(BookModel(**book))
    return books

async def get_book_by_id(db: AsyncIOMotorDatabase, book_id: int) -> Optional[BookModel]:
    book = await db["books"].find_one({"id": book_id})
    if book:
        return BookModel(**book)
    return None

async def create_book(db: AsyncIOMotorDatabase, book_data: dict) -> BookModel:
    book_id = await get_next_id(db, "book_id")
    book_data["id"] = book_id

    await db["books"].insert_one(book_data)
    return BookModel(**book_data)

async def update_book(db: AsyncIOMotorDatabase, book_id: int, book_data: dict) -> bool:
    result = await db["books"].update_one({"id": book_id}, {"$set": book_data})
    return result.modified_count > 0

async def get_next_id(db: AsyncIOMotorDatabase, counter_name: str) -> int:
    counter = await db["counters"].find_one_and_update(
        {"_id": counter_name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=True
    )
    return counter["sequence_value"]

async def delete_book(db: AsyncIOMotorDatabase, book_id: int) -> bool:
    result = await db["books"].delete_one({"id": book_id})
    return result.deleted_count > 0