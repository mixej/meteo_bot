import asyncio
import requests
import time

from logwriter import LogWriter
from bot_config import TOKEN
from aiogram.dispatcher.filters import Text
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from sensor import Sensor
from config import NORM_TEMP, NORM_HUM, NORM_PRESS

bot = Bot(token=TOKEN)
dispb = Dispatcher(bot)

# создание кнопок
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ["температура", "влажность", "давление"]
buttons_2 = ["сервис"]
keyboard.add(*buttons).add(buttons_2)
#markup5 = ReplyKeyboardMarkup().row(button1, button2, button3).add(KeyboardButton('Средний ряд'))



def start_bot():
# функция запуска бота телеграмм

	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	executor.start_polling(dispb)
		
		
@dispb.message_handler(commands="start")		
async def cmd_start(message: types.Message):
	await message.answer("Привет! какие показания тебя интересуют?", reply_markup=keyboard )

@dispb.message_handler(Text(equals="температура")) # температура
async def get_parametrs(message: types.Message):
	sensor = Sensor()
	if sensor.temp < min(NORM_TEMP):
		await message.answer("{0} Температура в комнате, {1:.1f}С\r\nтемпература ниже нормы".format(sensor.time, sensor.temp))
	elif sensor.temp > max(NORM_TEMP):
		await message.answer("{0} Температура в комнате, {1:.1f}С\r\nтемпература выше нормы".format(sensor.time, sensor.temp))
	else:
		await message.answer("{0} Температура в комнате, {1:.1f}С\r\nтемпература в норме".format(sensor.time, sensor.temp))
	
@dispb.message_handler(Text(equals="влажность")) # влажность
async def get_parametrs(message: types.Message):
	sensor = Sensor()
	if sensor.hum < min(NORM_HUM):
		await message.answer("{0} Влажность в комнате, {1:.1f}%\r\nвлажность ниже нормы".format(sensor.time, sensor.hum))
	elif sensor.hum > max(NORM_HUM):
		await message.answer("{0} Влажность в комнате, {1:.1f}%\r\nвлажность выше нормы".format(sensor.time, sensor.hum))
	else:
		await message.answer("{0} Влажность в комнате, {1:.1f}%\r\nвлажность в норме".format(sensor.time, sensor.hum))
	
@dispb.message_handler(Text(equals="давление")) # давление атмосферное
async def get_parametrs(message: types.Message):
	sensor = Sensor()
	if sensor.press < min(NORM_PRESS):
		await message.answer("{0} Давление, {1:.1f} мм рт.ст\r\nдавление ниже нормы".format(sensor.time, sensor.press))
	elif sensor.press > max(NORM_PRESS):
		await message.answer("{0} Давление, {1:.1f} мм рт.ст\r\nдавление выше нормы".format(sensor.time, sensor.press))
	else:
		await message.answer("{0} Давление, {1:.1f} мм рт.ст\r\nдавление в норме".format(sensor.time, sensor.press))	


