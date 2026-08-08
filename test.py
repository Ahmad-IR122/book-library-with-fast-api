"""
Book Library API - FastAPI + SQLite (via SQLModel)
----------------------------------------------------
A library system backed by a REAL database (SQLite file on disk).
Data persists across server restarts.

Setup:
    pip install fastapi uvicorn sqlmodel

Run:
    uvicorn book_library_db:app --reload

Then visit http://127.0.0.1:8000/docs

A file called "library.db" will be created in the same folder —
that's your actual database. You can inspect it with any SQLite
browser (e.g. "DB Browser for SQLite") if you're curious.
"""
"""
from fastapi import FastAPI, HTTPException, Query, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional
from enum import Enum
from contextlib import asynccontextmanager


# ---------- Database setup ----------

DATABASE_URL = "sqlite:///library.db"

# check_same_thread=False is needed only for SQLite + FastAPI's threaded workers
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency: gives each request its own DB session, closed automatically after."""
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once when the app starts up
    create_db_and_tables()
    yield
    # (nothing needed on shutdown here)


# ---------- Models ----------
# SQLModel classes double as: (1) DB table schema, (2) Pydantic validation model

class Genre(str, Enum):
    fiction = "fiction"
    nonfiction = "nonfiction"
    scifi = "scifi"
    fantasy = "fantasy"
    biography = "biography"
    history = "history"


class BookBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    genre: Genre = Genre.fiction
    year: int = Field(ge=0, le=2100)
    available: bool = True


class Book(BookBase, table=True):
    """The actual DB table. `table=True` makes this a real SQL table."""
    id: Optional[int] = Field(default=None, primary_key=True)


class BookCreate(BookBase):
    """What clients send when creating a book (no id yet)."""
    pass


class BookUpdate(SQLModel):
    """All fields optional, for partial updates (PATCH)."""
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[Genre] = None
    year: Optional[int] = None
    available: Optional[bool] = None


class BookRead(BookBase):
    """What we send back to clients (includes id)."""
    id: int


# ---------- App ----------

app = FastAPI(
    title="Book Library API (with database)",
    description="A library API backed by SQLite via SQLModel",
    version="2.0.0",
    lifespan=lifespan,
)


# ---------- Routes ----------

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Book Library API (now with a real database!)"}


@app.get("/books", response_model=list[BookRead], tags=["Books"])
def list_books(
    genre: Optional[Genre] = None,
    available: Optional[bool] = None,
    author: Optional[str] = Query(None, description="Filter by author (partial match)"),
    session: Session = Depends(get_session),
):
    """List all books, optionally filtered by genre, availability, or author."""
    query = select(Book)

    if genre is not None:
        query = query.where(Book.genre == genre)
    if available is not None:
        query = query.where(Book.available == available)
    if author is not None:
        query = query.where(Book.author.contains(author))

    return session.exec(query).all()


@app.get("/books/{book_id}", response_model=BookRead, tags=["Books"])
def get_book(book_id: int, session: Session = Depends(get_session)):
    """Get a single book by its ID."""
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    return book


@app.post("/books", response_model=BookRead, status_code=201, tags=["Books"])
def create_book(book: BookCreate, session: Session = Depends(get_session)):
    """Add a new book to the library."""
    db_book = Book.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)  # loads the auto-generated id
    return db_book


@app.patch("/books/{book_id}", response_model=BookRead, tags=["Books"])
def update_book(book_id: int, update: BookUpdate, session: Session = Depends(get_session)):
    """Partially update an existing book (only the fields you send are changed)."""
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

    update_data = update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(book, key, value)

    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@app.delete("/books/{book_id}", status_code=204, tags=["Books"])
def delete_book(book_id: int, session: Session = Depends(get_session)):
    Remove a book from the library.
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    session.delete(book)
    session.commit()
    return None


@app.post("/books/{book_id}/checkout", response_model=BookRead, tags=["Actions"])
def checkout_book(book_id: int, session: Session = Depends(get_session)):
    """Mark a book as checked out (unavailable)."""
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    if not book.available:
        raise HTTPException(status_code=400, detail="Book is already checked out")
    book.available = False
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@app.post("/books/{book_id}/return", response_model=BookRead, tags=["Actions"])
def return_book(book_id: int, session: Session = Depends(get_session)):
    """Mark a book as returned (available)."""
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    book.available = True
    session.add(book)
    session.commit()
    session.refresh(book)
    return book"""