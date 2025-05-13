from .db import (
    create_post as db_create_post,
    get_post_by_id as db_get_post_by_id,
    get_posts_by_author_id as db_get_posts_by_author_id,
    update_post as db_update_post,
    delete_post as db_delete_post,
    get_all_posts as db_get_all_posts,
    like_post as db_like_post,
    add_comment_to_post as db_add_comment_to_post,
    remove_comment_from_post as db_remove_comment_from_post,
    get_post_comments as db_get_post_comments,
    get_post_likes as db_get_post_likes,
    update_post_status as db_update_post_status
)
from .model import PostCreate, PostUpdate
from app.utils.responses import success_response, error_response, not_found_response

async def create_post(post: PostCreate):
    try:
        user = await db_create_post(post)
        return success_response("Post created successfully",data={"post_id": user})
    except Exception as e:
        return error_response(str(e))

async def get_post_by_id(post_id: str):
    try:
        post = await db_get_post_by_id(post_id)
        if not post:
            return not_found_response(msg="Post not found")
        return success_response("Post fetched successfully",data=post.model_dump())
    except Exception as e:
        return error_response(str(e))

async def get_posts_by_author_id(author_id: str):
    try:
        post = await db_get_posts_by_author_id(author_id)
        if not post:
            return not_found_response(msg="Posts not found")
        return success_response("Posts fetched successfully", data=post)
    except Exception as e:
        return error_response(str(e))

async def update_post(post_id: str, post_data: PostUpdate):
    try:
        post = await db_update_post(post_id, post_data)
        if not post:
            return not_found_response(msg="Post not found")
        return success_response("Post updated successfully",data=post)
    except Exception as e:
        return error_response(str(e))

async def delete_post(post_id: str):
    try:
        post = await db_delete_post(post_id)
        if not post:
            return not_found_response(msg="Post not found")
        return success_response("Post deleted successfully")
    except Exception as e:
        return error_response(str(e))

async def get_all_posts():
    try:
        posts = await db_get_all_posts()
        if not posts:
            return not_found_response(msg="Posts not found")
        return success_response("Posts fetched successfully",data=posts)
    except Exception as e:
        return error_response(str(e))

async def like_post(post_id: str):
    try:
        await db_like_post(post_id)
        return success_response("Post liked successfully")
    except Exception as e:
        return error_response(str(e))

async def add_comment_to_post(post_id: str, comment_id: str):
    try:
        await db_add_comment_to_post(post_id, comment_id)
        return success_response("Comment added to post successfully")
    except Exception as e:
        return error_response(str(e))

async def remove_comment_from_post(post_id: str, comment_id: str):
    try:
        await db_remove_comment_from_post(post_id, comment_id)
        return success_response("Comment removed from post successfully")
    except Exception as e:
        return error_response(str(e))
    
async def get_post_comments(post_id: str):
    try:
        comments = await db_get_post_comments(post_id)
        return success_response("Post comments fetched successfully", data=comments)
    except Exception as e:
        return error_response(str(e))

async def get_post_likes(post_id: str):
    try:
        likes = await db_get_post_likes(post_id)
        return success_response("Post likes fetched successfully", data=likes)
    except Exception as e:
        return error_response(str(e))

async def update_post_status(post_id: str, status: str):
    try:
        await db_update_post_status(post_id, status)
        return success_response("Post status updated successfully")
    except Exception as e:
        return error_response(str(e))