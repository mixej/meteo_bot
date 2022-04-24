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

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ["температура", "влажность", "давление"]
keyboard.add(*buttons)




def start_bot():
# функция запуска бота телеграмм

	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	executor.start_polling(dispb)
		
		
@dispb.message_handler(commands="start")		
async def cmd_start(message: types.Message):
	await message.answer("Привет! какие показания тебя интересуют?", reply_markup=keyboard)

@dispb.message_handler(Text(equals="температура")) # температура
async def get_parametrs(message: types.Message):
	sensor = Sensor()
	if sensor.temp < min(str(NORM_TEMP)):
		await message.answer("{0} Температура в комнате, {1:.1f}С\r\nтемпература ниже нормы".format(sensor.time, sensor.temp))
	elif sensor.temp > max(str(NORM_TEMP)):
		await message.answer("{0} Температура в комнате, {1:.1f}С\r\nтемпература выше нормы".format(sensor.time, sensor.temp))
	else:
		await message.answer("{0} Температура в комнате, {1:.1f}С\r\nтемпература в норме".format(sensor.time, sensor.temp))
	
@dispb.message_handler(Text(equals="влажность")) # влажность
async def get_parametrs(message: types.Message):
	sensor = Sensor()
	await message.answer("{0} Влажность в комнате, {1:.1f}%".format(sensor.time, sensor.hum))
	
@dispb.message_handler(Text(equals="давление")) # давление атмосферное
async def get_parametrs(message: types.Message):
	sensor = Sensor()
	await message.answer("{0} Давление, {1:.1f} мм рт.ст".format(sensor.time, sensor.press))	


