import database.requests as rq
import keyboards as kb
import os, math, asyncio, random, calendar
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from admin import IsAdmin, IsAdmin2
from flyerapi import Flyer
from aiogram.utils.deep_linking import create_start_link, decode_payload
from datetime import datetime

router = Router()
flyer = Flyer(key=os.getenv('FLAYER_KEY'))
media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')
admins_list = [6299587911, 780102984]

chicken_smile = ['🐣', '🐤', '🐥', '🐔', '🐓']

fed_smile = {
    'Сытая': '😊',
    'Голодная': '😋',
    'Мёртвая': '😵'
}

async def getimg():
    lvl1 = FSInputFile(path=os.path.join(media_dir, '1lvl.jpg'))
    lvl2 = FSInputFile(path=os.path.join(media_dir, '2lvl.jpg'))
    lvl3 = FSInputFile(path=os.path.join(media_dir, '3lvl.jpg'))
    lvl4 = FSInputFile(path=os.path.join(media_dir, '4lvl.jpg'))
    lvl5 = FSInputFile(path=os.path.join(media_dir, '5lvl.jpg'))
    win = FSInputFile(path=os.path.join(media_dir, 'win.jpg'))
    lose = FSInputFile(path=os.path.join(media_dir, 'lose.jpg'))
    dead = FSInputFile(path=os.path.join(media_dir, 'dead.jpg'))
    swap = FSInputFile(path=os.path.join(media_dir, 'swap.jpg'))
    nightattack = FSInputFile(path=os.path.join(media_dir, 'nightattack.jpg'))
    return lvl1, lvl2, lvl3, lvl4, lvl5, win, lose, dead, swap, nightattack

async def getimgurl():
    lvl1 = InputMediaPhoto(media='https://ibb.co/xt5QhCYq')
    lvl2 = InputMediaPhoto(media='https://ibb.co/HDs3gZC6')
    lvl3 = InputMediaPhoto(media='https://ibb.co/qf18c4M')
    lvl4 = InputMediaPhoto(media='https://ibb.co/0j8ZP9Tx')
    lvl5 = InputMediaPhoto(media='https://ibb.co/MXv4Zq2')
    win = InputMediaPhoto(media='https://ibb.co/fVTZ3c1T')
    lose = InputMediaPhoto(media='https://ibb.co/Dfj8YFJn')
    dead = InputMediaPhoto(media='https://ibb.co/ycdYVDvG')
    swap = InputMediaPhoto(media='https://ibb.co/gbvxSLKs')
    nightattack = InputMediaPhoto(media='https://ibb.co/gLSnzb2k')
    return lvl1, lvl2, lvl3, lvl4, lvl5, win, lose, dead, swap, nightattack

class get(StatesGroup):
    chickenname = State()
    robber_tg_id = State()
    user_id = State()
    roblox_name = State()
    amount = State()
    user_message = State()
    message = State()
    message2 = State()
    to_id = State()
    req_id = State()
    hp = State()
    fed = State()
    lvl = State()
    eggs = State()
    name = State()
    ref_count = State()
    upd_id = State()
    tg_id = State()
    mail = State()

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

@router.message(CommandStart())
async def start(message: Message, state: FSMContext, bot: Bot):
    print(message.text)
    await message.answer('<b>ЧТОБЫ ПОЛУЧИТЬ РОБУКСЫ БЕЗ ЛОГИНА И ПАРОЛЯ ВСТУПИ В ГРУППУ👇👇👇</b>', reply_markup=await kb.linkgroup())
    if message.text == '/start':
        await rq.set_user(message.from_user.id, 'None')
    else:
        invatitefrom = decode_payload(message.text.split(' ')[1])
        print(invatitefrom)
        from_data = await rq.get_user(invatitefrom)
        for fromuser in from_data:
            if int(fromuser.chickenhp) > 0:
                await rq.set_user(message.from_user.id, invatitefrom)
                new_ref_count = int(fromuser.ref_count) + 1
                await rq.upd_count(invatitefrom, new_ref_count)
            else:
                await rq.set_user(message.from_user.id, 'None')
    user_data = await rq.get_user(message.from_user.id)
    for user in user_data:
        if user.chickenname == 'None':
            await message.answer("🐣 Введите имя для вашей курицы:")
            await state.set_state(get.chickenname)
        else:
            img = await getimg()
            link = await create_start_link(bot,str(message.from_user.id), encode=True)
            feed_time = Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['feed_times']
            feed_times = str(f'{feed_time[0]}, {feed_time[1]}, {feed_time[2]}')
            await bot.send_photo(photo=img[int(user.chickenlvl)-1], chat_id=message.from_user.id, 
                                 caption=f"{chicken_smile[int(user.chickenlvl)-1]} <b>Имя курицы: {user.chickenname}</b>\n\n💰 Баланс: <b>{user.eggs}</b>\n🥚 Яиц в день: <b>{Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['daily_eggs']}</b>\n\n📊 Уровень курицы: <b>{user.chickenlvl}</b>\n{fed_smile[user.fed]} Состояние курицы: <b>{user.fed}</b>\n♥️ Кол-во жизней: <b>{user.chickenhp}</b>\n\n⏰ Время кормить: <b>{feed_times}</b>\n\n👥 Кол-во рефов: <b>{user.ref_count}</b>\n🔗 Ваша реферальная ссылка: <code>{link}</code>",
                                 reply_markup=await kb.menu())

@router.message(get.chickenname)
async def chickenname(message: Message, state: FSMContext, bot: Bot):
    img = await getimg()
    await rq.create_chicken(message.from_user.id, message.text)
    user_data = await rq.get_user(message.from_user.id)
    link = await create_start_link(bot,str(message.from_user.id), encode=True)
    for user in user_data:
        feed_time = Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['feed_times']
        feed_times = str(f'{feed_time[0]}, {feed_time[1]}, {feed_time[2]}')
        await bot.send_photo(photo=img[int(user.chickenlvl)-1], chat_id=message.from_user.id, 
                                 caption=f"{chicken_smile[int(user.chickenlvl)-1]} <b>Имя курицы: {user.chickenname}</b>\n\n💰 Баланс: <b>{user.eggs}</b>\n🥚 Яиц в день: <b>{Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['daily_eggs']}</b>\n\n📊 Уровень курицы: <b>{user.chickenlvl}</b>\n{fed_smile[user.fed]} Состояние курицы: <b>{user.fed}</b>\n♥️ Кол-во жизней: <b>{user.chickenhp}</b>\n\n⏰ Время кормить: <b>{feed_times}</b>\n\n👥 Кол-во рефов: <b>{user.ref_count}</b>\n🔗 Ваша реферальная ссылка: <code>{link}</code>",
                                 reply_markup=await kb.menu())
    await state.clear()
    
