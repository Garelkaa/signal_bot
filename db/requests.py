from asyncio import Lock
import asyncio
import datetime
from db.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import joinedload

from sqlalchemy.exc import IntegrityError

class UserReq:
    def __init__(self, db_session_maker: async_sessionmaker) -> None:
        self.db_session_maker = db_session_maker
        self.lock = Lock()

    async def add_user(self, uid: int, uname: str):
        async with self.lock:
            async with self.db_session_maker() as session:
                try:
                    new_user = User(uid=uid, uname=uname)
                    session.add(new_user)
                    await session.commit()
                    return True
                except IntegrityError:
                    await session.rollback()
                    return False
                