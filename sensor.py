# класс получения показаний с датчиков

import Adafruit_DHT as dht
import Adafruit_BMP.BMP085 as BMP085
import time

bmp = BMP085.BMP085()
DHT_PIN = 4


class Sensor:
	
	def __init__(self):

		h, t = dht.read_retry(dht.DHT22, DHT_PIN)
		p = bmp.read_pressure()
		self.hum = h
		self.press = p/133.3
		self.temp = t
		self.date = time.strftime('%m/%d/%y')
		self.time = time.strftime('%H:%M')
		self.filename = time.strftime('%m/%d/%H:%M')
