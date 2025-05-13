from fastapi import APIRouter, HTTPException, Depends
from .views import (
    create_comment,
    get_comment_by_id,
    get_comments_by_post_id,
    update_comment,
    delete_comment,
    get_all_comments
)
from .model import CommentCreate, CommentUpdate, CommentFull
from app.middleware.dependecy import get_current_user

comment_router = APIRouter(prefix="/comments", tags=["comments"])

@comment_router.post("/", response_model=str)
async def create_comment_endpoint(comment: CommentCreate):
    return await create_comment(comment)

@comment_router.get("/{comment_id}", response_model=CommentFull)
async def get_comment_by_id_endpoint(comment_id: str):
    comment = await get_comment_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@comment_router.get("/post/{post_id}", response_model=list[CommentFull])
async def get_comments_by_post_id_endpoint(post_id: str):
    return await get_comments_by_post_id(post_id)

@comment_router.patch("/{comment_id}", response_model=None)
async def update_comment_endpoint(comment_id: str, comment_data: CommentUpdate):
    await update_comment(comment_id, comment_data)

@comment_router.delete("/{comment_id}", response_model=None)
async def delete_comment_endpoint(comment_id: str):
    await delete_comment(comment_id)

@comment_router.get("/all/", response_model=list[CommentFull])
async def get_all_comments_endpoint():
    return await get_all_comments()