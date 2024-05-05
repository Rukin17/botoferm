import datetime
from typing import Union
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.users.schemas import ShowUser
from src.users.hashing import Hasher
from src.users.models import EnvStatus, TypeUser, User


async def create_user(
        login: str,
        password: str,
        project_id: UUID,
        env: EnvStatus,
        domain: TypeUser,
        db: AsyncSession
) -> Union[User, None]:
    hashed_password = Hasher.get_password_hash(password)
    db_user = User(
        login=login,
        password=hashed_password,
        project_id=project_id,
        env=env,
        domain=domain
    )
    db.add(db_user)
    await db.commit()
    return db_user


async def get_users(db: AsyncSession) -> list[ShowUser]:
    query = select(User).order_by(User.id)
    result = await db.execute(query)
    users = result.scalars().all()
    return list(users)


async def get_user_by_id(user_id: UUID, db: AsyncSession,) -> Union[User, None]:
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user_row = result.fetchone()
    if user_row:
        return user_row[0]
    return None


# TODO datetime..!
async def put_locktime(user: User, db: AsyncSession) -> User:
    user.locktime = datetime.datetime.now().timestamp()
    await db.commit()
    return user


async def reset_locktime(user: User, db: AsyncSession) -> User:
    user.locktime = None
    await db.commit()
    return user
