from fastapi import FastAPI
from app.routes import users, posts

app = FastAPI(title="Blog API", version="1.0.0")

# Подключаем роутеры
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])


@app.get("/")
async def root():
    return {"message": "Blog API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8004)
