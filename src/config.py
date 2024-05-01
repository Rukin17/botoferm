import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    async_db_url: str


def load():
    return Config(
        async_db_url=os.environ['SQLALCHEMY_ASYNC_DATABASE_URL']
    )

my_config = load()