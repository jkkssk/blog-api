import json
import os
from typing import Dict
from .models import User, Post


USERS_FILE = "users.json"
POSTS_FILE = "posts.json"


def load_users() -> Dict[int, User]:
    """Загружает пользователей из файла."""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {int(k): User(**v) for k, v in data.items()}
    except Exception as e:
        print(f"Error loading users: {e}")
    return {}


def save_users(users: Dict[int, User]) -> None:
    """Сохраняет пользователей в файл."""
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            data = {k: v.dict() for k, v in users.items()}
            json.dump(data, f, indent=2, default=str)
    except Exception as e:
        print(f"Error saving users: {e}")


def load_posts() -> Dict[int, Post]:
    """Загружает посты из файла."""
    try:
        if os.path.exists(POSTS_FILE):
            with open(POSTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {int(k): Post(**v) for k, v in data.items()}
    except Exception as e:
        print(f"Error loading posts: {e}")
    return {}


def save_posts(posts: Dict[int, Post]) -> None:
    """Сохраняет посты в файл."""
    try:
        with open(POSTS_FILE, "w", encoding="utf-8") as f:
            data = {k: v.dict() for k, v in posts.items()}
            json.dump(data, f, indent=2, default=str)
    except Exception as e:
        print(f"Error saving posts: {e}")
