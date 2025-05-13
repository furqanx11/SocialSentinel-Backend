from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt import JWTUtils
from app.auth.db import get_user_by_id
from app.utils.responses import unauthorized_response
from app.auth.model import UserFull

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
jwt = JWTUtils()

async def get_current_user(token: str = Depends(oauth2_scheme)):
    print(token)
    payload = jwt.verify_token(token)
    if not payload:
        return unauthorized_response("Invalid token")
    user_id = payload.get("user_id")
    if not user_id:
        return unauthorized_response("Invalid token")
    user = await get_user_by_id(user_id)
    if not user:
        return unauthorized_response("User not found")
    return user.id