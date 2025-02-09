from aiogram.types import InlineKeyboardButton
import database.requests as rq
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def menu():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="🌾 Кормить", callback_data="fed"))
    kb.add(InlineKeyboardButton(text="🌙 Судная ночь", callback_data="night"))
    row.append(2)
    kb.add(InlineKeyboardButton(text="🏆 Топ игроков", callback_data="top"))
    kb.add(InlineKeyboardButton(text="📤 Вывести робуксы", callback_data="withdraw"))
    row.append(2)
    kb.add(InlineKeyboardButton(text="🔺 Повысить уровень", callback_data="up_lvl"))
    kb.add(InlineKeyboardButton(text="🔄 Обновить", callback_data="update"))
    return kb.adjust(*row).as_markup()

async def linkgroup():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="🔗 Перейти", url="https://www.roblox.com/communities/34056135/Nakamaki-There"))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def getgoldegg():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="📥 Забрать", callback_data=f'getgoldegg'))
    kb.add(InlineKeyboardButton(text="❌ Закрыть", callback_data=f'del'))
    row.append(1)
    return kb.adjust(*row).as_markup()


async def night():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="🦹‍♂️ Начать грабёж", callback_data='rob'))
    kb.add(InlineKeyboardButton(text="« Назад", callback_data='to_main'))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def defense(robber_id):
    kb = InlineKeyboardBuilder()
    row = []
    #robber_id нужен для того чтобы бросить кубик и легко достать айди грабителя
    kb.add(InlineKeyboardButton(text="🛡 Защититься", callback_data=f'def_{robber_id}'))
    kb.add(InlineKeyboardButton(text="❌ Закрыть", callback_data='del'))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def to_know(robber_tg_id):
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="🔍 Узнать", callback_data=f'toknow_{robber_tg_id}'))
    kb.add(InlineKeyboardButton(text="❌ Закрыть", callback_data='del'))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def del_msg():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="❌ Закрыть", callback_data='del'))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def to_main():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="🏠 В меню", callback_data='to_main'))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def withdraw():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="📤 Вывести", callback_data='withdraw_all'))
    kb.add(InlineKeyboardButton(text="« Назад", callback_data='to_main'))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def apanel():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="Посмотреть заявки на вывод", callback_data='check_all_req'))
    kb.add(InlineKeyboardButton(text="Управление пользователями", callback_data='check_all_users'))
    kb.add(InlineKeyboardButton(text="Сделать рассылку", callback_data='create_mail'))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def backtousers():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="« Назад", callback_data='check_all_users'))
    row.append(1)
    return kb.adjust(*row).as_markup()


async def all_req(page):
    kb = InlineKeyboardBuilder()
    count = []
    for i in await rq.get_users(): count.append(1)
    ITEMS_PER_PAGE = 10
    total_pages = (len(count) - 1) // ITEMS_PER_PAGE + 1
    start_idx = int(int(page) * ITEMS_PER_PAGE)
    end_idx = int(start_idx) + ITEMS_PER_PAGE
    users_data = await rq.get_users()
    req_data = await rq.get_reqs()
    for req in req_data:
        kb.add(InlineKeyboardButton(text=f"{req.username} | {req.amount}", callback_data=f'checkreq_{req.id}'))
    nav_buttons = []
    if int(page) > 0:
        nav_buttons.append(InlineKeyboardButton(text="⏪ Назад", callback_data=f"pagereq_{int(page)-1}"))
    if int(page) < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(text="Вперед ⏩", callback_data=f"pagereq_{int(page)+1}"))
    for nav in nav_buttons:
        kb.add(nav)
    kb.add(InlineKeyboardButton(text="Назад в Админ-панель", callback_data='amain'))
    return kb.adjust(1).as_markup()

