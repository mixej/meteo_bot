# класс ведения лога показаний с датчиков
import os
import time
import Adafruit_DHT as dht
import Adafruit_BMP.BMP085 as BMP085
#FILENAME = 'meteo' + time.strftime('%H:%M') + '.csv'
FILENAME = 'meteo'
SLEEP_TIMEOUT = 10
bmp = BMP085.BMP085()
DHT_PIN = 4

class LogWriter: 
	
	# метод для создания шапки лога, проверяет наличие запесей в файле и при отсутствии таковых записывает шапку
	def write_header(self):		
		with open(FILENAME,'a+') as file:
			if os.stat(FILENAME).st_size == 0:
				file.write('Date,Time,Temp,Hum,Press\r\n')
			elif os.stat(FILENAME).st_size >= 150:
				os.rename(FILENAME, FILENAME + time.strftime('%H:%M') + '.csv')
				file = open(FILENAME, 'w+')
				file.seek(0)
				file.close()
	
#	def file_size(self):
#		if os.stat(FILENAME).st_size >= 150:
#			os.rename(FILENAME, FILENAME + time.strftime('%H:%M') + '.csv')
#			with open(FILENAME,'w'): pass
							
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
		while True:
			self.write_header()
			self.write_line()
			time.sleep(SLEEP_TIMEOUT)
