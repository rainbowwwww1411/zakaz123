from database.models import async_session, engine
from database.models import User, w_requests
from sqlalchemy import select, update, delete
from datetime import datetime

class Chicken:
    def __init__(self, level, lives):
        self.lives = lives
        self.level = level
        self.feed_times = self.get_feed_times()
        self.daily_eggs = self.get_daily_eggs()
        self.ref_needed = self.get_ref_needed()


    def get_feed_times(self):
        feed_times = {
            1: ["8:00-8:05", "13:00-13:05", "20:00-20:05"],
            2: ["8:00-8:10", "13:00-13:10", "20:00-20:10"],
            3: ["8:00-8:15", "13:00-13:15", "20:00-20:15"],
            4: ["8:00-8:20", "13:00-13:20", "20:00-20:20"],
            5: ["8:00-8:30", "13:00-13:30", "20:00-20:30"]
        }
        return feed_times.get(self.level, [])

    def get_daily_eggs(self):
        if self.lives=='2':
            eggs_per_level = {
                1: 10,
                2: 20,
                3: 30,
                4: 40,
                5: 50
            }
        elif self.lives=='1':
            eggs_per_level = {
                1: 5,
                2: 10,
                3: 15,
                4: 20,
                5: 15
            }
        else:
            eggs_per_level = {
                1: 0,
                2: 0,
                3: 0,
                4: 0,
                5: 0
            }
        return eggs_per_level.get(self.level, 0)

    def get_ref_needed(self):
        ref_needed = {
            1: 10,
            2: 15,
            3: 20,
            4: 25,
            5: 0  
        }
        return ref_needed.get(self.level, 0)

    def get_chicken_info(self):
        return {
            "level": self.level,
            "feed_times": self.feed_times,
            "daily_eggs": self.daily_eggs,
            "ref_needed": self.ref_needed,
        }


#тут добавляем юзера в бд при /start
async def set_user(tg_id, invitefrom):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id=tg_id, chickenname='None', chickenlvl='None', fed='Голодная', invitefrom=invitefrom, ref_count='None', chickenhp='0', eggs=0, last_rob='0', now_robbery='0', now_gold_egg='0'))
            await session.commit()



async def create_req(tg_id, username, roblox_name, amount):
    async with async_session() as session:
        session.add(w_requests(tg_id=tg_id, username=username, roblox_name=roblox_name, amount=amount))
        await session.commit()

async def check_top():
    async with async_session() as session:
        return await session.scalars(select(User).order_by(User.eggs.desc()))

async def get_users():
    async with async_session() as session:
        return await session.scalars(select(User))

#выбрать пользователей по уровню
async def get_userslvl(lvl):
    async with async_session() as session:
        return await session.scalars(select(User).where(User.chickenlvl==lvl))
    
async def get_usersnight():
    async with async_session() as session:
        return await session.scalars(select(User).where(User.chickenhp>=1))

async def get_user_id(id):
    async with async_session() as session:
        return await session.scalars(select(User).where(User.id==id))

async def get_user(tg_id):
    async with async_session() as session:
        return await session.scalars(select(User).where(User.tg_id==tg_id))

async def clean_user(tg_id):
    async with engine.begin() as conn:
        await conn.execute(update(User).where(User.tg_id==tg_id).values(last_rob=0, chickenname='None', ref_count='0', last_gold_egg='0'))

async def upd_last_rob(tg_id, date):
    async with engine.begin() as conn:
        await conn.execute(update(User).where(User.tg_id==tg_id).values(last_rob=date))
        
async def upd_now_robbery(tg_id, value):
    async with engine.begin() as conn:
        await conn.execute(update(User).where(User.tg_id==tg_id).values(now_robbery=value))
    
async def upd_now_gold_egg(tg_id, value):
    async with engine.begin() as conn:
        await conn.execute(update(User).where(User.tg_id==tg_id).values(now_gold_egg=value))
    
async def upd_nightuser(tg_id, value, eggs):
    async with engine.begin() as conn:
        if value == 1:
            await conn.execute(update(User).where(User.tg_id==tg_id).values(eggs=eggs))
        elif value == 2:
            await conn.execute(update(User).where(User.tg_id==tg_id).values(chickenhp='1'))
        elif value == 3:
            await conn.execute(update(User).where(User.tg_id==tg_id).values(fed='Мёртвая', chickenhp='0', eggs=0))
    
async def upd_hp(tg_id, hp):
    async with engine.begin() as conn:
        await conn.execute(update(User).where(User.tg_id==tg_id).values(chickenhp=hp))
        
async def upd_lvl(tg_id, lvl):
    async with engine.begin() as conn:
        await conn.execute(update(User).where(User.tg_id==tg_id).values(chickenlvl=lvl))
        
async def upd_name(tg_id, name):
    async with engine.begin() as conn:
        await conn.execute(update(User).where(User.tg_id==tg_id).values(chickenname=name))
        
async def upd_eggs(tg_id, eggs):
    async with engine.begin() as conn:
        await conn.execute(update(User).where(User.tg_id==tg_id).values(eggs=eggs))
    
async def upd_count(tg_id, ref_count):
    async with engine.begin() as conn:
        await conn.execute(update(User).where(User.tg_id==tg_id).values(ref_count=ref_count))
        
async def upd_fed(tg_id, fed):
    async with engine.begin() as conn:
        if fed=='Мёртвая':
            await conn.execute(update(User).where(User.tg_id==tg_id).values(fed=fed, eggs=0))
        else:
            await conn.execute(update(User).where(User.tg_id==tg_id).values(fed=fed))
    
async def create_chicken(tg_id, name):
    async with engine.begin() as conn:
        check = str(datetime.now()).split(' ')[1].split(':')
        h=check[0]
        m=int(check[1])
        #проверка времени для выставления сытости при создании курицы
        if h == '8' and m >= 00 and m <= 5:
            await conn.execute(update(User).where(User.tg_id==tg_id).values(chickenname=name, chickenlvl='1', fed='Голодная', chickenhp='2', ref_count='0', eggs='0'))
        elif h == '13' and m >= 00 and m <= 5:
            await conn.execute(update(User).where(User.tg_id==tg_id).values(chickenname=name, chickenlvl='1', fed='Голодная', chickenhp='2', ref_count='0', eggs='0'))
        elif h == '20' and m >= 00 and m <= 5:
            await conn.execute(update(User).where(User.tg_id==tg_id).values(chickenname=name, chickenlvl='1', fed='Голодная', chickenhp='2', ref_count='0', eggs='0'))
        else:
            await conn.execute(update(User).where(User.tg_id==tg_id).values(chickenname=name, chickenlvl='1', fed='Сытая', chickenhp='2', ref_count='0', eggs=0))

async def get_reqs():
    async with async_session() as session:
        return await session.scalars(select(w_requests))

async def get_req(id):
    async with async_session() as session:
        return await session.scalars(select(w_requests).where(w_requests.id==id))

async def get_req_tgid(tg_id):
    async with async_session() as session:
        return await session.scalars(select(w_requests).where(w_requests.tg_id==tg_id))

async def del_req(id):
    async with engine.begin() as conn:
        await conn.execute(delete(w_requests).where(w_requests.id==id))
      
            
            
            