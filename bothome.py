import asyncio
import requests
import datetime
import threading

import os
import time
import Adafruit_DHT as dht
import Adafruit_BMP.BMP085 as BMP085

from config import TOKEN
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=TOKEN)
dispb = Dispatcher(bot)

bmp = BMP085.BMP085()
DHT_PIN = 4
FILENAME = 'meteo.csv'
SLEEP_TIMEOUT = 300

# класс ведения лога показаний с датчиков
class LogWriter: 

	# метод для создания шапки лога, проверяет наличие запесей в файле и при отсутствии таковых записывает шапку
	def write_header(self):		
		with open(FILENAME,'a+') as file:
			if os.stat(FILENAME).st_size == 0:
				file.write('Date,Time,Temp,Hum,Press\r\n')
	# метод считывает показания с датчиков и пишет их в лог фаил			
	def write_line(self):
		h, t = dht.read_retry(dht.DHT22, DHT_PIN)
		p = bmp.read_pressure()
		if all(var is not None for var in[h,t,p]):
			with open(FILENAME,'a+') as file:
				file.write('{0},{1},{2:0.1f},{3:0.1f},{4:0.1f},\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), t, h, p/133.3))
		else:
			print("Failed to retrieve data from humidity sensor")
	# метод для запуска функций лога данных в фаил 
	# проверяет наличие шапки и пишет показания с указанным интервалом			
	def start(self):
		self.write_header()
		while True:
			self.write_line()
			time.sleep(SLEEP_TIMEOUT)

# функция запуска бота телеграмм
def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    executor.start_polling(dispb)
		
		
@dispb.message_handler(commands=["start"])		
#@db.message_handler()
async def start_comand(message: types.Message):
	await message.answer("Привет! какие показания тебя интересуют?\r\n /temp-Температура\r\n /hum-Влажность\r\n /press-Давление")

@dispb.message_handler(commands=["temp"])
async def get_parametrs(message: types.Message):

	h, t = dht.read_retry(dht.DHT22, DHT_PIN)
	#p = bmp.read_pressure()
	await message.answer("{0} Температура в комнате, {1:.1f}С".format(time.strftime('%H:%M'), t))
	
@dispb.message_handler(commands=["hum"])
async def get_parametrs(message: types.Message):

	h, t = dht.read_retry(dht.DHT22, DHT_PIN)
	#p = bmp.read_pressure()
	await message.answer("{0} Влажность в комнате, {1:.1f}%".format(time.strftime('%H:%M'), h))
	
@dispb.message_handler(commands=["press"])
async def get_parametrs(message: types.Message):

	#h, t = dht.read_retry(dht.DHT22, DHT_PIN)
	p = bmp.read_pressure()
	await message.answer("{0} Давление, {1:.1f} мм рт.ст".format(time.strftime('%H:%M'), p/133.3))	

	
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
