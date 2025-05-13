from app.db.db import db
from bson import ObjectId
from .model import PostCreate, PostUpdate, PostFull


posts_collection = db['posts']

async def create_post(post: PostCreate):
    post_dict = post.dict()
    result = await posts_collection.insert_one(post_dict)
    return str(result.inserted_id)

async def get_post_by_id(post_id: str):
    post = await posts_collection.find_one({"_id": ObjectId(post_id)})
    if post:
        post['id'] = str(post['_id'])
        return PostFull(**post)
    return None

async def get_posts_by_author_id(author_id: str):
    posts = []
    async for post in posts_collection.find({"author_id": author_id}):
        post['id'] = str(post['_id'])
        posts.append(PostFull(**post))
    return posts

async def update_post(post_id: str, post_data: PostUpdate):
    updated_post = posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": post_data.dict(exclude_unset=True)})
    if updated_post.modified_count > 0:
        post = await posts_collection.find_one({"_id": ObjectId(post_id)})
        if post:
            post['id'] = str(post['_id'])
            return PostFull(**post)
    return None

async def delete_post(post_id: str):
    deleted_post = posts_collection.delete_one({"_id": ObjectId(post_id)})
    if deleted_post.deleted_count > 0:
        return True
    return False

async def get_all_posts():
    posts = []
    async for post in posts_collection.find():
        post['id'] = str(post['_id'])
        posts.append(PostFull(**post))
    return posts

async def like_post(post_id: str):
    await posts_collection.update_one({"_id": ObjectId(post_id)}, {"$inc": {"likes": 1}})

async def add_comment_to_post(post_id: str, comment_id: str):
    await posts_collection.update_one({"_id": ObjectId(post_id)}, {"$push": {"comments": comment_id}})

async def remove_comment_from_post(post_id: str, comment_id: str):
    await posts_collection.update_one({"_id": ObjectId(post_id)}, {"$pull": {"comments": comment_id}})

async def get_post_comments(post_id: str):
    post = await posts_collection.find_one({"_id": ObjectId(post_id)})
    if post:
        return post.get("comments", [])
    return []

async def get_post_likes(post_id: str):
    post = await posts_collection.find_one({"_id": ObjectId(post_id)})
    if post:
        return post.get("likes", 0)
    return 0

async def update_post_status(post_id: str, status: str):
    await posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": {"status": status}})

async def get_posts_for_user(user_id: str):
    friend_list = []
    user_data = await db['users'].find_one({"_id": ObjectId(user_id)}, {"friends": 1})
    friend_list = user_data.get("friends", []) if user_data else []
    posts = []
    async for post in posts_collection.find({"$or": [{"author_id": user_id}, {"author_id": {"$in": friend_list}}]}):
        post['id'] = str(post['_id'])
        posts.append(PostFull(**post))
    return posts
