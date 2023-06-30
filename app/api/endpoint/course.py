from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

router = APIRouter()

@router.get("/course/test")
def test(test: str):
    return test
