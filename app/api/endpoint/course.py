from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

route = APIRouter()

@route.get("/course/test")
def test(test: str):
    return test
