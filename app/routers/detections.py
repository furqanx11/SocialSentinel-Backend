# from fastapi import APIRouter, HTTPException, status
# from app.models import Detections, Posts, Comments, Messages
# from app.schemas.detection_schema import FlaggedPost, FlaggedComment, FlaggedMessage
# from tortoise.exceptions import DoesNotExist
# from app.crud.elasticsearch_crud import ElasticsearchCRUD
# from typing import Optional

# # Initialize ElasticsearchCRUD with your index name
# es_crud = ElasticsearchCRUD(index_name="flagged_content")

# # Define a FastAPI router
# router = APIRouter()

# # 1. Create a document in Detections table and index in Elasticsearch
# @router.post("/", response_model=FlaggedPost, status_code=status.HTTP_201_CREATED)
# async def create_flagged_content(
#     model_name: str,
#     score: float,
#     reason: str,
#     post_id: Optional[int] = None,
#     comment_id: Optional[int] = None,
#     message_id: Optional[int] = None
    
# ):
#     # Validate that at least one of post_id, comment_id, or message_id is provided
#     if not any([post_id, comment_id, message_id]):
#         raise HTTPException(status_code=400, detail="At least one of post_id, comment_id, or message_id must be provided.")

#     content = None
#     detection_record = None

#     # Fetch the relevant content based on which ID is provided
#     if post_id:
#         try:
#             post = await Posts.get(id=post_id)
#             content = post.content
#             detection_record = await Detections.create(
#                 post=post,
#                 model_name=model_name,
#                 score=score,
#                 is_flagged=True,
#                 reason=reason
#             )
#         except DoesNotExist:
#             raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found.")
    
#     elif comment_id:
#         try:
#             comment = await Comments.get(id=comment_id)
#             content = comment.content
#             detection_record = await Detections.create(
#                 comment=comment,
#                 model_name=model_name,
#                 score=score,
#                 is_flagged=True,
#                 reason=reason
#             )
#         except DoesNotExist:
#             raise HTTPException(status_code=404, detail=f"Comment with id {comment_id} not found.")
    
#     elif message_id:
#         try:
#             message = await Messages.get(id=message_id)
#             content = message.content
#             detection_record = await Detections.create(
#                 message=message,
#                 model_name=model_name,
#                 score=score,
#                 is_flagged=True,
#                 reason=reason
#             )
#         except DoesNotExist:
#             raise HTTPException(status_code=404, detail=f"Message with id {message_id} not found.")

#     # Index the detection record in Elasticsearch
#     flagged_content = {
#         "post_id": post_id,
#         "comment_id": comment_id,
#         "message_id": message_id,
#         "content": content,
#         "reason": detection_record.reason,
#         "model_name": detection_record.model_name,
#         "score": detection_record.score,
#         "timestamp": detection_record.updated_at
#     }

#     # Index the document in Elasticsearch
#     es_crud.create(detection_record.id, flagged_content)

#     return flagged_content

# # 2. Get all flagged content from Elasticsearch
# @router.get("/", response_model=list[FlaggedPost])
# async def get_flagged_content():
#     return es_crud.get_all()

# # 3. Get flagged content by ID from Elasticsearch
# @router.get("/{id}", response_model=FlaggedPost)
# async def get_flagged_content_by_id(id: str):
#     return es_crud.get_by_id(id)

# # 4. Update a flagged content document in Elasticsearch
# @router.put("/{id}", response_model=FlaggedPost)
# async def update_flagged_content(id: str, flagged_content: FlaggedPost):
#     return es_crud.update(id, flagged_content.dict())

# # 5. Delete a flagged content document from Elasticsearch
# @router.delete("/{id}")
# async def delete_flagged_content(id: str):
#     return es_crud.delete(id)

from fastapi import APIRouter, HTTPException, status
from app.models import Detections, Posts, Comments, Messages
from app.schemas.detection_schema import FlaggedPost, CreateFlaggedContent
from tortoise.exceptions import DoesNotExist
from app.crud.elasticsearch_crud import ElasticsearchCRUD
from typing import Optional

# Initialize ElasticsearchCRUD with your index name
es_crud = ElasticsearchCRUD(index_name="flagged_content")

# Define a FastAPI router
router = APIRouter()

# 1. Create a document in Detections table and index in Elasticsearch
@router.post("/", response_model=FlaggedPost, status_code=status.HTTP_201_CREATED)
async def create_flagged_content(flagged_content: CreateFlaggedContent):
    # Validate that at least one of post_id, comment_id, or message_id is provided
    if not any([flagged_content.post_id, flagged_content.comment_id, flagged_content.message_id]):
        raise HTTPException(status_code=400, detail="At least one of post_id, comment_id, or message_id must be provided.")

    content = None
    detection_record = None

    # Fetch the relevant content based on which ID is provided
    if flagged_content.post_id:
        try:
            post = await Posts.get(id=flagged_content.post_id)
            content = post.content
            detection_record = await Detections.create(
                post=post,
                model_name=flagged_content.model_name,
                score=flagged_content.score,
                is_flagged=True,
                reason=flagged_content.reason
            )
        except DoesNotExist:
            raise HTTPException(status_code=404, detail=f"Post with id {flagged_content.post_id} not found.")
    
    elif flagged_content.comment_id:
        try:
            comment = await Comments.get(id=flagged_content.comment_id)
            content = comment.content
            detection_record = await Detections.create(
                comment=comment,
                model_name=flagged_content.model_name,
                score=flagged_content.score,
                is_flagged=True,
                reason=flagged_content.reason
            )
        except DoesNotExist:
            raise HTTPException(status_code=404, detail=f"Comment with id {flagged_content.comment_id} not found.")
    
    elif flagged_content.message_id:
        try:
            message = await Messages.get(id=flagged_content.message_id)
            content = message.content
            detection_record = await Detections.create(
                message=message,
                model_name=flagged_content.model_name,
                score=flagged_content.score,
                is_flagged=True,
                reason=flagged_content.reason
            )
        except DoesNotExist:
            raise HTTPException(status_code=404, detail=f"Message with id {flagged_content.message_id} not found.")

    # Index the detection record in Elasticsearch
    flagged_content_dict = {
        "post_id": flagged_content.post_id,
        "comment_id": flagged_content.comment_id,
        "message_id": flagged_content.message_id,
        "content": content,
        "reason": detection_record.reason,
        "model_name": detection_record.model_name,
        "score": detection_record.score,
        "timestamp": detection_record.updated_at
    }

    # Index the document in Elasticsearch
    es_crud.create(detection_record.id, flagged_content_dict)

    return flagged_content_dict

# 2. Get all flagged content from Elasticsearch
@router.get("/", response_model=list[FlaggedPost])
async def get_flagged_content():
    return es_crud.get_all()

# 3. Get flagged content by ID from Elasticsearch
@router.get("/{id}", response_model=FlaggedPost)
async def get_flagged_content_by_id(id: str):
    return es_crud.get(id)

# 4. Update a flagged content document in Elasticsearch
@router.put("/{id}", response_model=FlaggedPost)
async def update_flagged_content(id: str, flagged_content: FlaggedPost):
    return es_crud.update(id, flagged_content.dict())

# 5. Delete a flagged content document from Elasticsearch
@router.delete("/{id}")
async def delete_flagged_content(id: str):
    return es_crud.delete(id)