async def check_req(tg_id, req_id):
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="Выплачено", callback_data=f'paid_{req_id}'))
    kb.add(InlineKeyboardButton(text="Отправить сообщение", callback_data=f'sendmsg_{req_id}_{tg_id}'))
    kb.add(InlineKeyboardButton(text="« Назад", callback_data='check_all_req'))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def paid():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="Вернуться к заявкам", callback_data=f'check_all_req'))
    kb.add(InlineKeyboardButton(text="Перейти в Админ-панель", callback_data=f'amain'))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def backtoapanel():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="« Назад в Админ-панель", callback_data=f'amain'))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def createmail():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="Создать", callback_data=f'createmailall'))
    kb.add(InlineKeyboardButton(text="« Назад", callback_data=f'amain'))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def sendmsg(id):
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="Вернуться к заявке", callback_data=f'checkreq_{id}'))
    kb.add(InlineKeyboardButton(text="Посмотреть все заявки", callback_data=f'check_all_req'))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def sendmsg2(id):
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="« Назад", callback_data=f'selectuser_{id}'))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def answer():
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="Ответить", callback_data=f'answer'))
    kb.add(InlineKeyboardButton(text="❌ Закрыть", callback_data=f'del'))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def answer_admin(tg_id, req_id):
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="Ответить", callback_data=f'sendmsg_{req_id}_{tg_id}'))
    kb.add(InlineKeyboardButton(text="❌ Закрыть", callback_data='del'))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def check_all_users(page):
    kb = InlineKeyboardBuilder()
    count = []
    for i in await rq.get_users(): count.append(1)
    ITEMS_PER_PAGE = 10
    total_pages = (len(count) - 1) // ITEMS_PER_PAGE + 1
    start_idx = int(int(page) * ITEMS_PER_PAGE)
    end_idx = int(start_idx) + ITEMS_PER_PAGE
    users_data = await rq.get_users()
    kb.add(InlineKeyboardButton(text="Найти по tg_id", callback_data='search'))
    for user in users_data:
        kb.add(InlineKeyboardButton(text=f"{user.tg_id} | {user.chickenname}", callback_data=f'selectuser_{user.tg_id}')) if user.id>=start_idx and user.id<=end_idx else None
    nav_buttons = []
    if int(page) > 0:
        nav_buttons.append(InlineKeyboardButton(text="⏪ Назад", callback_data=f"page_{int(page)-1}"))
    if int(page) < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(text="Вперед ⏩", callback_data=f"page_{int(page)+1}"))
    for nav in nav_buttons:
        kb.add(nav)
    kb.add(InlineKeyboardButton(text="Назад в Админ-панель", callback_data='amain'))
    return kb.adjust(1).as_markup()

async def selectuser(tg_id):
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="Изменить имя", callback_data=f'edit_name_{tg_id}'))
    kb.add(InlineKeyboardButton(text="Изменить хп", callback_data=f'edit_hp_{tg_id}'))
    row.append(2)
    kb.add(InlineKeyboardButton(text="Изменить состояние", callback_data=f'edit_fed_{tg_id}'))
    kb.add(InlineKeyboardButton(text="Изменить яйца", callback_data=f'edit_eggs_{tg_id}'))
    row.append(2)
    kb.add(InlineKeyboardButton(text="Изменить рефералов", callback_data=f'edit_refs_{tg_id}'))
    kb.add(InlineKeyboardButton(text="Изменить уровень", callback_data=f'edit_lvl_{tg_id}'))
    row.append(2)
    kb.add(InlineKeyboardButton(text="Написать сообщение", callback_data=f'sendmsg2_{tg_id}'))
    row.append(1)
    kb.add(InlineKeyboardButton(text="« Назад", callback_data=f'check_all_users'))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def edithp(tg_id):
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="2", callback_data=f'choiseedit_hp_{tg_id}_2'))
    kb.add(InlineKeyboardButton(text="1", callback_data=f'choiseedit_hp_{tg_id}_1'))
    kb.add(InlineKeyboardButton(text="0", callback_data=f'choiseedit_hp_{tg_id}_0'))
    kb.add(InlineKeyboardButton(text="Назад", callback_data=f'selectuser_{tg_id}'))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def editfed(tg_id):
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="Голодная", callback_data=f'choiseedit_fed_{tg_id}_Голодная'))
    kb.add(InlineKeyboardButton(text="Сытая", callback_data=f'choiseedit_fed_{tg_id}_Сытая'))
    kb.add(InlineKeyboardButton(text="Мёртвая", callback_data=f'choiseedit_fed_{tg_id}_Мёртвая'))
    kb.add(InlineKeyboardButton(text="Назад", callback_data=f'selectuser_{tg_id}'))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def editback(tg_id):
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="Назад", callback_data=f'selectuser_{tg_id}'))
    row.append(1)
    return kb.adjust(*row).as_markup()

async def editlvl(tg_id):
    kb = InlineKeyboardBuilder()
    row = []
    kb.add(InlineKeyboardButton(text="5", callback_data=f'choiseedit_lvl_{tg_id}_5'))
    kb.add(InlineKeyboardButton(text="4", callback_data=f'choiseedit_lvl_{tg_id}_4'))
    kb.add(InlineKeyboardButton(text="3", callback_data=f'choiseedit_lvl_{tg_id}_3'))
    kb.add(InlineKeyboardButton(text="2", callback_data=f'choiseedit_lvl_{tg_id}_2'))
    kb.add(InlineKeyboardButton(text="1", callback_data=f'choiseedit_lvl_{tg_id}_1'))
    kb.add(InlineKeyboardButton(text="Назад", callback_data=f'selectuser_{tg_id}'))
    row.append(1)
    return kb.adjust(*row).as_markup()

