from fastapi import FastAPI
from app.routes import user_routes

app = FastAPI(
    title="User CRUD API",
    description="User CRUD using FastAPI and Pydantic",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to User CRUD API"
    }


app.include_router(user_routes.router)