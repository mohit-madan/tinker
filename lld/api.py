from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Request body schema
class UserCreate(BaseModel):
    name: str
    age: int
    email: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/users/{user_id}")
def get_user(user_id:int):
    return {"user_id": user_id}

@app.post("/users")
def create_user(user: UserCreate):
    return {
        "message": "User created successfully",
        "user": user
    }