from fastapi import FastAPI
from sqlalchemy import text
from routers.books import router as books_router
from routers.members import router as members_router
from database import engine

app = FastAPI()

@app.get("/")
def index():
  return {"message": "Hello, World!"}

@app.get("/db-check")
def db_check():
  with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
  return {"message": "Connected to Supabase successfully"}

app.include_router(books_router)
app.include_router(members_router)