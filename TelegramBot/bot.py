import time
import datetime
import logging
from aiogram import Bot, Dispatcher, executor, types
import asyncio
import gspread
import config
from database import user_database

#Инициализация бота
bot = Bot(token = config.TOKEN)
dp = Dispatcher(bot = bot)

#Подключение к Goggle Sheets
gc = gspread.service_account(filename=config.JSON)

#Инициализация соединения с БД
db = user_database('user_database.db')

#Старт бота, запись данных о пользователе
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    user_nickname = message.from_user.username
    logging.info(f'{user_id=} {user_full_name=}', time.asctime())
    print(user_id, user_full_name)

    if(not db.user_exists(message.from_user.id)):
        #Если юзера нет в БД добавляем его
        db.user_add(user_id, user_nickname, user_full_name)

#Запись в теркинг
@dp.message_handler(commands=['writed'])
async def record_write(message:types.Message):
    user_nickname = message.from_user.username
    text = message.text
    sh = gc.open_by_key(config.GOOGLESHEET_ID)
    sh.sheet1.append_row([user_nickname, text])


#Создание поста
@dp.message_handler(commands=['post'])
async def post_creat(message: types.Message):
    users = db.get_users()
    text = message.text
    text_split = text.split(' ')[1]
    for i in users:
        await bot.send_message(i[1], text_split)

#Рассылка
@dp.message_handler(commands=['loop'])
async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        now = time.asctime()
        await bot.send_message(5337835219, f'{now}', disable_notification=True)
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(10*60))
    executor.start_polling(dp)
    

