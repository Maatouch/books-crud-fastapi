from pydantic import BaseModel
from typing import Optional

class BookSchema(BaseModel):
    title: str
    author: str
    summary: Optional[str] = None

class BookResponseSchema(BookSchema):
    id: int