from sqlalchemy import Column,Integer,String,ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Conversation(Base):
    __tablename__='conversations'

    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"))
    title=Column(String(255))
    summary = Column(String(255), default="")
    messages=relationship('Message',back_populates='conversation',cascade="all,delete-orphan",passive_deletes=True)
    user=relationship('User',back_populates='conversations')

