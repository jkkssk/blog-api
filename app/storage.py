import json
import os
from .models import User, Post

# Файлы для хранения данных
USERS_FILE = "users.json"
POSTS_FILE = "posts.json"

def load_users():
    """Загружает пользователей из файла"""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                data = json.load(f)
                return {int(k): User(**v) for k, v in data.items()}
    except Exception:
        pass
    return {}

def save_users(users):
    """Сохраняет пользователей в файл"""
    try:
        with open(USERS_FILE, 'w') as f:
            data = {k: v.dict() for k, v in users.items()}
            json.dump(data, f, indent=2, default=str)
    except Exception as e:
        print(f"Error saving users: {e}")

def load_posts():
    """Загружает посты из файла"""
    try:
        if os.path.exists(POSTS_FILE):
            with open(POSTS_FILE, 'r') as f:
                data = json.load(f)
                return {int(k): Post(**v) for k, v in data.items()}
    except Exception:
        pass
    return {}

def save_posts(posts):
    """Сохраняет посты в файл"""
    try:
        with open(POSTS_FILE, 'w') as f:
            data = {k: v.dict() for k, v in posts.items()}
            json.dump(data, f, indent=2, default=str)
    except Exception as e:
        print(f"Error saving posts: {e}")