@router.callback_query(F.data=='getgoldegg')
async def getgoldegg(callback: CallbackQuery, bot: Bot):
    user_data = await rq.get_user(callback.from_user.id)
    for user in user_data:
        if user.now_gold_egg == 1:
            await rq.upd_eggs(callback.from_user.id, user.eggs+10)
            await rq.upd_now_gold_egg(callback.from_user.id, 0)
            await callback.message.edit_text('<b>Вы успешно забрали золотое яйцо!</b>\n\nНа ваш баланс было начислено <b>10</b> яиц.', reply_markup=await kb.del_msg())
        else:
             await callback.message.edit_text('<b>Вы не успели забрать золотое яйцо!</b>\nПопробуйте в следующий раз.', reply_markup=await kb.del_msg())


@router.callback_query(F.data=='fed')
async def fed(callback: CallbackQuery, bot: Bot):
    check = await flyer.check(user_id=callback.from_user.id, language_code=callback.from_user.language_code)
    if not check:
        return
    else:
        img = await getimg()
        link = await create_start_link(bot,str(callback.from_user.id), encode=True)
        check = str(datetime.now()).split(' ')[1].split(':')
        h = check[0]
        m = int(check[1])
        user_data = await rq.get_user(callback.from_user.id)
        for user in user_data:
            if user.chickenlvl == '1':
                if h == '8' and m >= 00 and m <= 5 or h == '13' and m >= 00 and m <= 5 or h == '20' and m >= 00 and m <= 5:
                    if user.fed == 'Голодная':
                        await rq.upd_fed(callback.from_user.id, 'Сытая')
                        await callback.answer(text='Вы покормили курицу!')
                        feed_time = Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['feed_times']
                        feed_times = str(f'{feed_time[0]}, {feed_time[1]}, {feed_time[2]}')
                        await bot.edit_message_caption(message_id=callback.message.message_id,chat_id=callback.from_user.id, 
                                    caption=f"{chicken_smile[int(user.chickenlvl)-1]} <b>Имя курицы: {user.chickenname}</b>\n\n💰 Баланс: <b>{user.eggs}</b>\n🥚 Яиц в день: <b>{Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['daily_eggs']}</b>\n\n📊 Уровень курицы: <b>{user.chickenlvl}</b>\n{fed_smile[user.fed]} Состояние курицы: <b>{user.fed}</b>\n♥️ Кол-во жизней: <b>{user.chickenhp}</b>\n\n⏰ Время кормить: <b>{feed_times}</b>\n\n👥 Кол-во рефов: <b>{user.ref_count}</b>\n🔗 Ваша реферальная ссылка: <code>{link}</code>",
                                    reply_markup=await kb.menu())
                    elif user.fed == 'Сытая':
                        await callback.answer(text='Ваша курица сыта!')
                    else:
                        await callback.answer(text='Ваша курица мертва!')
                else:
                    await callback.answer(text='Ваша курица сыта!')
            elif user.chickenlvl == '2':
                if h == '8' and m >= 00 and m <= 10 or h == '13' and m >= 00 and m <= 10 or h == '20' and m >= 00 and m <= 10:
                    if user.fed == 'Голодная':
                        await rq.upd_fed(callback.from_user.id, 'Сытая')
                        await callback.answer(text='Вы покормили курицу!')
                        feed_time = Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['feed_times']
                        feed_times = str(f'{feed_time[0]}, {feed_time[1]}, {feed_time[2]}')
                        await bot.edit_message_caption(message_id=callback.message.message_id,chat_id=callback.from_user.id, 
                                    caption=f"{chicken_smile[int(user.chickenlvl)-1]} <b>Имя курицы: {user.chickenname}</b>\n\n💰 Баланс: <b>{user.eggs}</b>\n🥚 Яиц в день: <b>{Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['daily_eggs']}</b>\n\n📊 Уровень курицы: <b>{user.chickenlvl}</b>\n{fed_smile[user.fed]} Состояние курицы: <b>{user.fed}</b>\n♥️ Кол-во жизней: <b>{user.chickenhp}</b>\n\n⏰ Время кормить: <b>{feed_times}</b>\n\n👥 Кол-во рефов: <b>{user.ref_count}</b>\n🔗 Ваша реферальная ссылка: <code>{link}</code>",
                                    reply_markup=await kb.menu())
                    elif user.fed == 'Сытая':
                        await callback.answer(text='Ваша курица сыта!')
                    else:
                        await callback.answer(text='Ваша курица мертва!')
                else:
                    await callback.answer(text='Ваша курица сыта!')
            elif user.chickenlvl == '3':
                if h == '8' and m >= 00 and m <= 15 or h == '13' and m >= 00 and m <= 15 or h == '20' and m >= 00 and m <= 15:
                    if user.fed == 'Голодная':
                        await rq.upd_fed(callback.from_user.id, 'Сытая')
                        await callback.answer(text='Вы покормили курицу!')
                        feed_time = Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['feed_times']
                        feed_times = str(f'{feed_time[0]}, {feed_time[1]}, {feed_time[2]}')
                        await bot.edit_message_caption(message_id=callback.message.message_id,chat_id=callback.from_user.id, 
                                    caption=f"{chicken_smile[int(user.chickenlvl)-1]} <b>Имя курицы: {user.chickenname}</b>\n\n💰 Баланс: <b>{user.eggs}</b>\n🥚 Яиц в день: <b>{Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['daily_eggs']}</b>\n\n📊 Уровень курицы: <b>{user.chickenlvl}</b>\n{fed_smile[user.fed]} Состояние курицы: <b>{user.fed}</b>\n♥️ Кол-во жизней: <b>{user.chickenhp}</b>\n\n⏰ Время кормить: <b>{feed_times}</b>\n\n👥 Кол-во рефов: <b>{user.ref_count}</b>\n🔗 Ваша реферальная ссылка: <code>{link}</code>",
                                    reply_markup=await kb.menu())
                    elif user.fed == 'Сытая':
                        await callback.answer(text='Ваша курица сыта!')
                    else:
                        await callback.answer(text='Ваша курица мертва!')
                else:
                    await callback.answer(text='Ваша курица сыта!')
            elif user.chickenlvl == '4':
                if h == '8' and m >= 00 and m <= 20 or h == '13' and m >= 00 and m <= 20 or h == '20' and m >= 00 and m <= 20:
                    if user.fed == 'Голодная':
                        await rq.upd_fed(callback.from_user.id, 'Сытая')
                        await callback.answer(text='Вы покормили курицу!')
                        feed_time = Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['feed_times']
                        feed_times = str(f'{feed_time[0]}, {feed_time[1]}, {feed_time[2]}')
                        await bot.edit_message_caption(message_id=callback.message.message_id,chat_id=callback.from_user.id, 
                                    caption=f"{chicken_smile[int(user.chickenlvl)-1]} <b>Имя курицы: {user.chickenname}</b>\n\n💰 Баланс: <b>{user.eggs}</b>\n🥚 Яиц в день: <b>{Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['daily_eggs']}</b>\n\n📊 Уровень курицы: <b>{user.chickenlvl}</b>\n{fed_smile[user.fed]} Состояние курицы: <b>{user.fed}</b>\n♥️ Кол-во жизней: <b>{user.chickenhp}</b>\n\n⏰ Время кормить: <b>{feed_times}</b>\n\n👥 Кол-во рефов: <b>{user.ref_count}</b>\n🔗 Ваша реферальная ссылка: <code>{link}</code>",
                                    reply_markup=await kb.menu())
                    elif user.fed == 'Сытая':
                        await callback.answer(text='Ваша курица сыта!')
                    else:
                        await callback.answer(text='Ваша курица мертва!')
                else:
                    await callback.answer(text='Ваша курица сыта!')
            elif user.chickenlvl == '5':
                if h == '8' and m >= 00 and m <= 30 or h == '13' and m >= 00 and m <= 30 or h == '20' and m >= 00 and m <= 30:
                    if user.fed == 'Голодная':
                        await rq.upd_fed(callback.from_user.id, 'Сытая')
                        await callback.answer(text='Вы покормили курицу!')
                        feed_time = Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['feed_times']
                        feed_times = str(f'{feed_time[0]}, {feed_time[1]}, {feed_time[2]}')
                        await bot.edit_message_caption(message_id=callback.message.message_id,chat_id=callback.from_user.id, 
                                    caption=f"{chicken_smile[int(user.chickenlvl)-1]} <b>Имя курицы: {user.chickenname}</b>\n\n💰 Баланс: <b>{user.eggs}</b>\n🥚 Яиц в день: <b>{Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['daily_eggs']}</b>\n\n📊 Уровень курицы: <b>{user.chickenlvl}</b>\n{fed_smile[user.fed]} Состояние курицы: <b>{user.fed}</b>\n♥️ Кол-во жизней: <b>{user.chickenhp}</b>\n\n⏰ Время кормить: <b>{feed_times}</b>\n\n👥 Кол-во рефов: <b>{user.ref_count}</b>\n🔗 Ваша реферальная ссылка: <code>{link}</code>",
                                    reply_markup=await kb.menu())
                    elif user.fed == 'Сытая':
                        await callback.answer(text='Ваша курица сыта!')
                    else:
                        await callback.answer(text='Ваша курица мертва!')
                else:
                    await callback.answer(text='Ваша курица сыта!')

