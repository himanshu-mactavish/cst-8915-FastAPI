# post_service.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import requests

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    user_id: int

posts_db: Dict[int, Post] = {}

user_service_url = "http://localhost:5000"  # Replace with the User service URL

@app.post("/posts/", response_model=Post)
def create_post(post: Post):
    # Check if the user exists
    user_response = requests.get(f"{user_service_url}/users/{post.user_id}")
    if user_response.status_code != 200:
        raise HTTPException(status_code=404, detail="User not found")
    
    post_id = len(posts_db) + 1
    posts_db[post_id] = post
    return post

@app.get("/posts/{post_id}", response_model=Post)
def read_post(post_id: int):
    post = posts_db.get(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.put("/posts/{post_id}", response_model=Post)
def update_post(post_id: int, updated_post: Post):
    post = posts_db.get(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    post.title = updated_post.title
    post.content = updated_post.content
    post.user_id = updated_post.user_id
    return post

@app.delete("/posts/{post_id}", response_model=Post)
def delete_post(post_id: int):
    post = posts_db.pop(post_id, None)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
