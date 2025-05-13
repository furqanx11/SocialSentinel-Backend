from fastapi import APIRouter, HTTPException, Depends
from .views import (
    create_post,
    get_post_by_id,
    get_posts_by_author_id,
    update_post,
    delete_post,
    get_all_posts,
    like_post,
    add_comment_to_post,
    remove_comment_from_post,
    get_post_comments,
    get_post_likes,
    update_post_status
)
from .model import PostCreate, PostUpdate, PostFull

post_router = APIRouter(prefix="/post", tags=["Post"])

@post_router.post("/", response_model=str)
async def create_post_endpoint(post: PostCreate):
    return await create_post(post)

@post_router.get("/{post_id}", response_model=PostFull)
async def get_post_by_id_endpoint(post_id: str):
    post = await get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@post_router.get("/author/{author_id}", response_model=list[PostFull])
async def get_posts_by_author_id_endpoint(author_id: str):
    return await get_posts_by_author_id(author_id)

@post_router.patch("/{post_id}", response_model=None)
async def update_post_endpoint(post_id: str, post_data: PostUpdate):
    await update_post(post_id, post_data)

@post_router.delete("/{post_id}", response_model=None)
async def delete_post_endpoint(post_id: str):
    await delete_post(post_id)

@post_router.get("/all/", response_model=list[PostFull])
async def get_all_posts_endpoint():
    return await get_all_posts()

@post_router.patch("/{post_id}/like", response_model=None)
async def like_post_endpoint(post_id: str):
    await like_post(post_id)

@post_router.patch("/{post_id}/comment", response_model=None)
async def add_comment_to_post_endpoint(post_id: str, comment_id: str):
    await add_comment_to_post(post_id, comment_id)

@post_router.delete("/{post_id}/comment", response_model=None)
async def remove_comment_from_post_endpoint(post_id: str, comment_id: str):
    await remove_comment_from_post(post_id, comment_id)

@post_router.get("/{post_id}/comments", response_model=list[str])
async def get_post_comments_endpoint(post_id: str):
    return await get_post_comments(post_id)

@post_router.get("/{post_id}/likes", response_model=int)
async def get_post_likes_endpoint(post_id: str):
    return await get_post_likes(post_id)

@post_router.patch("/{post_id}/status", response_model=None)
async def update_post_status_endpoint(post_id: str, status: str):
    await update_post_status(post_id, status)

