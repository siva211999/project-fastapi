from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags=['users']


)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash_value(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_users_id(id: int, db: Session = Depends(get_db)):
    ans_get_user_id = db.query(models.User).filter(models.User.id == id).first()

    if not ans_get_user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"your id: {id} is not valid")

    return ans_get_user_id
