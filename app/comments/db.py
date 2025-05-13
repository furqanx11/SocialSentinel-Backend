from app.db.db import db
from app.auth.db import get_username_by_id
from bson import ObjectId
from .model import CommentCreate, CommentUpdate, CommentFull


comments_collection = db['comments']

async def create_comment(comment: CommentCreate):
    comment_dict = comment.dict()
    result = await comments_collection.insert_one(comment_dict)
    return str(result.inserted_id)

async def get_comment_by_id(comment_id: str):
    comment = await comments_collection.find_one({"_id": ObjectId(comment_id)})
    if comment:
        comment['id'] = str(comment['_id'])
        comment['username'] = await get_username_by_id(comment['author_id'])
        return CommentFull(**comment)
    return None

async def get_comments_by_post_id(post_id: str):
    comments = []
    async for comment in comments_collection.find({"post_id": post_id}):
        comment['id'] = str(comment['_id'])
        comment['username'] = await get_username_by_id(comment['author_id'])
        comments.append(CommentFull(**comment))
    return comments

async def update_comment(comment_id: str, comment_data: CommentUpdate):
    updated_comment = await comments_collection.update_one({"_id": ObjectId(comment_id)}, {"$set": comment_data.dict(exclude_unset=True)})
    if updated_comment.modified_count > 0:
        comment = await comments_collection.find_one({"_id": ObjectId(comment_id)})
        if comment:
            comment['id'] = str(comment['_id'])
            comment['username'] = await get_username_by_id(comment['author_id'])
            return CommentFull(**comment)
    return None

async def delete_comment(comment_id: str):
    deleted_comment = await comments_collection.delete_one({"_id": ObjectId(comment_id)})
    if deleted_comment.deleted_count > 0:
        return True
    return False

async def get_all_comments():
    comments = []
    async for comment in comments_collection.find():
        comment['id'] = str(comment['_id'])
        comment['username'] = await get_username_by_id(comment['author_id'])
        comments.append(CommentFull(**comment))
    return comments