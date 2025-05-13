import jwt
from datetime import datetime, timedelta
from .constants import JWT_ALGORITHM, JWT_EXPIRY, JWT_SECRET

class JWTUtils:
    def create_token(self, payload: dict) -> str:
        payload["exp"] = datetime.utcnow() + timedelta(minutes=JWT_EXPIRY)
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token

    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms = [JWT_ALGORITHM])
            return payload
        except Exception:
            return None