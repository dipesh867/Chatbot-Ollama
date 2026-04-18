from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import auth_routes,user_routes,conversation_routes,message_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5501",
        "http://localhost:5501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(conversation_routes.router)
app.include_router(message_routes.router)