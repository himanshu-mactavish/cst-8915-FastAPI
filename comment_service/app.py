# comment_service.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict
import requests

app = FastAPI()

class Comment(BaseModel):
    text: str
    user_id: int
    post_id: int

comments_db: Dict[int, Comment] = {}

user_service_url = "http://localhost:8001"  
post_service_url = "http://localhost:8002"

def get_user_from_user_service(user_id: int):
    user_response = requests.get(f"{user_service_url}/users/{user_id}")
    if user_response.status_code != 200:
        raise HTTPException(status_code=404, detail="User not found")
    return user_id

def get_post_from_post_service(post_id: int):
    post_response = requests.get(f"{post_service_url}/posts/{post_id}")
    if post_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Post not found")
    return post_id

# Dependencies to get the User and Post using the user and post services
def get_user(user_id: int = Depends(get_user_from_user_service)):
    return user_id

def get_post(post_id: int = Depends(get_post_from_post_service)):
    return post_id



@app.post("/comments/", response_model=Comment)
def create_comment(comment: Comment, user: int = Depends(get_user), post: int = Depends(get_post)):
    comment_id = len(comments_db) + 1
    comments_db[comment_id] = comment
    return comment

@app.get("/comments/{comment_id}", response_model=Comment)
def read_comment(comment_id: int):
    comment = comments_db.get(comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@app.put("/comments/{comment_id}", response_model=Comment)
def update_comment(comment_id: int, updated_comment: Comment):
    comment = comments_db.get(comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    comment.text = updated_comment.text
    comment.user_id = updated_comment.user_id
    comment.post_id = updated_comment.post_id
    return comment

@app.delete("/comments/{comment_id}", response_model=Comment)
def delete_comment(comment_id: int):
    comment = comments_db.pop(comment_id, None)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment