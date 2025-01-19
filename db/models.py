from contextlib import asynccontextmanager
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, String, Boolean, BigInteger, DateTime
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from datetime import datetime


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, autoincrement=True)


class User(Base):
    __tablename__ = 'users'

    uid = Column(BigInteger(), nullable=False, unique=True)
    uname = Column(String(50), nullable=True)
    status = Column(String(), default="user")
    warning = Column(Boolean(), default=False)
    created_at = Column(DateTime(), default=datetime.now())
    

class Refferer(Base):
    __tablename__ = 'referer'
    
    name = Column(String(), nullable=False, unique=True)
    count_people = Column(Integer(), default=0)
    type = Column(String(), nullable=False)


class Ref1win(Base):
    __tablename__ = '1win'
    
    uid = Column(BigInteger(), nullable=False, unique=True)
    created_at = Column(DateTime(), default=datetime.now())
    

class CreateDatabase:
    def __init__(self, database_url: str, echo: bool = False) -> None:
        """
        Инициализация асинхронного движка и сессии для работы с базой данных.
        """
        self.engine = create_async_engine(url=database_url, echo=echo)
        self.async_session = async_sessionmaker(
            bind=self.engine, 
            expire_on_commit=False,  
            class_=AsyncSession,  
            autoflush=False
        )


    @asynccontextmanager
    async def get_session(self):
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()


    async def async_main(self):
        """
        Создание всех таблиц в базе данных.
        """
        async with self.engine.begin() as conn:
            try:
                await conn.run_sync(Base.metadata.create_all)
                print("Таблицы успешно созданы")
            except Exception as e:
                print(f'Ошибка при создании таблиц: {e}')
                