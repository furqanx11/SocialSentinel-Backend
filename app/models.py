from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class BaseModel(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True

class Users(BaseModel):
    name = fields.CharField(max_length=50)
    username = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(max_length=255) 
    email = fields.CharField(max_length=255, unique=True)
    role = fields.CharField(max_length=20)
    is_active = fields.BooleanField(default=True)

    class PydanticMeta:
        exclude = ['password'] 

class Posts(BaseModel):
    content = fields.TextField()

class Comments(BaseModel):
    content = fields.TextField()

class Messages(BaseModel):
    content = fields.TextField()

class UserPosts(BaseModel):
    user = fields.ForeignKeyField('models.Users', related_name='posts')
    post = fields.ForeignKeyField('models.Posts', related_name='users')

class PostComments(BaseModel):
    user = fields.ForeignKeyField('models.Users', related_name='comments')
    post = fields.ForeignKeyField('models.Posts', related_name='comments')
    comment = fields.ForeignKeyField('models.Comments', related_name='posts')

class UserMessages(BaseModel):
    user = fields.ForeignKeyField('models.Users', related_name='messages')
    message = fields.ForeignKeyField('models.Messages', related_name='users')

class Detections(BaseModel):
    post = fields.ForeignKeyField('models.Posts', related_name='detections', null=True)
    comment = fields.ForeignKeyField('models.Comments', related_name='detections', null=True)
    message = fields.ForeignKeyField('models.Messages', related_name='detections', null=True)
    model_name = fields.CharField(max_length=100)
    score = fields.FloatField()
    is_flagged = fields.BooleanField(default=False)
    reason = fields.TextField()

Users_Pydantic = pydantic_model_creator(Users, name='Users')
Posts_Pydantic = pydantic_model_creator(Posts, name='Posts')
Comments_Pydantic = pydantic_model_creator(Comments, name='Comments')
Messages_Pydantic = pydantic_model_creator(Messages, name='Messages')
UserPosts_Pydantic = pydantic_model_creator(UserPosts, name='UserPosts')
PostComments_Pydantic = pydantic_model_creator(PostComments, name='PostComments')
UserMessages_Pydantic = pydantic_model_creator(UserMessages, name='UserMessages')
Detections_Pydantic = pydantic_model_creator(Detections, name='Detections')