@router.callback_query(F.data.startswith('toknow'))
async def toknow(callback: CallbackQuery, bot: Bot):
    user_data = await rq.get_user(callback.from_user.id)
    for user in user_data:
        if user.eggs>30:
            await callback.message.edit_text(f'TGID грабителя: <b>{callback.data.split('_')[1]}</b>\n\nЗа услугу было списано 30 яиц.')

@router.callback_query(F.data=='top')
async def fed(callback: CallbackQuery, bot: Bot):
    top_users = await rq.check_top()
    toppers = []
    for top in top_users:
        toppers.append([top.tg_id, top.chickenname, top.eggs])
    try:
        await callback.message.answer(f'''<b>🏆 Топ пользователей:</b>
                                      
🥇 {toppers[0][1]} - {toppers[0][2]} яиц
🥈 {toppers[1][1]} - {toppers[1][2]} яиц
🥉 {toppers[2][1]} - {toppers[2][2]} яиц
🏅 {toppers[3][1]} - {toppers[3][2]} яиц
🏅 {toppers[4][1]} - {toppers[4][2]} яиц''', reply_markup=await kb.del_msg())
    except Exception as e:
        print(e)
        await callback.answer('Топ пустой')

@router.callback_query(F.data=='up_lvl')
async def up_lvl(callback: CallbackQuery, bot: Bot):
    img = await getimgurl()
    link = await create_start_link(bot,str(callback.from_user.id), encode=True)
    user_data = await rq.get_user(callback.from_user.id)
    for user in user_data:
        if int(user.chickenlvl) == 1 and int(user.ref_count) >= 10:
            await rq.upd_lvl(callback.from_user.id, 2)
            await callback.answer('Ваш уровень был обновлен до 2')
            feed_time = Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['feed_times']
            feed_times = str(f'{feed_time[0]}, {feed_time[1]}, {feed_time[2]}')
            await bot.edit_message_media(chat_id=callback.from_user.id, message_id=callback.message.message_id, media=img[1])
            await bot.edit_message_caption(chat_id=callback.from_user.id, message_id=callback.message.message_id, caption=f"{chicken_smile[int(user.chickenlvl)-1]} <b>Имя курицы: {user.chickenname}</b>\n\n💰 Баланс: <b>{user.eggs}</b>\n🥚 Яиц в день: <b>{Chicken(level=2, lives=user.chickenhp).get_chicken_info()['daily_eggs']}</b>\n\n📊 Уровень курицы: <b>2</b>\n{fed_smile[user.fed]} Состояние курицы: <b>{user.fed}</b>\n♥️ Кол-во жизней: <b>{user.chickenhp}</b>\n\n⏰ Время кормить: <b>{feed_times}</b>\n\n👥 Кол-во рефов: <b>{user.ref_count}</b>\n🔗 Ваша реферальная ссылка: <code>{link}</code>", 
                                           reply_markup=await kb.menu())
        elif int(user.chickenlvl) == 2 and int(user.ref_count) >= 25:
            await rq.upd_lvl(callback.from_user.id, 3)
            await callback.answer('Ваш уровень был обновлен до 3')
            feed_time = Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['feed_times']
            feed_times = str(f'{feed_time[0]}, {feed_time[1]}, {feed_time[2]}')
            await bot.edit_message_media(chat_id=callback.from_user.id, message_id=callback.message.message_id, media=img[2])
            await bot.edit_message_caption(chat_id=callback.from_user.id, message_id=callback.message.message_id, caption=f"{chicken_smile[int(user.chickenlvl)-1]} <b>Имя курицы: {user.chickenname}</b>\n\n💰 Баланс: <b>{user.eggs}</b>\n🥚 Яиц в день: <b>{Chicken(level=3, lives=user.chickenhp).get_chicken_info()['daily_eggs']}</b>\n\n📊 Уровень курицы: <b>3</b>\n{fed_smile[user.fed]} Состояние курицы: <b>{user.fed}</b>\n♥️ Кол-во жизней: <b>{user.chickenhp}</b>\n\n⏰ Время кормить: <b>{feed_times}</b>\n\n👥 Кол-во рефов: <b>{user.ref_count}</b>\n🔗 Ваша реферальная ссылка: <code>{link}</code>", 
                                           reply_markup=await kb.menu())
        elif int(user.chickenlvl) == 3 and int(user.ref_count) >= 45:
            await rq.upd_lvl(callback.from_user.id, 4)
            await callback.answer('Ваш уровень был обновлен до 4')
            feed_time = Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['feed_times']
            feed_times = str(f'{feed_time[0]}, {feed_time[1]}, {feed_time[2]}')
            await bot.edit_message_media(chat_id=callback.from_user.id, message_id=callback.message.message_id, media=img[3])
            await bot.edit_message_caption(chat_id=callback.from_user.id, message_id=callback.message.message_id, caption=f"{chicken_smile[int(user.chickenlvl)-1]} <b>Имя курицы: {user.chickenname}</b>\n\n💰 Баланс: <b>{user.eggs}</b>\n🥚 Яиц в день: <b>{Chicken(level=4, lives=user.chickenhp).get_chicken_info()['daily_eggs']}</b>\n\n📊 Уровень курицы: <b>4</b>\n{fed_smile[user.fed]} Состояние курицы: <b>{user.fed}</b>\n♥️ Кол-во жизней: <b>{user.chickenhp}</b>\n\n⏰ Время кормить: <b>{feed_times}</b>\n\n👥 Кол-во рефов: <b>{user.ref_count}</b>\n🔗 Ваша реферальная ссылка: <code>{link}</code>", 
                                           reply_markup=await kb.menu())
        elif int(user.chickenlvl) == 4 and int(user.ref_count) >= 70:
            await rq.upd_lvl(callback.from_user.id, 5)
            await callback.answer('Ваш уровень был обновлен до 5')
            feed_time = Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['feed_times']
            feed_times = str(f'{feed_time[0]}, {feed_time[1]}, {feed_time[2]}')
            await bot.edit_message_media(chat_id=callback.from_user.id, message_id=callback.message.message_id, media=img[4])
            await bot.edit_message_caption(chat_id=callback.from_user.id, message_id=callback.message.message_id, caption=f"{chicken_smile[int(user.chickenlvl)-1]} <b>Имя курицы: {user.chickenname}</b>\n\n💰 Баланс: <b>{user.eggs}</b>\n🥚 Яиц в день: <b>{Chicken(level=5, lives=user.chickenhp).get_chicken_info()['daily_eggs']}</b>\n\n📊 Уровень курицы: <b>5</b>\n{fed_smile[user.fed]} Состояние курицы: <b>{user.fed}</b>\n♥️ Кол-во жизней: <b>{user.chickenhp}</b>\n\n⏰ Время кормить: <b>{feed_times}</b>\n\n👥 Кол-во рефов: <b>{user.ref_count}</b>\n🔗 Ваша реферальная ссылка: <code>{link}</code>", 
                                           reply_markup=await kb.menu())
        elif int(user.chickenlvl) < 2 and int(user.ref_count) < 10:
            await callback.answer(f'До повышения уровня вам нужно {10 - int(user.ref_count)} рефералов')
        elif int(user.chickenlvl) < 3 and int(user.chickenlvl) > 1 and int(user.ref_count) < 25:
            await callback.answer(f'До повышения уровня вам нужно {25 - int(user.ref_count)} рефералов')
        elif int(user.chickenlvl) < 4 and int(user.chickenlvl) > 2 and int(user.ref_count) < 45:
            await callback.answer(f'До повышения уровня вам нужно {45 - int(user.ref_count)} рефералов')
        elif int(user.chickenlvl) < 5 and int(user.chickenlvl) > 3 and int(user.ref_count) < 70:
            await callback.answer(f'До повышения уровня вам нужно {70 - int(user.ref_count)} рефералов')

