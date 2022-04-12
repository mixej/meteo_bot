# класс ведения лога показаний с датчиков
import os
import time
import shutil
from sensor import Sensor 

FILENAME = 'meteo'
DIRNAME = 'Base'
SLEEP_TIMEOUT = 10 #время между считыванием показаний
MAXFILESIZE = 100 #РАЗМЕР ФАЙЛА ДЛЯ КОПИРОВАНИЯ А АРХИВ
sensor = Sensor()

class LogWriter: 
	
	
	def write_header(self):	
	# метод для создания шапки лога, проверяет наличие запесей в файле и при отсутствии таковых записывает шапку	
		with open(FILENAME,'w') as file:
			file.write('Date,Time,Temp,Hum,Press\r\n')
	
	def dir_make(self):

		try:
			os.mkdir(DIRNAME)
		except Exception as e:
			pass		
	
	
	def file_cp(self):
	#метод переименовывает фаил->перемещает его в папку и стирает исходный	
		
		new_file = FILENAME + sensor.time + '.csv'
		os.rename(FILENAME, new_file)
		shutil.move(new_file, DIRNAME)
		self.write_header()

							
	
	def write_line(self):
	# метод считывает показания с датчиков и пишет их в лог фаил			
		if all(var is not None for var in [sensor.hum, sensor.press, sensor.temp]) and os.stat(FILENAME).st_size <= MAXFILESIZE:
			sensor.__init__()
			with open(FILENAME,'a+') as file:
				file.write('{0},{1},{2:0.1f},{3:0.1f},{4:0.1f},\r\n'.format(sensor.date, sensor.time, sensor.temp, sensor.hum, sensor.press))
		else:
			self.file_cp()
#			self.write_header()


	def start(self):
	# метод для запуска функций лога данных в фаил 
	# проверяет наличие шапки и пишет показания с указанным интервалом	
		
		self.dir_make()
		try:
			if os.stat(FILENAME).st_size == 0:
				self.write_header()
		except FileNotFoundError:
			self.write_header()
		while True:
			
			self.write_line()
			time.sleep(SLEEP_TIMEOUT)
