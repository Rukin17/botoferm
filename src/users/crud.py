from uuid import UUID

from users.schemas import ShowUser
from users.hashing import Hasher
from users.models import EnvStatus, TypeUser, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(
        db: AsyncSession,
        login: str,
        password: str,
        project_id: UUID,
        env: EnvStatus,
        domain: TypeUser 
) -> User:
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