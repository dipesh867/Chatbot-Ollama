from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user
from database import get_db
from models.user import User
from models.conversation import Conversation
from models.message import Message
from schemas import ConversationOut,ConversationWithMessage

from jose import jwt, JWTError

router = APIRouter()



@router.get("/conversations",response_model=list[ConversationOut])
def get_conversations(db:Session=Depends(get_db),user=Depends(get_current_user)):
    
    return db.query(Conversation).filter(
        Conversation.user_id==user.id
    ).order_by(Conversation.id.desc()).all()


@router.get("/conversations/{conv_id}",response_model=ConversationWithMessage)
def get_conversation(conv_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    conv=db.query(Conversation).filter(
        Conversation.id==conv_id,Conversation.user_id==user.id
    ).first()

    if not conv:
        raise HTTPException(status_code=404,detail="Conversation Not Found")
    
    return conv

@router.delete("/conversations/{conv_id}")
def delete_conversations(conv_id:int,db: Session=Depends(get_db), user=Depends(get_current_user)):
    conv=db.query(Conversation).filter(
        Conversation.id==conv_id,
        Conversation.user_id==user.id
    ).first()
    if not conv:
        raise HTTPException(status_code=404,detail="Conversation Not Found")
    db.delete(conv)
    db.commit()

    return {"message":"deleted"}