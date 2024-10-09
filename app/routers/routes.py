from fastapi import APIRouter, HTTPException, status, Response
from typing import Type, TypeVar, Callable
from pydantic import BaseModel, ValidationError
from app.exceptions.custom_exceptions import CustomValidationException
from typing import List, Any

TCreateSchema = TypeVar("TCreateSchema", bound=BaseModel)
TResponseSchema = TypeVar("TResponseSchema", bound=BaseModel)
TUpdateSchema = TypeVar("TUpdateSchema", bound=BaseModel)

def routes(
    create_func: Callable[[dict], TResponseSchema],
    get_func: Callable[[str], TResponseSchema],
    update_func: Callable[[str, dict], TResponseSchema],
    delete_func: Callable[[str], None],
    get_all : Callable[[], list[Any]],
    create_schema: Type[TCreateSchema],
    response_schema: Type[TResponseSchema],
    update_schema: Type[TUpdateSchema] 
) -> APIRouter:
    router = APIRouter() 

    @router.post("/", response_model=response_schema, status_code=status.HTTP_201_CREATED)
    async def create(item: create_schema):
        try:
            item = await create_func(item.dict())
            if not item:
                raise CustomValidationException(status_code=400, detail="Item not created.", pre = True)
            return item
        except ValidationError as e:
            raise CustomValidationException(status_code=400, detail=str(e))
    
    @router.get("/get_all", response_model=List[response_schema])
    async def read_all():
        items = await get_all()
        return items

    @router.get("/{id}", response_model=response_schema)
    async def read(id: int):
        item = await get_func(id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

    @router.patch("/{id}", response_model=response_schema)
    async def update_item(id: int, item: update_schema):
        try:
            item_data = item.dict(exclude_unset=True)
            updated_item = await update_func(id, item_data)
            if not updated_item:
                raise HTTPException(status_code=404, detail="Item not found")
            return updated_item
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=str(e))
        
    @router.delete("/{id}", response_model=None)
    async def delete(id: str):
        item_to_delete = await get_func(id)
        if not item_to_delete:
            raise HTTPException(status_code=404, detail="Item not found")
        await delete_func(id)
        return {"detail": "Item deleted successfully"}
    
    

    return router