from sqlalchemy import Column,String,Integer,ForeignKey,Text
from sqlalchemy.orm import relationship
from database import Base

class Message(Base):
    __tablename__="messages"

    id=Column(Integer,primary_key=True,unique=True)
    conversation_id=Column(Integer,ForeignKey("conversations.id",ondelete="CASCADE"))
    role=Column(String(20))
    content=Column(Text)
    conversation=relationship("Conversation",back_populates='messages')