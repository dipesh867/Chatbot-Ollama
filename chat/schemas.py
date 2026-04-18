from pydantic import BaseModel
from typing import List,Optional


class UserCreate(BaseModel):
    name:str
    email:str
    password:str

class UserLogin(BaseModel):
    email:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class RefreshRequest(BaseModel):
    refresh_token: str

class ConversationCreate(BaseModel):
    id:int
    title:str

    class Config:
        orm_mode=True

class ConversationCreate(BaseModel):
    title:str|None=None

class ConversationOut(BaseModel):
    id:int
    title:str
    class Config:
        orm_mode=True

class ConversationWithMessage(BaseModel):
    id:int
    title:str
    messages: List["MessageOut"]

    class Config:
        orm_mode=True

class MessageCreate(BaseModel):
    conversation_id:Optional[int]=None
    content:str

class MessageOut(BaseModel):
    id:int
    role:str
    content:str

    class Config:
        orm_mode=True
