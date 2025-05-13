import os
from dotenv import load_dotenv

load_dotenv()

# Database
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_USER_NAME = os.getenv("MONGO_USER_NAME")
MONGO_USER_PASSWORD = os.getenv("MONGO_USER_PASSWORD")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXPIRY = int(os.getenv("JWT_EXPIRY"))
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")