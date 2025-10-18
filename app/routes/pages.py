from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Any
from ..storage import load_posts, save_posts, load_users
from ..models import Post
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

posts = load_posts()
users = load_users()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request) -> Any:
    return templates.TemplateResponse(
        "index.html", {"request": request, "posts": list(posts.values())}
    )


@router.get("/new", response_class=HTMLResponse)
async def new_post_form(request: Request) -> Any:
    return templates.TemplateResponse(
        "create_post.html", {"request": request, "users": list(users.values())}
    )


@router.post("/new", response_class=HTMLResponse)
async def create_post(
    request: Request,
    author_id: int = Form(...),
    title: str = Form(...),
    content: str = Form(...),
) -> Any:
    post_id = len(posts) + 1
    now = datetime.now()
    post = Post(
        id=post_id,
        authorId=author_id,
        title=title,
        content=content,
        createdAt=now,
        updatedAt=now,
    )
    posts[post_id] = post
    save_posts(posts)
    return RedirectResponse(url=f"/posts/{post_id}", status_code=303)


@router.get("/{post_id}", response_class=HTMLResponse)
async def view_post(request: Request, post_id: int) -> Any:
    post = posts.get(post_id)
    if not post:
        return HTMLResponse("Post not found", status_code=404)
    author = users.get(post.authorId)
    return templates.TemplateResponse(
        "post.html", {"request": request, "post": post, "author": author}
    )


@router.get("/{post_id}/edit", response_class=HTMLResponse)
async def edit_post_form(request: Request, post_id: int) -> Any:
    post = posts.get(post_id)
    if not post:
        return HTMLResponse("Post not found", status_code=404)
    return templates.TemplateResponse(
        "edit_post.html", {"request": request, "post": post}
    )


@router.post("/{post_id}/edit", response_class=HTMLResponse)
async def edit_post(  # noqa: E501
    request: Request,
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
) -> Any:
    post = posts.get(post_id)
    if not post:
        return HTMLResponse("Post not found", status_code=404)
    post.title = title
    post.content = content
    post.updatedAt = datetime.now()
    posts[post_id] = post
    save_posts(posts)
    return RedirectResponse(url=f"/posts/{post_id}", status_code=303)


@router.post("/{post_id}/like", response_class=HTMLResponse)
async def like_post(request: Request, post_id: int) -> Any:
    post = posts.get(post_id)
    if not post:
        return HTMLResponse("Post not found", status_code=404)
    post.likes += 1
    post.updatedAt = datetime.now()
    posts[post_id] = post
    save_posts(posts)
    return RedirectResponse(url=f"/posts/{post_id}", status_code=303)


@router.post("/{post_id}/rate", response_class=HTMLResponse)
async def rate_post(  # noqa: E501
    request: Request, post_id: int, value: int = Form(...)
) -> Any:
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
    return RedirectResponse(url=f"/posts/{post_id}", status_code=303)
