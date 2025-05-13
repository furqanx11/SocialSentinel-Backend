from datetime import datetime
from bson import ObjectId
from app.db.db import db
from .model import UserSignUp, UserFull, UserUpdate, UserLogin
from collections import Counter


users_collection = db['users']
detected_words_collection = db['detected_words']

async def create_user(user: UserSignUp):
    user_dict = user.dict()
    result = await users_collection.insert_one(user_dict)
    return str(result.inserted_id)

async def authenticate_user(user: UserLogin):
    user = await users_collection.find_one({"$or": [{"username": user.username}, {"email": user.email}], "password": user.password})
    if user:
        user["id"] = str(user["_id"])
        return UserFull(**user)
    return None

async def get_user_by_id(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user['id'] = str(user['_id'])
        
        return UserFull(**user)
    return None

async def get_user_by_username(username: str):
    user = await users_collection.find_one({"username": username})
    if user:
        user['id'] = str(user['_id'])
        return UserFull(**user)
    return None

async def get_user_by_email(email: str):
    user = await users_collection.find_one({"email": email})
    if user:
        user['id'] = str(user['_id'])
        
        return UserFull(**user)
    return None

async def update_user(user_id: str, user_data: UserUpdate):
    updated_user = await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": user_data})
    if updated_user.modified_count > 0:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user['id'] = str(user['_id'])
            return UserFull(**user)
    return None

async def delete_user(user_id: str):
    deleted_user = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if deleted_user.deleted_count > 0:
        return True
    return False

async def get_all_users():
    users = []
    async for user in users_collection.find():
        user['id'] = str(user['_id'])
        users.append(UserFull(**user))
    return users

async def get_fairness_score(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return user['fairness_score']

async def block_user(user_id: str, status:str):
    user = await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"is_blocked":True,"status": status}})
    if user.modified_count > 0:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user['id'] = str(user['_id'])
            return UserFull(**user)
    return None

async def unblock_user(user_id: str, status:str):
    user = await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"is_blocked":False,"status": status}})
    if user.modified_count > 0:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user['id'] = str(user['_id'])
            return UserFull(**user)
    return None

async def get_user_status(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return user['status']
    return None

async def add_friends(user_id: str, friend_ids: list[str]):
    await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$addToSet": {"friends": {"$each": friend_ids}}}
    )

    await users_collection.update_many(
        {"_id": {"$in": [ObjectId(fid) for fid in friend_ids]}},
        {"$addToSet": {"friends": user_id}}
    )

    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user['id'] = str(user['_id'])
        return UserFull(**user)

    return None

async def get_user_by_name(name: str):
    user = await users_collection.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})
    if user:
        user['id'] = str(user['_id'])
        return UserFull(**user)
    return None

async def get_username_by_id(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return user['username']
    return None

async def update_fairness_score(user_id: str, score: float):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user['fairness_score'] += score
        await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"fairness_score": user['fairness_score']}})
        user['id'] = str(user['_id'])
        return UserFull(**user)
    return None

async def add_detected_words(user_id: str, word:str):
    await detected_words_collection.insert_one({"user_id": user_id, "word": word, "detected_at": datetime.utcnow()})

async def get_detected_words_for_user(user_id: str):
    words = []
    async for word in detected_words_collection.find({"user_id": user_id}):
        words.append(word['word'])
    return dict(Counter(words))

async def get_all_detected_words():
    words = []
    async for word in detected_words_collection.find():
        words.append(word['word'])
    return dict(Counter(words))