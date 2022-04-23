# класс ведения лога показаний с датчиков
import os
import time
import shutil
from sensor import Sensor 
import config

#FILENAME = 'meteo'
#DIRNAME = 'Base'
#SLEEP_TIMEOUT = 5 # время между считыванием показаний
#MAXFILESIZE = 150 # размер файла для копирования в архив


class LogWriter: 
	
	
	def write_header(self):	
	# метод для создания шапки лога, проверяет наличие запесей в файле и при отсутствии таковых записывает шапку	
		with open(FILENAME,'w') as file:
			file.write('Date,Time,Temp,Hum,Press\r\n')
	
	def dir_make(self):
	# создание директории для лога данных
		try:
			os.mkdir(DIRNAME)
		except FileExistsError:
			pass		
	
	
	def file_cp(self):
	# метод переименовывает фаил->перемещает его в папку и стирает исходный
	# добавить проверку совпадения имени файла	
		sensor = Sensor()
		new_file = time.strftime('%m-%d_%H:%M') + '.csv'
		os.rename(FILENAME, new_file)
		shutil.move(new_file, DIRNAME)
		self.write_header()

							
	
	def write_line(self):
	# метод считывает показания с датчиков и пишет их в лог фаил	
		sensor = Sensor()		
		if all(var is not None for var in [sensor.hum, sensor.press, sensor.temp]) and os.stat(FILENAME).st_size <= MAXFILESIZE:
			with open(FILENAME,'a+') as file:
				file.write('{0},{1},{2:0.1f},{3:0.1f},{4:0.1f}\r\n'.format(sensor.date, sensor.time, sensor.temp, sensor.hum, sensor.press))
		else:
			self.file_cp()


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
