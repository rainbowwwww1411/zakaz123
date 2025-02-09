import asyncio
import os
import random
import database.requests as rq
import keyboards as kb
from aiogram import Bot, Dispatcher
from handlers import router, Chicken
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from database.models import async_main
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from datetime import datetime


#вся система с временем
async def clock():
    while True:
        async with Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML)) as bot:
            datelist = str(datetime.now()).split(' ')[0].split('-')
            clocklist = str(datetime.now()).split(' ')[1].split(':')
            hour = int(clocklist[0])
            minutes = int(clocklist[1])
            seconds = int(clocklist[2].split('.')[0])
            month = int(datelist[1])
            number = int(datelist[2])
            if number == 1 and seconds < 1:
                users_all = await rq.get_users()
                for user in users_all:
                    await rq.clean_user(user.tg_id)
                    await asyncio.sleep(550)
            if hour == 8 and minutes == 0 and seconds < 5 or hour == 13 and minutes == 0 and seconds < 5 or hour == 20 and minutes == 0 and seconds < 5:
                users_all = await rq.get_users()
                for users in users_all:
                    if int(users.chickenhp) > 0:
                        await rq.upd_fed(users.tg_id, 'Голодная')
                    else:
                        None
                # ставим таймер на 5 минут
                await asyncio.sleep(300)
                for i in range(1, 5):
                    users_all = await rq.get_userslvl(f'{i}')
                    for users in users_all:
                        if users.fed == 'Голодная':
                            new_hp = int(users.chickenhp)-1
                            await rq.upd_hp(users.tg_id, new_hp)
                            if new_hp == 0:
                                await rq.upd_fed(users.tg_id, 'Мёртвая')
                                await rq.upd_eggs(users.tg_id, 0)
                                await bot.send_message(chat_id=users.tg_id, text='<b>Ты забыл покормить курицу!</b> Она умерла и твой баланс был обнулён.')
                                if users.invitefrom != 'None':
                                    ref_data = await rq.get_user(user.invitefrom)
                                    for ref in ref_data:
                                        ref_count = int(ref.ref_count)-1
                                        await rq.upd_count(ref.tg_id, ref_count)
                                        await bot.send_message(chat_id=ref.tg_id, text=f'<b>Курица вашего реферала погибла.</b> Теперь у вас <b>{ref_count}</b> рефералов.')

                            else:
                                await rq.upd_fed(users.tg_id, 'Сытая')
                                await bot.send_message(chat_id=users.tg_id, text='<b>Ты забыл покормить курицу и она потеряла жизнь!</b> У неё осталась последняя жизнь.')
                        else:
                            None
                    await asyncio.sleep(300)
            else:
                if hour < 8:
                    time1 = str(datetime.now()).split(' ')[1].split('.')[0]
                    time2 = "08:00:00"
                    time_format = "%H:%M:%S"
                    t1 = datetime.strptime(time1, time_format)
                    t2 = datetime.strptime(time2, time_format)
                    time_difference = t2 - t1
                    print("Разница во времени:", time_difference)
                    min=str(time_difference).split(':')[1]
                    sec=str(time_difference).split(':')[2]
                    if int(min)*60+int(sec) < 550:
                        await asyncio.sleep(550)
                    else:
                        await asyncio.sleep(int(str(time_difference).split(':')[0])*60*60+int(str(time_difference).split(':')[1])*60+int(str(time_difference).split(':')[2]))
                elif hour >= 8 and hour < 13 or hour == 8:
                    time1 = str(datetime.now()).split(' ')[1].split('.')[0]
                    time2 = "13:00:00"
                    time_format = "%H:%M:%S"
                    t1 = datetime.strptime(time1, time_format)
                    t2 = datetime.strptime(time2, time_format)
                    time_difference = t2 - t1
                    print("Разница во времени:", time_difference)
                    min=str(time_difference).split(':')[1]
                    sec=str(time_difference).split(':')[2]
                    if int(min)*60+int(sec) < 550:
                        await asyncio.sleep(550)
                    else:
                        await asyncio.sleep(int(str(time_difference).split(':')[0])*60*60+int(str(time_difference).split(':')[1])*60+int(str(time_difference).split(':')[2]))
                elif hour >= 13 and hour < 20 or hour == 13:
                    time1 = str(datetime.now()).split(' ')[1].split('.')[0]
                    time2 = "20:00:00"
                    time_format = "%H:%M:%S"
                    t1 = datetime.strptime(time1, time_format)
                    t2 = datetime.strptime(time2, time_format)
                    time_difference = t2 - t1
                    print("Разница во времени:", time_difference)
                    min=str(time_difference).split(':')[1]
                    sec=str(time_difference).split(':')[2]
                    if int(min)*60+int(sec) < 550:
                        await asyncio.sleep(550)
                    else:
                        await asyncio.sleep(int(str(time_difference).split(':')[0])*60*60+int(str(time_difference).split(':')[1])*60+int(str(time_difference).split(':')[2]))
                elif hour >= 20 or hour == 20:
                    time1 = str(datetime.now()).split(' ')[1].split('.')[0]
                    time2 = "23:59:59"
                    time_format = "%H:%M:%S"
                    t1 = datetime.strptime(time1, time_format)
                    t2 = datetime.strptime(time2, time_format)
                    time_difference = t2 - t1
                    print("Разница во времени:", time_difference)
                    min=str(time_difference).split(':')[1]
                    sec=str(time_difference).split(':')[2]
                    if int(min)*60+int(sec) < 550:
                        await asyncio.sleep(550)
                    else:
                        await asyncio.sleep(int(str(time_difference).split(':')[0])*60*60+int(str(time_difference).split(':')[1])*60+int(str(time_difference).split(':')[2]))
                        users_all = await rq.get_users()
                        for users in users_all:
                            if users.chickenhp != 0:
                                new_eggs = users.eggs + int(Chicken(level=users.chickenlvl, lives=users.chickenhp).get_chicken_info()['daily_eggs'])
                                await rq.upd_eggs(users.tg_id, new_eggs)
                                await Bot.send_message(chat_id=users.tg_id, text=f'Ты получил <b>{Chicken(level=users.chickenlvl, lives=users.chickenhp).get_chicken_info()['daily_eggs']}</b> яиц\n\nНа твоём балансе <b>{new_eggs}</b>🥚')
            await bot.close()
            
