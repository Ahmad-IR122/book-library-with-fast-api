from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.book import Book
from schemas.books import BookCreate, BookUpdate, BookResponse

router = APIRouter(
  prefix="/books",
  tags=["Books"]
)

@router.get("/get-books", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
  return db.query(Book).all()