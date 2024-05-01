from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


from users.crud import create_user
from users.crud import get_users
from users.crud import get_user_by_id
from users.crud import put_locktime
from users.crud import reset_locktime
from users.models import EnvStatus, TypeUser, User
from users.schemas import UserCreate, ShowUser
from uuid import UUID
from db import get_db

user_router = APIRouter(tags=['User'])


@user_router.post('/', response_model=UserCreate)
async def create_new_user(
        login: str,
        password: str,
        project_id: UUID,
        env: EnvStatus,
        domain: TypeUser,
        db: AsyncSession = Depends(get_db)
) -> User:
    new_user = await create_user(
        db=db,
        login=login,
        password=password,
        project_id=project_id,
        env=env,
        domain=domain
        )
    
    return new_user    


@user_router.get('/all_users', response_model=list[ShowUser])
async def get_all_users(db: AsyncSession = Depends(get_db)) -> list[ShowUser]:
    users = await get_users(db=db)
    return users


#TODO проверить заблокирован ли пользователь
@user_router.post('/acquire', response_model=ShowUser)
async def acquire_lock(user_id: UUID, db: AsyncSession = Depends(get_db)) -> ShowUser:
    current_user = await get_user_by_id(user_id=user_id, db=db)
    if not current_user:
        raise HTTPException(status_code=404, detail=("User doesn't exists"))
    
    locked_user = await put_locktime(user=current_user, db=db)
    return locked_user


@user_router.post('/release', response_model=ShowUser)
async def release_lock(user_id: UUID, db: AsyncSession = Depends(get_db)) -> ShowUser:
    current_user = await get_user_by_id(user_id=user_id, db=db)
    if not current_user:
        raise HTTPException(status_code=404, detail=("User dosen't exists"))
    released_user = await reset_locktime(user=current_user, db=db)
    return released_user