from fastapi import APIRouter, HTTPException
from ..models import User
from ..storage import save_users, load_users
from typing import List

router = APIRouter()
users = load_users()

@router.post("/", response_model=User)
async def create_user(name: str, email: str):
    user_id = len(users) + 1
    user = User(id=user_id, name=name, email=email)
    users[user_id] = user
    save_users(users)
    return user

@router.get("/", response_model=List[User])
async def list_users():
    return list(users.values())

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, name: str = None, email: str = None):
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if name: user.name = name
    if email: user.email = email
    users[user_id] = user
    save_users(users)
    return user

@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    if users.pop(user_id, None) is None:
        raise HTTPException(status_code=404, detail="User not found")
    save_users(users)
    return {"result": "deleted"}