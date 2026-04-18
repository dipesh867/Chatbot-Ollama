from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship
from database import Base
from models.conversation import Conversation

class User(Base):
    __tablename__='users'

    id=Column(Integer,primary_key=True)
    name=Column(String(255))
    email=Column(String(40),unique=True)
    password=Column(String(255))
    conversations = relationship("Conversation", back_populates="user",cascade="all,delete-orphan",passive_deletes=True)

