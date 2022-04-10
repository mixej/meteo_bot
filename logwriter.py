# класс ведения лога показаний с датчиков
import os
import time
import shutil
import Adafruit_DHT as dht
import Adafruit_BMP.BMP085 as BMP085
#FILENAME = 'meteo' + time.strftime('%H:%M') + '.csv'
FILENAME = 'meteo'
DIRNAME = 'Base'
SLEEP_TIMEOUT = 10 #время между считыванием показаний
MAXFILESIZE = 100
bmp = BMP085.BMP085()
DHT_PIN = 4

class LogWriter: 
	
	
	def write_header(self):	
	# метод для создания шапки лога, проверяет наличие запесей в файле и при отсутствии таковых записывает шапку	
		with open(FILENAME,'w') as file:
			file.write('Date,Time,Temp,Hum,Press\r\n')
	
	def dir_make(self):
		if os.stat(FILENAME).st_size == 0:
			self.write_header()	
		try:
			os.mkdir(DIRNAME)
		except Exception as e:
			pass		
	
	
	def file_cp(self):
	#метод переименовывает фаил->перемещает его в папку и стирает исходный	
		new_file = FILENAME + time.strftime('%H:%M') + '.csv'
		os.rename(FILENAME, new_file)
		shutil.move(new_file, DIRNAME)
#		open(FILENAME,"w").close()

							
	
	def write_line(self):
	# метод считывает показания с датчиков и пишет их в лог фаил			
		h, t = dht.read_retry(dht.DHT22, DHT_PIN)
		p = bmp.read_pressure()
		if all(var is not None for var in [h,t,p]) and os.stat(FILENAME).st_size <= MAXFILESIZE:
			with open(FILENAME,'a+') as file:
				file.write('{0},{1},{2:0.1f},{3:0.1f},{4:0.1f},\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), t, h, p/133.3))
		else:
			self.file_cp()
			self.write_header()


	def start(self):
	# метод для запуска функций лога данных в фаил 
	# проверяет наличие шапки и пишет показания с указанным интервалом	
		with open(FILENAME,'w') as file:
		self.dir_make()
		
		while True:
			self.write_line()
			time.sleep(SLEEP_TIMEOUT)
