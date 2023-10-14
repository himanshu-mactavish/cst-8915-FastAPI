# user_service.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class User(BaseModel):
    username: str
    email: str

users_db: Dict[int, User] = {
    1:{"mac":"mac@localhost.com"}
}

@app.post("/users/", response_model=User)
def create_user(user: User):
    user_id = len(users_db) + 1
    users_db[user_id] = user
    return user

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    user = users_db.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User):
    user = users_db.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = updated_user.username
    user.email = updated_user.email
    return user

@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int):
    user = users_db.pop(user_id, None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
