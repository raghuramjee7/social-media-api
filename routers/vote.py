from fastapi import APIRouter, Depends, HTTPException
from database.pyd_models import VoteIn, VoteOut
from database.connect import get_db
from fastapi import status
from sqlalchemy.orm import Session
from app.utils import validate_user
from database.model import Vote, Post

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_200_OK)
async def vote(user_vote: VoteIn, db: Session = Depends(get_db), current_user: int = Depends(validate_user)):
    
    post_check = db.query(Post).filter(Post.id == user_vote.id).first()

    if post_check is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post does not exist"
            )
    
    vote_query = db.query(Vote).filter(Vote.user_id == current_user.id, Vote.post_id == user_vote.id)
    found_vote = vote_query.first()

    if user_vote.direction == 1:
        if found_vote is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User has already voted for the post"
            )
        new_vote = Vote(
            post_id = user_vote.id,
            user_id = current_user.id
        )
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {
            "message": "Vote Created"
        }
    else:
        if found_vote is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote not Found"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {
            "message": "Vote Deleted"
        }