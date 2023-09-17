from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oath2
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)


@router.get("/", response_model=List[schemas.PostOut])
def acc_post(db: Session = Depends(get_db), users_data: int = Depends(oath2.get_current_user)):
    # cur.execute("""SELECT * FROM posts""")
    # posts = cur.fetchall()
    result = (db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
              .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)).all()
    val = db.query(models.Post).all()
    return result


@router.get("/your_post/{id_num}", response_model=schemas.Post)
def acc_post_by_number(id_num: int, db: Session = Depends(get_db), users_data: int = Depends(oath2.get_current_user)):
    # cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # get_post = cur.fetchone()
    print(users_data.email)
    get_post = db.query(models.Post).filter(models.Post.id == id_num).first()

    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id : {id} is not valid")
    if get_post.owner_id != users_data.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'it is not your postpp')

    return get_post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def acc_create(post: schemas.PostCreate, db: Session = Depends(get_db),
               users_data: int = Depends(oath2.get_current_user)):
    # cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    # (post.title, post.content, post.published))
    # new_posts = cur.fetchone()
    # conn.commit()
    print(users_data.email)
    add_post = models.Post(owner_id=users_data.id, **post.dict())
    db.add(add_post)
    db.commit()
    db.refresh(add_post)

    return add_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), users_data: int = Depends(oath2.get_current_user)):
    # cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # delete_my_post = cur.fetchone()
    # conn.commit()
    print(users_data.email)
    take = db.query(models.Post).filter(models.Post.id == id)

    take2 = take.first()

    if take.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The given id:{id} is not valid')

    if take2.owner_id != users_data.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"It is not your post")

    take.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                users_data: int = Depends(oath2.get_current_user)):
    # cur.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
    #           (post.title, post.content, post.published, str(id)))
    # up_post = cur.fetchone()
    # conn.commit()
    print(users_data.email)
    take2 = db.query(models.Post).filter(models.Post.id == id)

    sd = take2.first()

    if sd is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The given id: {id} is not valid')

    if sd.owner_id != users_data.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"It is not your post")

    take2.update(post.dict(), synchronize_session=False)
    db.commit()

    return take2.first()
