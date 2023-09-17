from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, models, oath2, database
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/votes",
    tags=['Vote']
)


@router.post("/")
def vote(vote_by: schemas.Vote, db: Session = Depends(database.get_db),
         current_user: int = Depends(oath2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote_by.post_id,
                                              models.Vote.user_id == current_user.id)
    vote_value = vote_query.first()

    if (vote_by.dir == 1):
        if vote_value:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"already voted")
        new_vote = models.Vote(post_id=vote_by.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully Voted" }
    else:
        if not vote_value:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"there is no vote")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted"}



