from beanie import PydanticObjectId
from fastapi_users import schemas
from fastapi_users_db_beanie import BeanieBaseUser, BeanieUserDatabase


class User(BeanieBaseUser[PydanticObjectId]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class UserRead(schemas.BaseUser[PydanticObjectId]):
    pass


async def get_user_db():
    yield BeanieUserDatabase(User)