async def goldeggclock():
    while True:
        async with Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML)) as bot:
            datelist = str(datetime.now()).split(' ')[0].split('-')
            clocklist = str(datetime.now()).split(' ')[1].split(':')
            hour = int(clocklist[0])
            minutes = int(clocklist[1])
            seconds = int(clocklist[2].split('.')[0])
            month = int(datelist[1])
            number = int(datelist[2])
            if hour == 13 and minutes >= 45 and hour <= 19 or hour > 13 and hour <=19:
                r_num = random.randint(1,2)
                r_hour = random.randint(10,120)
                await asyncio.sleep(r_hour*60)
                if r_num == 1:
                    user_data = await rq.get_users()
                    for user in user_data:
                        if user.chickenlvl == '5':
                            if user.id % 2 == 0:
                                None
                            else:
                                await rq.upd_now_gold_egg(user.tg_id, 1)
                                bot.send_message('<b>‼️ Вам доступно золотое яйцо. ‼️</b> Вы должны забрать его в течении двух минут, а иначе оно сгорит.', 
                                                 reply_markup=await kb.getgoldegg())
                        else: None
                    await asyncio.sleep(2*60)
                    user_data = await rq.get_users()
                    for user in user_data:
                        if user.chickenlvl == '5':
                            if user.id % 2 == 0:
                                None
                            else:
                                if user.now_gold_egg == '1':
                                    bot.send_message('Ваше золотое яйцо сгорело.', reply_markup=await kb.del_msg())
                                else:
                                    None
                        else: None
                    await asyncio.sleep(120*60)
                    r_hour = random.randint(10,120)
                    user_data = await rq.get_users()
                    for user in user_data:
                        if user.chickenlvl == '5':
                            if user.id % 2 == 0:
                                await rq.upd_now_gold_egg(user.tg_id, '1')
                                bot.send_message('<b>‼️ Вам доступно золотое яйцо. ‼️</b> Вы должны забрать его в течении двух минут, а иначе оно сгорит.', 
                                                 reply_markup=await kb.getgoldegg())
                            else: None
                        else: None
                    await asyncio.sleep(2*60)
                    user_data = await rq.get_users()
                    for user in user_data:
                        if user.chickenlvl == '5':
                            if user.id % 2 == 0:
                                if user.now_gold_egg == '1':
                                    await rq.upd_now_gold_egg(user.tg_id, '0')
                                    bot.send_message('Ваше золотое яйцо сгорело.', reply_markup=await kb.del_msg())
                                else:
                                    None
                            else: 
                                None
                        else: None
                elif r_num == 2:
                    user_data = await rq.get_users()
                    for user in user_data:
                        if user.chickenlvl == '5':
                            if user.id % 2 == 0:
                                await rq.upd_now_gold_egg(user.tg_id, '1')
                                bot.send_message('<b>‼️ Вам доступно золотое яйцо. ‼️</b> Вы должны забрать его в течении двух минут, а иначе оно сгорит.', 
                                                 reply_markup=await kb.getgoldegg())
                            else: 
                                None
                        else: 
                            None
                    await asyncio.sleep(2*60)
                    user_data = await rq.get_users()
                    for user in user_data:
                        if user.chickenlvl == '5':
                            if user.id % 2 == 0:
                                if user.now_gold_egg == '1':
                                    bot.send_message('Ваше золотое яйцо сгорело.', reply_markup=await kb.del_msg())
                                else:
                                    None
                            else:
                                None
                        else: None
                    await asyncio.sleep(120*60)
                    r_hour = random.randint(10,120)
                    user_data = await rq.get_users()
                    for user in user_data:
                        if user.chickenlvl == '5':
                            if user.id % 2 == 0:
                                None
                            else: 
                                await rq.upd_now_gold_egg(user.tg_id, '1')
                                bot.send_message('<b>‼️ Вам доступно золотое яйцо. ‼️</b> Вы должны забрать его в течении двух минут, а иначе оно сгорит.', 
                                                 reply_markup=await kb.getgoldegg())
                        else: None
                    await asyncio.sleep(2*60)
                    user_data = await rq.get_users()
                    for user in user_data:
                        if user.chickenlvl == '5':
                            if user.id % 2 == 0:
                                None
                            else: 
                                if user.now_gold_egg == '1':
                                    await rq.upd_now_gold_egg(user.tg_id, '0')
                                    bot.send_message('Ваше золотое яйцо сгорело.', reply_markup=await kb.del_msg())
                                else:
                                    None
                        else: None
                
            else:
                if hour < 13 or hour == 13 and minutes < 45:
                    time1 = str(datetime.now()).split(' ')[1].split('.')[0]
                    time2 = "13:45:00"
                    time_format = "%H:%M:%S"
                    t1 = datetime.strptime(time1, time_format)
                    t2 = datetime.strptime(time2, time_format)
                    time_difference = t2 - t1
                    print("Разница во времени2:", time_difference)
                    min=str(time_difference).split(':')[1]
                    sec=str(time_difference).split(':')[2]
                    if int(min)*60+int(sec) < 550:
                        await asyncio.sleep(550)
                    else:
                        await asyncio.sleep(int(str(time_difference).split(':')[0])*60*60+int(str(time_difference).split(':')[1])*60+int(str(time_difference).split(':')[2]))
                elif hour > 19 or hour==19 and minutes>0:
                    time1 = str(datetime.now()).split(' ')[1].split('.')[0]
                    time2 = "00:00:00"
                    time_format = "%H:%M:%S"
                    t1 = datetime.strptime(time1, time_format)
                    t2 = datetime.strptime(time2, time_format)
                    time_difference = t2 - t1
                    print("Разница во времени2:", time_difference)
                    min=str(time_difference).split(':')[1]
                    sec=str(time_difference).split(':')[2]
                    if int(min)*60+int(sec) < 550:
                        await asyncio.sleep(550)
                    else:
                        await asyncio.sleep(int(str(time_difference).split(':')[0])*60*60+int(str(time_difference).split(':')[1])*60+int(str(time_difference).split(':')[2]))
        
        await bot.close()
        await asyncio.sleep(525)

    

async def main():
    await async_main()
    load_dotenv()
    async with Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML)) as bot:
        dp = Dispatcher(storage=MemoryStorage())
        dp.include_router(router)
        await dp.start_polling(bot)


# async def main():
#     await async_main()
#     load_dotenv()
#     bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#     dp = Dispatcher(storage=MemoryStorage())
#     dp.include_router(router)
#     await dp.start_polling(bot)

#запуск параллельно бота и времени
async def all():
    await asyncio.gather(
        main(),
        clock(),
        goldeggclock()
    )


if __name__ == "__main__":
    asyncio.run(all())
    