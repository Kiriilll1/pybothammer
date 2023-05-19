import asyncio
import logging
import re
from aiogram import Dispatcher, types, executor
import aiohttp
from token_bot import bot
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from settings import HOST

logging.basicConfig(level=logging.INFO)
memstore=MemoryStorage()
dp=Dispatcher(bot, storage=memstore)

class Form(StatesGroup):
    access_to_courses=State()
    courses=State()
    MyProfile=State()
    Feedback=State()

# @dp.message_handler(commands=['start'])
# async def start(message:types.Message, state:FSMContext):
# 	print(message.chat.id)
# 	await message.answer("Cоздать пользователя",
#     reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="create",web_app=WebAppInfo(url=f"https://exquisite-klepon-261123.netlify.app/{message.chat.id}"))))
	
	#await Form.Feedback.set()
	#await Form.access_to_courses.set()


async def send_data(chatID: int):
    """Send data to django server"""
    payload = {
		'chatID': chatID		
	}
    print(payload)
    async with aiohttp.ClientSession() as session:
        async with session.post(f'http://{HOST}/user/getUserId', data=payload) as response:
            print("Status:", response.status)
	

@dp.message_handler(commands=['start'])
async def MyProfile(message:types.Message,state:FSMContext):
	print(message.chat.id)
	button=types.KeyboardButton(text="Мой профиль👤")
	buttonKurs=types.KeyboardButton(text="Тесты📚")
	# buttonFeed=types.KeyboardButton(text="Обратная связь📞")
	keyboardProfile=types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
	keyboardProfile.add(button,buttonKurs)
	await message.answer("👇👇",reply_markup=keyboardProfile)	
	await message.answer("Cоздать пользователя",reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="Создать",web_app=WebAppInfo(url=f"https://exquisite-klepon-261123.netlify.app/{message.chat.id}"))))
	
	
	

@dp.message_handler(text=['Мой профиль👤'])
async def Kurs(message:types.Message):
	await message.answer("Профиль",
	reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="Профиль",web_app=WebAppInfo(url=f"https://exquisite-klepon-261123.netlify.app/{message.chat.id}/course"))))

@dp.message_handler(text=['Обратная связь📞'],)
async def feedback(message:types.Message,state:FSMContext):
	await bot.send_message(message.chat.id,"Не работает, только через веб-вью")
	# printb = await bot.send_message(message.chat.id, "Введите ваше сообщение")
	# print(printb)
    # global userfeedback
	# print(dir(message))
	# print(message)
	# print(type(message))
	# keyboardFeedback=types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
	# button=types.KeyboardButton(text='Подтвердить✅')
	# keyboardFeedback.add(button)
	# await bot.send_message(message.chat.id,"После ввода вашего сообщения нажмите кнопку 'Подтвердить✅'",reply_markup=keyboardFeedback)
	#await Form.Feedback.set()

@dp.message_handler(state=Form.Feedback,text=['Подтвердить✅'])
async def sendfeedback(message:types.Message,state:FSMContext):
	await bot.send_message(message.chat.id,'Готово, ваш отзыв отправлен!')
	#print(userfeedback)
	#await Form.MyProfile.set()
	

@dp.message_handler(text=['Тесты📚'],state=None)
async def Kurs(message:types.Message):
	await message.answer("Тесты",
    reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="Тесты",web_app=WebAppInfo(url=f"https://idyllic-valkyrie-eedcf6.netlify.app/{message.chat.id}"))))



async def main():
	await dp.start_polling(bot)

if __name__=="__main__":
	asyncio.run(main())