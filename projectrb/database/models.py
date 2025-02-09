import os
from dotenv import load_dotenv
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

load_dotenv()
engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

# тут хранится пользователь
class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    chickenname: Mapped[str] = mapped_column(String(300))
    chickenlvl: Mapped[str] = mapped_column(String(200))
    chickenhp: Mapped[str] = mapped_column(String(200))
    eggs: Mapped[int] = mapped_column()
    fed: Mapped[str] = mapped_column(String(300))
    ref_count: Mapped[str] = mapped_column(String(300))
    invitefrom: Mapped[str] = mapped_column(String(300))
    last_rob: Mapped[str] = mapped_column(String(300))
    now_robbery: Mapped[str] = mapped_column(String(300))
    now_gold_egg: Mapped[str] = mapped_column(String(300))

#заявки на вывод
class w_requests(Base):
    __tablename__ = 'w_req'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(300))
    roblox_name: Mapped[str] = mapped_column(String(300))
    amount: Mapped[str] = mapped_column(String(300))
    
Session = async_sessionmaker(bind=engine)
session = Session()

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)