@router.callback_query(F.data=='update')
async def update(callback: CallbackQuery, bot: Bot):
        user_data = await rq.get_user(callback.from_user.id)
        for user in user_data:
            img = await getimgurl()
            link = await create_start_link(bot,str(callback.from_user.id), encode=True)
            photo = img[int(user.chickenlvl)-1]
            await bot.edit_message_media(media=photo, chat_id=callback.from_user.id,
            message_id=callback.message.message_id,)
            feed_time = Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['feed_times']
            feed_times = str(f'{feed_time[0]}, {feed_time[1]}, {feed_time[2]}')
            await bot.edit_message_caption(message_id=callback.message.message_id, chat_id=callback.from_user.id, 
                                 caption=f"{chicken_smile[int(user.chickenlvl)-1]} <b>Имя курицы: {user.chickenname}</b>\n\n💰 Баланс: <b>{user.eggs}</b>\n🥚 Яиц в день: <b>{Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['daily_eggs']}</b>\n\n📊 Уровень курицы: <b>{user.chickenlvl}</b>\n{fed_smile[user.fed]} Состояние курицы: <b>{user.fed}</b>\n♥️ Кол-во жизней: <b>{user.chickenhp}</b>\n\n⏰ Время кормить: <b>{feed_times}</b>\n\n👥 Кол-во рефов: <b>{user.ref_count}</b>\n🔗 Ваша реферальная ссылка: <code>{link}</code>",
                                 reply_markup=await kb.menu())
        
@router.callback_query(F.data=='night')
async def night(callback: CallbackQuery, state: FSMContext, bot: Bot):
    clocklist = str(datetime.now()).split(' ')[1].split(':')
    datelist = str(datetime.now()).split(' ')[0].split('-')
    number = int(datelist[2])
    hour = int(clocklist[0])
    img = await getimg()
    user_data = await rq.get_users()
    count = 0
    for users in user_data:
        count += 1
    user_data = await rq.get_user(callback.from_user.id)
    for user in user_data:
        if hour == 23 and int(user.chickenlvl) >= 3 and number>int(user.last_rob):
            await bot.send_photo(photo=img[9], chat_id=callback.from_user.id, caption='Цена грабежа: <b>10</b> 🥚\n\nВы хотите начать грабёж?', reply_markup=await kb.night())
            await state.update_data(robber_tg_id=callback.from_user.id)
            random_num=random.randint(1, count)
            while True:
                if random_num==user.id:
                    random_num=random.randint(1, count)
                    return True
                else:
                    await state.update_data(user_id=random_num)
                    return False
        elif number>int(user.last_rob) and int(user.last_rob) != 0:
            await callback.answer('Вы уже грабили сегодня.')
        else:
            await callback.message.answer('Судная ночь работает активируется с 23:00 до 00:00 и доступна с 3-го уровня.', reply_markup=await kb.del_msg())

