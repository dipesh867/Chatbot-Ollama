from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user
from database import get_db
from models.conversation import Conversation
from models.message import Message
from schemas import MessageCreate
from chatbot import get_chatbot_response
from summary import update_summary_task

router = APIRouter()


@router.post("/messages")
def send_message(
    data: MessageCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    # -----------------------------
    # 1. GET OR CREATE CONVERSATION
    # -----------------------------
    if data.conversation_id:
        conv = db.query(Conversation).filter(
            Conversation.id == data.conversation_id,
            Conversation.user_id == user.id
        ).first()

        if not conv:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found or deleted"
            )
    else:
        conv = Conversation(
            user_id=user.id,
            title=data.content[:40]
        )
        db.add(conv)
        db.commit()
        db.refresh(conv)

    # -----------------------------
    # 2. SAVE USER MESSAGE
    # -----------------------------
    user_msg = Message(
        conversation_id=conv.id,
        role="user",
        content=data.content
    )
    db.add(user_msg)
    db.commit()

    # -----------------------------
    # 3. GET AI RESPONSE
    # -----------------------------
    ai_reply = get_chatbot_response(
        user_input=data.content,
        summary=conv.summary
    )

    assistant_msg = Message(
        conversation_id=conv.id,
        role="assistant",
        content=ai_reply
    )
    db.add(assistant_msg)
    db.commit()

    # -----------------------------
    # 4. UPDATE SUMMARY (BACKGROUND)
    # -----------------------------
    background_tasks.add_task(update_summary_task, conv.id)

    # -----------------------------
    # 5. RESPONSE
    # -----------------------------
    return {
        "conversation_id": conv.id,
        "assistant_msg": {
            "id": assistant_msg.id,
            "role": "assistant",
            "content": ai_reply
        },
        "user_msg": {
            "id": user_msg.id,
            "role": "user",
            "content": data.content
        }
    }