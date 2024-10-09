from fastapi import APIRouter
from app.crud.model_crud import CRUD
from app.schemas.user_schema import UserCreate, UserUpdate, UserRead
from app.models import Users, Users_Pydantic
from app.routers.routes import routes

user_crud = CRUD(Users, Users_Pydantic)

router = routes(
    create_func=user_crud.create,
    get_func=user_crud.get,
    update_func=user_crud.update,
    delete_func=user_crud.delete,
    get_all=user_crud.get_all,
    create_schema=UserCreate,
    response_schema=UserRead,
    update_schema=UserUpdate
)
