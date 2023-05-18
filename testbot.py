import asyncio
import logging
import re
from aiogram import Dispatcher, types, executor
from token_bot import bot
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
#from aiogram.fsm.context import FSMContext

import requests
import aiohttp

logging.basicConfig(level=logging.INFO)
memstore=MemoryStorage()
dp=Dispatcher(bot, storage=memstore)

class Form(StatesGroup):
	first_name=State()
	last_name=State()
	phone_name=State()
	access_to_courses=State()
 
@dp.message_handler(commands=['start'],state=None)
async def start(message:types.Message):
	await bot.send_message(message.chat.id,"bot work!")
	keyboard=types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
	create_user=types.KeyboardButton(text='Создать пользователя')
	keyboard.add(create_user)
	await bot.send_message(message.chat.id,"Для того чтобы создать воспользуйтесь клавиатурой ниже", reply_markup=keyboard)

@dp.message_handler(text=['Создать пользователя'], state=None)
async def asd(message: types.Message):
	await bot.send_message(message.chat.id, "Введите ваше имя")
	await Form.first_name.set()
	
@dp.message_handler(state=Form.first_name)
async def set_fname(message: types.Message, state:FSMContext):
	async with state.proxy() as proxy:
		proxy['first_name']= message.text
		await Form.last_name.set()
	await bot.send_message(message.chat.id, "Введите вашу фамилию")

@dp.message_handler(state=Form.last_name)
async def set_lname(message:types.Message, state:FSMContext):
	async with state.proxy() as proxy:
		proxy['last_name']=message.text
		await Form.phone_name.set()
	await bot.send_message(message.chat.id,"Введите ваш номер телефона")

	
@dp.message_handler(state=Form.phone_name)
async def phone_name(message:types.Message, state:FSMContext):
	async with state.proxy() as proxy:
		proxy['phone_name']=message.text
		pattern = result = re.findall(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', message.text)
		print(bool(pattern))
		s=await state.get_data()

	if pattern:
		s=await state.get_data()
		await bot.send_message(message.chat.id,"Пользователь успешно создан!✅\n"f'Ваши данные: {s.get("first_name")} {s.get("last_name")} {s.get("phone_name")}')
		await Form.access_to_courses.set()
		await send_data(s.get("first_name"),  s.get("last_name"), s.get("phone_name"))
	else:
		await bot.send_message(message.chat.id,"Введен некорректный номер.❌\nВведите корректный номер.👇")
		await Form.phone_name.set()


@dp.message_handler(state=Form.access_to_courses)
async def access_to_courses(message:types.Message, state:FSMContext):
	async with state.proxy() as proxy:
		await state.finish()
		keyboardKurs=types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
		buttonkurs=types.KeyboardButton(text="Курсы📚")
		keyboardKurs.add(buttonkurs)
		await bot.send_message(message.chat.id,"Выберете доступный курс",reply_markup=keyboardKurs)
 
# def send_data(first_name: str, last_name: str, phone_number: str):
#     """Send data to django server"""
#     payload = {
# 		'first_name': first_name,
# 		'last_name': last_name,
# 		'phone_number': phone_number,
# 	}
#     print(payload)
#     requests.post(f"http://127.0.0.1:8000/getUser", data=payload)

async def send_data(first_name: str, last_name: str, phone_name: str):
    """Send data to django server"""
    payload = {
		'first_name': first_name,
		'last_name': last_name,
		'phone_number': phone_name,
	}
    print(payload)
    async with aiohttp.ClientSession() as session:
        # await sess.post(f"https://api.telegram.org/bot{TOKEN}/getUser")
        async with session.post('http://localhost:8000/getUser', data=payload) as response:
            print("Status:", response.status)

	
    

async def main():
	await dp.start_polling(bot)

if __name__=="__main__":
	asyncio.run(main())
