from pydantic import BaseModel
from typing import Optional

class BookModel(BaseModel):
    id: int
    title: str
    author: str
    summary: Optional[str] = None