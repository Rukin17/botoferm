import datetime
import enum
import uuid

from sqlalchemy import TIMESTAMP
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, declarative_base, mapped_column


Base = declarative_base()


class EnvStatus(enum.Enum):
    PROD = 'Prod'
    PREPROD = 'Preprod'
    STAGE = 'Stage'


class TypeUser(enum.Enum):
    CANARY = 'Canary'
    REGULAR = 'Regular'


class User(Base):
    __tablename__ = 'user'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    created_ad: Mapped[datetime.date] = mapped_column(TIMESTAMP, default=datetime.date.today())
    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    project_id: Mapped[uuid.UUID] = mapped_column()
    env: Mapped[EnvStatus]
    domain: Mapped[TypeUser]
    locktime: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP, default=None)
    
    def __repr__(self):
        return f'id {self.id}, login {self.login}'