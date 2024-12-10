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
            
    async def get_referer_links(self, ref_type: str):
        async with self.lock:
            async with self.db_session_maker() as session:
                result = await session.execute(
                    select(Refferer.name, Refferer.count_people)
                    .filter(Refferer.type == ref_type)
                )
                return [{"name": row.name, "count_people": row.count_people} for row in result]
    
    async def add_referer_link(self, name: str, ref_type: str):
        async with self.lock:
            async with self.db_session_maker() as session:
                new_ref = Refferer(name=name, type=ref_type, count_people=0)
                session.add(new_ref)
                await session.commit()

    async def delete_referer_link(self, name: str, ref_type: str):
        async with self.lock:
            async with self.db_session_maker() as session:
                result = await session.execute(
                    select(Refferer).filter(Refferer.name == name, Refferer.type == ref_type)
                )
                link = result.scalar_one_or_none()
                if not link:
                    return False
                await session.delete(link)
                await session.commit()
                return True
    
    async def add_admin(self, admin_id: int):
        async with self.lock:
            async with self.db_session_maker() as session:
                result = await session.execute(
                    select(User).filter(User.uid == admin_id)
                )
                user = result.scalar_one_or_none()

                if not user:
                    return False  # Пользователь не найден

                if user.status == "admin":
                    return False  # Уже является администратором

                user.status = "admin"
                await session.commit()
                return True

    async def get_all_admins(self):
        async with self.lock:
            async with self.db_session_maker() as session:
                result = await session.execute(
                    select(User.uid, User.uname).filter(User.status == "admin")
                )
                return [{"id": row.uid, "username": row.uname} for row in result]

    async def delete_admin(self, admin_id: int):
        async with self.lock:
            async with self.db_session_maker() as session:
                result = await session.execute(
                    select(User).filter(User.uid == admin_id, User.status == "admin")
                )
                user = result.scalar_one_or_none()

                if not user:
                    return False  # Пользователь не найден или не является администратором

                user.status = "user"
                await session.commit()
                return True

    async def update_admin(self, admin_id: int, new_username: str):
        async with self.lock:
            async with self.db_session_maker() as session:
                result = await session.execute(
                    select(User).filter(User.uid == admin_id, User.status == "admin")
                )
                user = result.scalar_one_or_none()

                if not user:
                    return False  # Администратор не найден

                user.uname = new_username
                await session.commit()
                return True
