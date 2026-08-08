from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from database import BaseModel


class Book(BaseModel):
  __tablename__ = "books"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  title : Mapped[str] = mapped_column(String(100), nullable=False)
  author : Mapped[str] = mapped_column(String(100), nullable=False)
  category : Mapped[str | None] = mapped_column(String(100), nullable=True)
  published_year : Mapped[int | None] = mapped_column(Integer, nullable=True)
  is_available : Mapped[bool] = mapped_column(Boolean, default=True)
  