@router.callback_query(F.data=='rob')
async def rob(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user_data = await rq.get_user(callback.from_user.id)
    datelist = str(datetime.now()).split(' ')[0].split('-')
    number = int(datelist[2])
    for user in user_data:
        if int(user.eggs) >= 10:
            await callback.answer('Ищем жертву 🔎')
            user_data = await rq.get_users()
            count = 0
            for users in user_data:
                count += 1
            user_data = await rq.get_user_id(data['user_id'])
            for user in user_data:
                robber_data = await rq.get_user(callback.from_user.id)
                for robber in robber_data:
                    await rq.upd_eggs(robber.tg_id, robber.eggs-10)
                    await rq.upd_last_rob(robber.tg_id, str(number))
                    await rq.upd_now_robbery(robber.tg_id, '1')
                    await callback.message.edit_text(f'Ваша жертва: <b>{user.chickenname}</b>\n\nОграбление будет закончено через 10 минут, если жертва не защитится.', reply_markup=await kb.del_msg())
                    await bot.send_message(chat_id=user.tg_id, text=f'Вас грабит {robber.chickenname}', reply_markup=await kb.defense(callback.from_user.id))
                    await asyncio.sleep(10*60)
                    img = await getimg()
                    robber_data = await rq.get_user(data['robber_tg_id'])
                    for robber in robber_data:
                        if robber.now_robbery == '1':
                            await bot.send_photo(photo=img[5], chat_id=robber.tg_id, caption=f'<b>Успешное ограбление!</b>\n\nЖертва не стала защищаться.\n\nВы получили <b>15 яиц.</b>', reply_markup=await kb.del_msg())
                            await rq.upd_nightuser(robber.tg_id, 1, robber.eggs+15)
                            user_data = await rq.get_user_id(data['user_id'])
                            for user in user_data:
                                if int(user.eggs) < 10:
                                    if int(user.chickenhp) == 2:
                                        await bot.send_photo(photo=img[6],chat_id=user.tg_id, caption=f'<b>Вас ограбили!</b>\n\n♥️ Вы потеряли 1 жизнь.\n🔍 За 30 яиц вы можете узнать, кто вас ограбил.', reply_markup=await kb.to_know(robber.tg_id))
                                        await rq.upd_nightuser(user.tg_id, 2, user.eggs-10)
                                    else:
                                        await bot.send_photo(photo=img[7],chat_id=user.tg_id, caption=f'<b>Вас ограбили!</b>!\n\nВаша курица не пережила ограбление и скончалась.', reply_markup=await kb.del_msg())
                                        if user.invitefrom != 'None':
                                            ref_data = await rq.get_user(user.invitefrom)
                                            for ref in ref_data:
                                                ref_count = int(ref.ref_count)-1
                                                await rq.upd_count(ref.tg_id, ref_count)
                                                await bot.send_message(chat_id=ref.tg_id, text=f'<b>Курица вашего реферала погибла.</b> Теперь у вас <b>{ref_count}</b> рефералов.')
                                elif int(user.eggs) >= 10:
                                    await bot.send_photo(photo=img[6],chat_id=user.tg_id, caption=f'<b>Вас ограбили!</b>\n\n♥️ Вы потеряли 10 яиц.\n🔍 За 30 яиц вы можете узнать, кто вас ограбил.', reply_markup=await kb.to_know(robber.tg_id))
        else:
            await callback.answer('У вас нету 10 яиц для грабежа.')

@router.callback_query(F.data.startswith('def_'))
async def defense(callback: CallbackQuery, bot: Bot):
    await bot.send_message(chat_id=callback.data.split('_')[1], text='<b>Жертва пытается защититься.</b> Если вам выпадет число больше, чем у жертвы вы её ограбите, а иначе <b>вы потерпите поражение.</b>', reply_markup=await kb.del_msg())
    rob_dice = await bot.send_dice(callback.data.split('_')[1])
    rob_dice = rob_dice['dice']['value']
    user_dice = await bot.send_dice(callback.from_user.id)
    user_dice = user_dice['dice']['value']
    user_data = await rq.get_user(callback.from_user.id)
    img = await getimg()
    for user in user_data:
        if int(rob_dice) > int(user_dice):
            rob_data = await rq.get_user(callback.data.split('_')[1])
            for robber in rob_data:
                await bot.send_photo(photo=img[5], chat_id=callback.data.split('_')[1], caption=f'<b>Успешное ограбление!</b>\n\nВам выпало число <b>{rob_dice}</b>, а жертве <b>{user_dice}</b>.\n\nВы получили <b>15</b> яиц.', reply_markup=await kb.del_msg())
                await rq.upd_nightuser(callback.data.split('_')[1], 1, robber.eggs+15)
                if int(user.eggs) < 10:
                    if int(user.chickenhp) == 2:
                        await bot.send_photo(photo=img[6],chat_id=callback.from_user.id, caption=f'<b>Вас ограбили!</b>\n\nВам выпало число <b>{user_dice}</b>, а грабителю <b>{rob_dice}</b>.\n\n♥️ Вы потеряли 1 жизнь.\n🔍 За 30 яиц вы можете узнать, кто вас ограбил.', reply_markup=await kb.to_know(robber.tg_id))
                        await rq.upd_nightuser(callback.from_user.id, 2, user.eggs-10)
                    else:
                        await bot.send_photo(photo=img[7],chat_id=callback.from_user.id, caption=f'Вас ограбили!\n\nВам выпало число <b>{user_dice}</b>, а грабителю <b>{rob_dice}</b>.\n\nВаша курица не пережила ограбление и погибла.', reply_markup=await kb.del_msg())
                        if user.invitefrom != 'None':
                            ref_data = await rq.get_user(user.invitefrom)
                            for ref in ref_data:
                                ref_count = int(ref.ref_count)-1
                                await rq.upd_count(ref.tg_id, ref_count)
                                await bot.send_message(chat_id=ref.tg_id, text=f'<b>Курица вашего реферала погибла.</b> Теперь у вас <b>{ref_count}</b> рефералов.')
                elif int(user.eggs) >= 10:
                    await bot.send_photo(photo=img[6],chat_id=callback.from_user.id, caption=f'<b>Вас ограбили!</b>\n\nВам выпало число <b>{user_dice}</b>, а грабителю <b>{rob_dice}</b>.\n\nВы потеряли 10 яиц.\n🔍 За 30 яиц вы можете узнать, кто вас ограбил.', reply_markup=await kb.to_know(robber.tg_id))
        else:
            await bot.send_photo(photo=img[6], chat_id=callback.data.split('_')[1], caption=f'<b>Ограбление не удалось!</b>\n\nВам выпало число <b>{rob_dice}</b>, а жертве <b>{user_dice}</b>.', reply_markup=await kb.del_msg())
            await bot.send_photo(photo=img[5],chat_id=callback.from_user.id, caption=f'<b>Вы успешно отбились!</b>\n\nВам выпало число{user_dice}, а грабителю <b>{user_dice}</b>.\n\n🔍 За 30 яиц вы можете узнать, кто вас пытался ограбить.', reply_markup=await kb.to_know(robber.tg_id))

@router.callback_query(F.data=='del')
async def delete_msg(callback: CallbackQuery, bot: Bot):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)

