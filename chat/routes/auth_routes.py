from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas import UserLogin, RefreshRequest,UserCreate

from auth.jwt_handler import create_access_token, create_refresh_token
from jose import jwt, JWTError

router = APIRouter()
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access = create_access_token({"user_id": db_user.id})
    refresh = create_refresh_token({"user_id": db_user.id})

    return {
        "access_token": access,
        "refresh_token": refresh,
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email
        }
    }

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User Already Exists")

    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password  # ⚠️ hash this later
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 🔐 CREATE TOKENS (same as login)
    access = create_access_token({"user_id": new_user.id})
    refresh = create_refresh_token({"user_id": new_user.id})

    return {
        "access_token": access,
        "refresh_token": refresh,
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }

@router.post("/refresh")
def refresh(data: RefreshRequest):

    try:
        payload = jwt.decode(
            data.refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        new_access = create_access_token({"user_id": user_id})

        return {"access_token": new_access}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    

@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}