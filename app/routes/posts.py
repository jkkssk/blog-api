from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from ..models import Post
from ..storage import save_posts, load_posts, load_users
from typing import List
from datetime import datetime

router = APIRouter()
posts = load_posts()
def get_users():
    return load_users()

users = get_users()

templates = Jinja2Templates(directory="app/templates")

@router.post("/", response_model=Post)
async def create_post(authorId: int, title: str, content: str):
    current_users = get_users()
    if authorId not in current_users:
        raise HTTPException(status_code=400, detail="Unknown authorId")
    post_id = len(posts) + 1
    now = datetime.now()
    post = Post(id=post_id, authorId=authorId, title=title, content=content, createdAt=now, updatedAt=now)
    posts[post_id] = post
    save_posts(posts)
    return post

@router.get("/", response_model=List[Post])
async def list_posts():
    return list(posts.values())

@router.get("/{post_id}", response_model=Post)
async def get_post(post_id: int):
    post = posts.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=Post)
async def update_post(post_id: int, title: str = None, content: str = None):
    post = posts.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if title: post.title = title
    if content: post.content = content
    post.updatedAt = datetime.now()
    posts[post_id] = post
    save_posts(posts)
    return post

@router.delete("/{post_id}", response_model=dict)
async def delete_post(post_id: int):
    if posts.pop(post_id, None) is None:
        raise HTTPException(status_code=404, detail="Post not found")
    save_posts(posts)
    return {"result": "deleted"}

@router.post("/{post_id}/like")
async def like_post(post_id: int):
    post = posts.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.likes += 1
    post.updatedAt = datetime.now()
    posts[post_id] = post
    save_posts(posts)
    return {"result": "liked", "likes": post.likes}

@router.post("/{post_id}/rate")
async def rate_post_api(post_id: int, value: int = Form(...)):
    if value < 1 or value > 5:
        raise HTTPException(status_code=400, detail="Rating must be 1-5")
    post = posts.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.ratings.append(value)
    post.rating = round(sum(post.ratings) / len(post.ratings), 2)
    post.updatedAt = datetime.now()
    posts[post_id] = post
    save_posts(posts)
    return {"result": "rated", "current_rating": post.rating, "votes": len(post.ratings)}

# ---- HTML routes
# ВАЖНО: Маршрут /new/html должен быть ВЫШЕ маршрутов с {post_id}
@router.get("/html/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "posts": list(posts.values())})

@router.get("/new/html", response_class=HTMLResponse)
async def new_post_form(request: Request):
    return templates.TemplateResponse("create_post.html", {"request": request, "users": list(users.values())})

@router.post("/new/html", response_class=HTMLResponse)
async def create_post_form(request: Request, authorId: int = Form(...), title: str = Form(...), content: str = Form(...)):
    post_id = len(posts) + 1
    now = datetime.now()
    post = Post(id=post_id, authorId=authorId, title=title, content=content, createdAt=now, updatedAt=now)
    posts[post_id] = post
    save_posts(posts)
    return RedirectResponse(url=f"/posts/{post_id}/html", status_code=303)

# Маршруты с {post_id} должны быть ПОСЛЕ /new/html
@router.get("/{post_id}/html", response_class=HTMLResponse)
async def view_post_html(request: Request, post_id: int):
    post = posts.get(post_id)
    if not post:
        return HTMLResponse("Post not found", status_code=404)
    author = users.get(post.authorId)
    return templates.TemplateResponse("post.html", {"request": request, "post": post, "author": author})

@router.get("/{post_id}/edit/html", response_class=HTMLResponse)
async def edit_post_form(request: Request, post_id: int):
    post = posts.get(post_id)
    if not post:
        return HTMLResponse("Post not found", status_code=404)
    return templates.TemplateResponse("edit_post.html", {"request": request, "post": post})

@router.post("/{post_id}/edit/html", response_class=HTMLResponse)
async def edit_post_submit(request: Request, post_id: int, title: str = Form(...), content: str = Form(...)):
    post = posts.get(post_id)
    if not post:
        return HTMLResponse("Post not found", status_code=404)
    post.title = title
    post.content = content
    post.updatedAt = datetime.now()
    posts[post_id] = post
    save_posts(posts)
    return RedirectResponse(url=f"/posts/{post_id}/html", status_code=303)

@router.post("/{post_id}/like/html", response_class=HTMLResponse)
async def like_post_html(request: Request, post_id: int):
    post = posts.get(post_id)
    if not post:
        return HTMLResponse("Post not found", status_code=404)
    post.likes += 1
    post.updatedAt = datetime.now()
    posts[post_id] = post
    save_posts(posts)
    return RedirectResponse(url=f"/posts/{post_id}/html", status_code=303)

@router.post("/{post_id}/rate/html", response_class=HTMLResponse)
async def rate_post_html(request: Request, post_id: int, value: int = Form(...)):
    post = posts.get(post_id)
    if not post:
        return HTMLResponse("Post not found", status_code=404)
    if value < 1 or value > 5:
        return HTMLResponse("Rating must be 1-5", status_code=400)
    post.ratings.append(value)
    post.rating = round(sum(post.ratings) / len(post.ratings), 2)
    post.updatedAt = datetime.now()
    posts[post_id] = post
    save_posts(posts)
    return RedirectResponse(url=f"/posts/{post_id}/html", status_code=303)