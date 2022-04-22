import asyncio
import requests
import threading

import time

from logwriter import LogWriter
from config import TOKEN
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from sensor import Sensor

bot = Bot(token=TOKEN)
dispb = Dispatcher(bot)



def start_bot():
# функция запуска бота телеграмм

	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	executor.start_polling(dispb)
		
		
@dispb.message_handler(commands=["start"])		
async def start_comand(message: types.Message):
	await message.answer("Привет! какие показания тебя интересуют?\r\n /temp-Температура\r\n /hum-Влажность\r\n /press-Давление")

@dispb.message_handler(commands=["temp"]) # температура
async def get_parametrs(message: types.Message):
	sensor = Sensor()
	await message.answer("{0} Температура в комнате, {1:.1f}С".format(sensor.time, sensor.temp))
	
@dispb.message_handler(commands=["hum"]) # влажность
async def get_parametrs(message: types.Message):
	sensor = Sensor()
	await message.answer("{0} Влажность в комнате, {1:.1f}%".format(sensor.time, sensor.hum))
	
@dispb.message_handler(commands=["press"]) # давление атмосферное
async def get_parametrs(message: types.Message):
	sensor = Sensor()
	await message.answer("{0} Давление, {1:.1f} мм рт.ст".format(sensor.time, sensor.press))	

	
if __name__ == '__main__':
	log_writer = LogWriter()

	
	# разделение процессов работы бота и логирования показаний
	thread1 = threading.Thread(target=start_bot)
	thread2 = threading.Thread(target=log_writer.start)
	thread1.start()
	thread2.start()
	
	# запуск процессов в цикле???? 
	thread1.join()
	thread2.join()
