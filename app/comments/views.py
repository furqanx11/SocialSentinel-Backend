from .db import (
    create_comment as db_create_comment,
    get_comment_by_id as db_get_comment_by_id,
    get_comments_by_post_id as db_get_comments_by_post_id,
    update_comment as db_update_comment,
    delete_comment as db_delete_comment,
    get_all_comments as db_get_all_comments
)
from .model import CommentCreate, CommentUpdate
from app.utils.responses import success_response, error_response, not_found_response

async def create_comment(comment: CommentCreate):
    try:
        comment = await db_create_comment(comment)
        return success_response(data=comment, msg="Comment created")
    except Exception as e:
        return error_response(e)

async def get_comment_by_id(comment_id: str):
    try: 
        comment = await db_get_comment_by_id(comment_id)
        if comment:
            return success_response("Comment found", comment)
        else:
            return not_found_response("Comment not found")
    except Exception as e:
        return error_response(e)

async def get_comments_by_post_id(post_id: str):
    try:
        comments = await db_get_comments_by_post_id(post_id)
        if comments:
            return success_response("Comments found", comments)
        else:
            return not_found_response("No comments found for this post")
    except Exception as e:
        return error_response(e)

async def update_comment(comment_id: str, comment_data: CommentUpdate):
    try:
        comment = await db_update_comment(comment_id, comment_data)
        if comment:
            return success_response("Comment updated", comment)
        else:
            return not_found_response("Comment not found")
    except Exception as e:
        return error_response(e)

async def delete_comment(comment_id: str):
    try:
        comment = await db_delete_comment(comment_id)
        if comment:
            return success_response("Comment deleted")
        else:
            return not_found_response("Comment not found")
    except Exception as e:
        return error_response(e)

async def get_all_comments():
    try:
        comments = await db_get_all_comments()
        if comments:
            return success_response("Comments found", comments)
        else:
            return not_found_response("No comments found")
    except Exception as e:
        return error_response(e)