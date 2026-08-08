from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    category: str | None = None
    published_year: int | None = None
    is_available: bool = True

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    category: str | None = None
    published_year: int | None = None
    is_available: bool | None = None

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    category: str | None
    published_year: int | None
    is_available: bool

    model_config = {
        "from_attributes": True
    }