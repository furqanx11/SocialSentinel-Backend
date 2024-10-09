from app.crud.model_crud import CRUD
from app.schemas.post_schema import PostCreate, PostUpdate, PostRead
from app.models import Posts, Posts_Pydantic
from app.routers.routes import routes

post_crud = CRUD(Posts, Posts_Pydantic)

router = routes(
    create_func=post_crud.create,
    get_func=post_crud.get,
    get_all=post_crud.get_all,
    update_func=post_crud.update,
    delete_func=post_crud.delete,
    create_schema=PostCreate,
    response_schema=PostRead,
    update_schema=PostUpdate
)
