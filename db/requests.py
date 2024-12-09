from asyncio import Lock
import asyncio
import datetime
from db.models import User, Refferer
from sqlalchemy import func, select
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
                
    async def user_exists(self, uid: int) -> bool:
        async with self.lock:
            async with self.db_session_maker() as session:
                result = await session.execute(select(User).where(User.uid == uid))
                return result.scalar() is not None

    
    async def get_ref_code(self, name: str):
        async with self.lock:
            async with self.db_session_maker() as session:
                result = await session.execute(
                    select(Refferer.name).filter(Refferer.name == name)
                )
                
                
                return True if result.scalar() else False
            
    async def get_user_status(self, uid: int):
        async with self.lock:
            async with self.db_session_maker() as session:
                result = await session.execute(
                    select(User.status).filter(User.uid == uid)
                )
                
                
                return True if result.scalar() == 'admin' else False
            
    async def get_user_count(self):
        async with self.lock:
            async with self.db_session_maker() as session:
                result = await session.execute(
                    select(func.count(User.uid))  # Подсчитываем количество пользователей
                )
                return result.scalar()  # Возвращаем результат

            
    async def get_all_users(self):
        async with self.lock:
            async with self.db_session_maker() as session:
                result = await session.execute(
                    select(User.uid, User.uname)  # Выбираем нужные поля
                )
                return [dict(uid=row.uid, uname=row.uname) for row in result]

                