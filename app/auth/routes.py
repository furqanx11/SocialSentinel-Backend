from fastapi import APIRouter, HTTPException, Depends
from .views import (
    create_user,
    authenticate_user,
    get_user_by_id,
    get_user_by_username,
    get_user_by_email,
    update_user,
    delete_user,
    get_all_users,
    get_fairness_score,
    block_user,
    unblock_user,
    get_user_status,
    add_friends,
    validate_token,
    get_user_by_name
)
from .model import UserSignUp, UserLogin, UserUpdate, UserFull, UserFriends
from app.middleware.dependecy import get_current_user

user_router = APIRouter(prefix="/auth", tags=["auth"])

@user_router.post("/", response_model=str)
async def user_signup(user: UserSignUp):
    return await create_user(user)

@user_router.post("/login", response_model=UserFull)
async def user_login(user: UserLogin):
    authenticated_user = await authenticate_user(user)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return authenticated_user

@user_router.get("/user/{user_id}", response_model=UserFull)
async def get_by_id(user_id: str):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.get("/username/{username}", response_model=UserFull)
async def get_by_username_endpoint(username: str):
    user = await get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.get("/email/{email}", response_model=UserFull)
async def get_by_email(email: str):
    user = await get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.patch("/{user_id}", response_model=None)
async def user_update(user_id: str, user_data: UserUpdate):
    await update_user(user_id, user_data)

@user_router.delete("/{user_id}", response_model=None)
async def user_delete(user_id: str):
    await delete_user(user_id)

@user_router.get("/", response_model=list[UserFull])
async def all_users():
    return await get_all_users()

@user_router.get("/{user_id}/fairness_score", response_model=float)
async def user_fairness_score(user_id: str):
    fairness_score = await get_fairness_score(user_id)
    if fairness_score is None:
        raise HTTPException(status_code=404, detail="User not found")
    return fairness_score

@user_router.patch("/{user_id}/block", response_model=None)
async def user_block(user_id: str, status: str):
    await block_user(user_id, status)

@user_router.patch("/{user_id}/unblock", response_model=None)
async def user_unblock(user_id: str, status: str):
    await unblock_user(user_id, status)

@user_router.get("/{user_id}/status", response_model=str)
async def get_status(user_id: str):
    status = await get_user_status(user_id)
    if status is None:
        raise HTTPException(status_code=404, detail="User not found")
    return status

@user_router.post("/add_friends", response_model=None)
async def user_friends(data: UserFriends):
    await add_friends(data)
    return {"message": "Friend added successfully"}

user_router.get("/user/validate_token", response_model=UserFull)(validate_token)

@user_router.get("/user/name/{name}", response_model=UserFull)
async def get_by_name(name: str):
    user = await get_user_by_name(name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

user_router.get("/current_user", response_model=UserFull)(get_current_user)