@router.callback_query(F.data=='to_main')
async def to_main(callback: CallbackQuery, bot: Bot):
    user_data = await rq.get_user(callback.from_user.id)
    for user in user_data:
        img = await getimg()
        link = await create_start_link(bot,str(callback.from_user.id), encode=True)
        feed_time = Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['feed_times']
        feed_times = str(f'{feed_time[0]}, {feed_time[1]}, {feed_time[2]}')
        await bot.send_photo(photo=img[int(user.chickenlvl)-1], chat_id=callback.from_user.id, 
                                 caption=f"{chicken_smile[int(user.chickenlvl)-1]} <b>Имя курицы: {user.chickenname}</b>\n\n💰 Баланс: <b>{user.eggs}</b>\n🥚 Яиц в день: <b>{Chicken(level=int(user.chickenlvl), lives=user.chickenhp).get_chicken_info()['daily_eggs']}</b>\n\n📊 Уровень курицы: <b>{user.chickenlvl}</b>\n{fed_smile[user.fed]} Состояние курицы: <b>{user.fed}</b>\n♥️ Кол-во жизней: <b>{user.chickenhp}</b>\n\n⏰ Время кормить: <b>{feed_times}</b>\n\n👥 Кол-во рефов: <b>{user.ref_count}</b>\n🔗 Ваша реферальная ссылка: <code>{link}</code>",
                                 reply_markup=await kb.menu())

@router.callback_query(F.data=='withdraw')
async def withdraw(callback: CallbackQuery, state: FSMContext, bot: Bot):
    img = await getimg()
    datelist = str(datetime.now()).split(' ')[0].split('-')
    year = int(datelist[0])
    mon = int(datelist[1])
    num = int(datelist[2])
    if calendar.isleap(year):
        if mon==1 and num==31 or mon==2 and num==29 or mon==3 and num==31 or mon==4 and num==30 or mon==5 and num==31 or mon==6 and num==30 or mon==7 and num==31 or mon==8 and num==31 or mon==9 and num==30 or mon==10 and num==31 or mon==11 and num==30 or mon==12 and num==31:
            user_data=await rq.get_user(callback.from_user.id)
            for user in user_data:
                await bot.send_photo(photo=img[8], chat_id=callback.from_user.id, caption=f'🛍 <b>Магазин робуксов:</b>\n\n<b>1 робукс = 5 яиц</b>\n\n<b>У вас {user.eggs}</b> яиц\nДоступно для вывода<b>{int(math.floor(user.eggs/5)) if user.eggs >=5 else 0}</b>\n\n<b>ПЕРЕД ВЫВОДОМ И ДО ЕГО КОНЦА У ВАС ДОЛЖЕН БЫТЬ ОДИН И ТОТ ЖЕ ЮЗЕРНЕЙМ!!!</b>', reply_markup=await kb.withdraw())
                await state.update_data(amount=int(math.floor(user.eggs/5)))
        else:
            await callback.message.answer('Вывод доступен только в последний день месяца.\n\nКурс <b>5🥚 = 1ROBUX</b>.', reply_markup=await kb.del_msg())
    else:
        if mon==1 and num==31 or mon==2 and num==28 or mon==3 and num==31 or mon==4 and num==30 or mon==5 and num==31 or mon==6 and num==30 or mon==7 and num==31 or mon==8 and num==31 or mon==9 and num==30 or mon==10 and num==31 or mon==11 and num==30 or mon==12 and num==31:
            user_data=await rq.get_user(callback.from_user.id)
            for user in user_data:
                await bot.send_photo(photo=img[8], chat_id=callback.from_user.id, caption=f'🛍 <b>Магазин робуксов:</b>\n\n<b>1 робукс = 5 яиц</b>\n\n<b>У вас {user.eggs}</b> яиц\nДоступно для вывода<b>{int(math.floor(user.eggs/5)) if user.eggs >=5 else 0}</b>\n\n<b>ПЕРЕД ВЫВОДОМ И ДО ЕГО КОНЦА У ВАС ДОЛЖЕН БЫТЬ ОДИН И ТОТ ЖЕ ЮЗЕРНЕЙМ!!!</b>', reply_markup=await kb.withdraw())
                await state.update_data(amount=int(math.floor(user.eggs/5)))
        else:
            await callback.message.answer('Вывод доступен только в последний день месяца.\n\nКурс <b>5🥚 = 1ROBUX</b>.', reply_markup=await kb.del_msg())

@router.callback_query(F.data=='withdraw_all')
async def withdraw_all(callback: CallbackQuery, state: FSMContext, bot: Bot):
    datelist = str(datetime.now()).split(' ')[0].split('-')
    year = int(datelist[0])
    mon = int(datelist[1])
    num = int(datelist[2])
    if calendar.isleap(year):
        if mon==1 and num==31 or mon==2 and num==29 or mon==3 and num==31 or mon==4 and num==30 or mon==5 and num==31 or mon==6 and num==30 or mon==7 and num==31 or mon==8 and num==31 or mon==9 and num==30 or mon==10 and num==31 or mon==11 and num==30 or mon==12 and num==31:
            user_data=await rq.get_user(callback.from_user.id)
            for user in user_data:
                if user.eggs >= 5:
                    await callback.message.answer('<b>Введите ваш ник в роблоксе:</b>')
                    await state.set_state(get.roblox_name)
                else:
                    await callback.answer('Недостаточно яиц для минимального вывода')
    else:
        if mon==1 and num==31 or mon==2 and num==28 or mon==3 and num==31 or mon==4 and num==30 or mon==5 and num==31 or mon==6 and num==30 or mon==7 and num==31 or mon==8 and num==31 or mon==9 and num==30 or mon==10 and num==31 or mon==11 and num==30 or mon==12 and num==31:
            user_data=await rq.get_user(callback.from_user.id)
            for user in user_data:
                if user.eggs >= 5:
                    await callback.message.answer('<b>Введите ваш ник в роблоксе:</b>')
                    await state.set_state(get.roblox_name)
                else:
                    await callback.answer('Недостаточно яиц для минимального вывода')
                
