from fastapi import Header
from datetime import datetime
from .db import (
    create_user as db_create_user,
    authenticate_user as db_authenticate_user,
    get_user_by_id as db_get_user_by_id,
    get_user_by_username as db_get_user_by_username,
    get_user_by_email as db_get_user_by_email,
    update_user as db_update_user,
    delete_user as db_delete_user,
    get_all_users as db_get_all_users,
    get_fairness_score as db_get_fairness_score,
    block_user as db_block_user,
    unblock_user as db_unblock_user,
    get_user_status as db_get_user_status,
    add_friends as db_add_friends,
    get_user_by_name as db_get_user_by_name,
)
from .model import UserSignUp, UserLogin, UserUpdate, UserFriends
from app.utils.responses import success_response, error_response, not_found_response, unauthorized_response
from app.utils.jwt import JWTUtils

jwt = JWTUtils()

async def create_user(user: UserSignUp):
    try:
        username_exists = await db_get_user_by_username(user.username)
        email_exists = await db_get_user_by_email(user.email)
        if username_exists:
            return error_response("Username already exists")
        if email_exists:
            return error_response("Email already exists")
        if not user:
            return error_response("User creation failed")
        user_id = await db_create_user(user)
        token = jwt.create_token({"user_id": str(user_id)})
        return success_response("User created successfully", data=token)
    except Exception as e:
        return error_response(e)

async def authenticate_user(user: UserLogin):
    try:
        user = await db_authenticate_user(user)
        if user:
            token = jwt.create_token({"user_id": str(user.id)})
            return success_response("User authenticated successfully", token)
        else:
            return not_found_response("User not found")
    except Exception as e:
        return error_response(e)

async def get_user_by_id(user_id: str):
    try:
        user = await db_get_user_by_id(user_id)
        if user:
            user = user.dict()
            if 'last_active' in user and isinstance(user['last_active'], datetime):
                user['last_active'] = user['last_active'].isoformat()
            return success_response("User found", user)
        else:
            return not_found_response("User not found")
    except Exception as e:
        return error_response(e)

async def get_user_by_username(username: str):
    try:
        user = await db_get_user_by_username(username)
        if user:
            user = user.dict()
            if 'last_active' in user and isinstance(user['last_active'], datetime):
                user['last_active'] = user['last_active'].isoformat()
            return success_response("User found", user)
        else:
            return not_found_response("User not found")
    except Exception as e:
        return error_response(e)

async def get_user_by_email(email: str):
    try:
        user = await db_get_user_by_email(email)
        if user:
            user = user.dict()
            if 'last_active' in user and isinstance(user['last_active'], datetime):
                user['last_active'] = user['last_active'].isoformat()
            return success_response("User found", user)
        else:
            return not_found_response("User not found")
    except Exception as e:
        return error_response(e)

async def update_user(user_id: str, user_data: UserUpdate):
    try:
        user = await db_update_user(user_id, user_data.dict(exclude_unset=True))
        if user:
            user = user.dict()
            if 'last_active' in user and isinstance(user['last_active'], datetime):
                user['last_active'] = user['last_active'].isoformat()
            return success_response("User updated successfully", user)
        else:
            return not_found_response("User not found")
    except Exception as e:
        return error_response(e)

async def delete_user(user_id: str):
    try:
        user = await db_delete_user(user_id)
        if user:
            return success_response("User deleted successfully")
        else:
            return not_found_response("User not found")
    except Exception as e:
        return error_response(e)

async def get_all_users():
    try:
        users = await db_get_all_users()
        users = [user.dict() for user in users]
        for user in users:
            if 'last_active' in user and isinstance(user['last_active'], datetime):
                user['last_active'] = user['last_active'].isoformat()
        return success_response("Users retrieved successfully", users)
    except Exception as e:
        return error_response(e)
    
async def get_fairness_score(user_id: str):
    try:
        score = await db_get_fairness_score(user_id)
        if score is not None:
            return success_response("Fairness score retrieved successfully", score)
        else:
            return not_found_response("User not found")
    except Exception as e:
        return error_response(e)

async def block_user(user_id: str, status: str):
    try:
        user = await db_block_user(user_id, status)
        if user:
            user = user.dict()
            if 'last_active' in user and isinstance(user['last_active'], datetime):
                user['last_active'] = user['last_active'].isoformat()
            return success_response("User blocked successfully", user)
        else:
            return not_found_response("User not found")
    except Exception as e:
        return error_response(e)

async def unblock_user(user_id: str, status: str):
    try:
        user = await db_unblock_user(user_id, status)
        if user:
            user = user.dict()
            if 'last_active' in user and isinstance(user['last_active'], datetime):
                user['last_active'] = user['last_active'].isoformat()
            return success_response("User unblocked successfully", user)
        else:
            return not_found_response("User not found")
    except Exception as e:
        return error_response(e)


async def get_user_status(user_id: str):
    try:
        status = await db_get_user_status(user_id)
        if status is not None:
            return success_response("User status retrieved successfully", status)
        else:
            return not_found_response("User not found")
    except Exception as e:
        return error_response(e)

async def add_friends(data:UserFriends):
    try:
        user = await db_add_friends(data.user_id, data.friend_ids)
        if user:
            user = user.dict()
            return success_response("Friends added successfully", user)
        else:
            return not_found_response("User not found")
    except Exception as e:
        return error_response(e)

async def validate_token(authorization: str = Header(None)):
    try:
        if not authorization or not authorization.startswith("Bearer "):
            return unauthorized_response(msg="invalid_token")

        token = authorization.split("Bearer ")[1]
        payload = jwt.verify_token(token)
        if payload:
            print("Payload:", payload)
            return success_response(msg="token_valid", data=payload)
        return unauthorized_response(msg="invalid_token")
    except Exception as e:
        return error_response(e)

async def get_user_by_name(name: str):
    try:
        user = await db_get_user_by_name(name)
        if user:
            user = user.dict()
            return success_response("User found", user)
        else:
            return not_found_response("User not found")
    except Exception as e:
        return error_response(e)