@router.message(get.roblox_name)
async def create_req(message: Message, state: FSMContext):
    await rq.create_req(message.from_user.id, message.from_user.username, message.text)
    await message.answer('Ваша заявка отправлена администрации. В течении 24 часов вам выплатят робуксы.', 
                         reply_markup=await kb.to_main())
    await state.clear()

@router.callback_query(F.data=='answer')
async def answer(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('<b>Введите сообщение для администрации:</b>', 
                                     reply_markup=await kb.del_msg())
    await state.set_state(get.user_message)
    
@router.message(get.user_message)
async def user_message(message: Message, state: FSMContext, bot: Bot):
    await message.answer('<b>Сообщение отправлено Администрации.</b>', reply_markup=await kb.del_msg())
    req_data = await rq.get_req_tgid(message.from_user.id)
    for req in req_data:
        for admin in admins_list:
            await bot.send_message(chat_id=admin, text=f'Сообщение от {req.username}(tgid:{req.tg_id})\n\n{message.text}', 
                                   reply_markup=await kb.answer_admin(message.from_user.id, req.id))
    await state.clear()


#apanel

@router.message(Command('apanel'), IsAdmin(admins_list))
async def apanel(message: Message):
    await message.answer('Вы зашли в Админ-панель', reply_markup=await kb.apanel())

@router.callback_query(F.data=='amain', IsAdmin2(admins_list))
async def amain(callback: CallbackQuery):
    await callback.message.edit_text('Вы зашли в Админ-панель', reply_markup=await kb.apanel())
    
@router.callback_query(F.data=='create_mail', IsAdmin2(admins_list))
async def create_mail(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите текст для рассылки:', reply_markup=await kb.backtoapanel())
    await state.set_state(get.mail)
    
@router.message(get.mail, IsAdmin(admins_list))
async def mailq(message: Message, state: FSMContext):
    await state.update_data(mail=message.text)
    await message.answer(f'Вы точно хотите создать рассылку?\n\nТекст для рассылки:\n{message.text}', reply_markup=await kb.createmail())


@router.callback_query(F.data=='createmailall', IsAdmin2(admins_list))
async def createmailall(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    users_data = await rq.get_users()
    await callback.message.edit_text('Вам придёт оповещение когда рассылка закончится.', reply_markup=await kb.backtoapanel())
    count_a = 0
    count_b = 0
    for user in users_data:
        try:
            await bot.send_message(chat_id=user.tg_id, text=data['mail'])
            count_a += 1
        except:
            count_b += 1
    await callback.message.answer(f'Рассылка была закончена.\n\nУспешные: {count_a}\nНеудачные: {count_b}')
    await state.clear()

@router.callback_query(F.data.startswith('selectuser_'), IsAdmin2(admins_list))
async def selectuser(callback: CallbackQuery):
    user_data = await rq.get_user(callback.data.split('_')[1])
    for user in user_data:
        await callback.message.edit_text(f'TG_ID: {user.tg_id}\n\nНик курицы: {user.chickenname}\nЖизней: {user.chickenhp}\nУровень: {user.chickenlvl}\nСостояние: {user.fed}\nЯиц: {user.eggs}\n\nПригласил: {user.invitefrom if user.invitefrom !='None'else 'Никто не приглашал'}\nКол-во рефов: {user.ref_count}\n\nГрабит в данный момент?: {'Да' if user.now_robbery != '0' else 'Нет'}\nПоследний раз грабил: {user.last_rob} числа', reply_markup=await kb.selectuser(user.tg_id))

@router.callback_query(F.data.startswith('edit_'), IsAdmin2(admins_list))
async def edit(callback: CallbackQuery, state: FSMContext):
    await state.update_data(upd_id=callback.data.split('_')[2])
    if callback.data.split('_')[1] == 'name':
        await callback.message.edit_text('Введите новое имя курицы:', reply_markup=await kb.editback(callback.data.split('_')[2]))
        await state.set_state(get.name) 
    elif callback.data.split('_')[1] == 'hp':
        await callback.message.edit_text('Введите новое количество жизней или можете выбрать из предложенных:', reply_markup=await kb.edithp(callback.data.split('_')[2]))
        await state.set_state(get.hp)
    elif callback.data.split('_')[1] == 'fed':
        await callback.message.edit_text('Выберите новое состояние курицы:', reply_markup=await kb.editfed(callback.data.split('_')[2]))
        await state.set_state(get.fed)
    elif callback.data.split('_')[1] == 'eggs':
        await callback.message.edit_text('Введите новое количество яиц:', reply_markup=await kb.editback(callback.data.split('_')[2]))
        await state.set_state(get.eggs)
    elif callback.data.split('_')[1] == 'refs':
        await callback.message.edit_text('Введите новое количество рефералов:', reply_markup=await kb.editback(callback.data.split('_')[2]))
        await state.set_state(get.ref_count)
    elif callback.data.split('_')[1] == 'lvl':
        await callback.message.edit_text('Выберите новый уровень:', reply_markup=await kb.editlvl(callback.data.split('_')[2]))
        await state.set_state(get.lvl)

@router.callback_query(F.data.startswith('choiseedit'), IsAdmin2(admins_list))
async def choice(callback: CallbackQuery, state: FSMContext):
    if callback.data.split('_')[1] == 'hp':
        await callback.message.edit_text('Вы успешно поменяли количество жизней', reply_markup=await kb.editback(callback.data.split('_')[2]))
        await rq.upd_hp(callback.data.split('_')[2], 
                        callback.data.split('_')[3])
        await state.clear()
    elif callback.data.split('_')[1] == 'fed':
        await callback.message.edit_text('Вы успешно поменяли состояние курицы', reply_markup=await kb.editback(callback.data.split('_')[2]))
        await rq.upd_fed(callback.data.split('_')[2], 
                        callback.data.split('_')[3])
        await state.clear()
    elif callback.data.split('_')[1] == 'lvl':
        await callback.message.edit_text('Вы успешно поменяли уровень курицы', reply_markup=await kb.editback(callback.data.split('_')[2]))
        await rq.upd_lvl(callback.data.split('_')[2],
                        callback.data.split('_')[3])
        await state.clear()

@router.message(get.eggs, IsAdmin(admins_list))
async def edit_eggs(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        await rq.upd_eggs(data['upd_id'], int(message.text))
        await message.answer('Вы успешно поменяи количество яиц.', reply_markup=await kb.editback(data['upd_id']))
    except:
        await message.answer('Поменять количество яиц не удалось', reply_markup=await kb.editback(data['upd_id']))
        
@router.message(get.ref_count, IsAdmin(admins_list))
async def edit_refs(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        await rq.upd_count(data['upd_id'], message.text)
        await message.answer('Вы успешно поменяи количество рефов.', reply_markup=await kb.editback(data['upd_id']))
    except:
        await message.answer('Поменять количество рефов не удалось', reply_markup=await kb.editback(data['upd_id']))
        
@router.message(get.hp, IsAdmin(admins_list))
async def edit_hp(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        await rq.upd_hp(data['upd_id'], message.text)
        await message.answer('Вы успешно поменяи количество жизней.', reply_markup=await kb.editback(data['upd_id']))
    except:
        await message.answer('Поменять количество жизней не удалось', reply_markup=await kb.editback(data['upd_id']))
        
@router.message(get.name, IsAdmin(admins_list))
async def edit_name(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        await rq.upd_name(data['upd_id'], message.text)
        await message.answer('Вы успешно поменяи имя курицы.', reply_markup=await kb.editback(data['upd_id']))
    except:
        await message.answer('Поменять имя курицы не удалось', reply_markup=await kb.editback(data['upd_id']))

@router.callback_query(F.data=='search', IsAdmin2(admins_list))
async def search(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите telegram id пользователя:', reply_markup=await kb.backtousers())
    await state.set_state(get.tg_id)
    
@router.message(get.tg_id, IsAdmin(admins_list))
async def get_search(message: Message, state: FSMContext):
    try:
        user_data = await rq.get_user(message.text)
        for user in user_data:
            await message.answer(f'TG_ID: {user.tg_id}\n\nНик курицы: {user.chickenname}\nЖизней: {user.chickenhp}\nУровень: {user.chickenlvl}\nСостояние: {user.fed}\nЯиц: {user.eggs}\n\nПригласил: {user.invitefrom if user.invitefrom !='None'else 'Никто не приглашал'}\nКол-во рефов: {user.ref_count}\n\nГрабит в данный момент?: {'Да' if user.now_robbery != '0' else 'Нет'}\nПоследний раз грабил: {user.last_rob} числа', reply_markup=await kb.selectuser(user.tg_id))
    except:
        await message.answer('Такого пользователя нету')

@router.callback_query(F.data=='check_all_users', IsAdmin2(admins_list))
async def check_all_users(callback: CallbackQuery):
    await callback.message.edit_text('Все пользователи [tg_id | имя курицы]:', 
                                     reply_markup=await kb.check_all_users(0))

@router.callback_query(F.data=='check_all_req', IsAdmin2(admins_list))
async def check_all_req(callback: CallbackQuery):
    await callback.message.edit_text('Все заявки на вывод [username | робуксы]:', 
                                     reply_markup=await kb.all_req(0))
    
@router.callback_query(F.data.startswith('pagereq_'), IsAdmin2(admins_list))
async def pagereq(callback: CallbackQuery):
    await callback.message.edit_text('Все заявки на вывод [username | робуксы]:', 
                                     reply_markup=await kb.all_req(callback.data.split('_')[1]))
    
@router.callback_query(F.data.startswith('page_'), IsAdmin2(admins_list))
async def pageusers(callback: CallbackQuery):
    await callback.message.edit_text('Все пользователи [tg_id | имя курицы]:', 
                                     reply_markup=await kb.check_all_users(callback.data.split('_')[1]))

@router.callback_query(F.data.startswith('checkreq_'), IsAdmin2(admins_list))
async def checkreq(callback: CallbackQuery, state: FSMContext, bot: Bot):
    req_data = await rq.get_req(callback.data.split('_')[1])
    for req in req_data:
        await callback.message.edit_text(f'Заявка от {req.username} (tgid: {req.tg_id})\n\nВыводит {req.amount}\n\nНик в роблоксе: {req.roblox_name}', 
                                         reply_markup=await kb.check_req(req.tg_id, req.id))

@router.callback_query(F.data.startswith('paid_'), IsAdmin2(admins_list))
async def paid(callback: CallbackQuery, state: FSMContext, bot: Bot):
    req_data = await rq.get_req(callback.data.split('_')[1])
    for req in req_data:
        await bot.send_message(chat_id=req.tg_id, text='Робуксы были выплачены.', reply_markup=await kb.del_msg())
    await rq.del_req(callback.data.split('_')[1])
    await callback.message.edit_text('Пользователю было отправлено оповещение.', reply_markup=await kb.paid())

@router.callback_query(F.data.startswith('sendmsg_'), IsAdmin2(admins_list))
async def sendmsg(callback: CallbackQuery, state: FSMContext):
    await state.update_data(to_id=callback.data.split('_')[2])
    await callback.message.edit_text('Введите сообщение, которое будет отправлено пользователю:', 
                                     reply_markup=await kb.sendmsg(callback.data.split('_')[1]))
    await state.update_data(req_id=callback.data.split('_')[1])
    await state.set_state(get.message)
    
@router.callback_query(F.data.startswith('sendmsg2_'), IsAdmin2(admins_list))
async def sendmsg2(callback: CallbackQuery, state: FSMContext):
    await state.update_data(to_id=callback.data.split('_')[2])
    await callback.message.edit_text('Введите сообщение, которое будет отправлено пользователю:', 
                                     reply_markup=await kb.sendmsg2(callback.data.split('_')[2]))
    await state.set_state(get.message)

@router.message(get.message, IsAdmin(admins_list))
async def send_msg(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await bot.send_message(chat_id=data['to_id'], text=f'Сообщение от администрации проекта:\n\n{message.text}', 
                           reply_markup=await kb.answer())
    await message.answer('Сообщение было отправлено.', 
                         reply_markup=await kb.sendmsg(data['req_id']))
    await state.clear()
    
@router.message(get.message2, IsAdmin(admins_list))
async def send_msg2(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await bot.send_message(chat_id=data['to_id'], text=f'Сообщение от администрации проекта:\n\n{message.text}', 
                           reply_markup=await kb.answer())
    await message.answer('Сообщение было отправлено.', 
                         reply_markup=await kb.sendmsg2(data['to_id']))
    await state.clear()

@router.callback_query(F.data=='check_all_users', IsAdmin2(admins_list))
async def check_all_users(callback: CallbackQuery):
    await callback.message.edit_text('Все пользователи бота [username | робуксы]:', 
                                     reply_markup=await kb.all_req())


