# класс получения показаний с датчиков



import RPi.GPIO as GPIO
import Adafruit_DHT as dht
import Adafruit_BMP.BMP085 as BMP085
import time
#from config import bmp, DHT_PIN



bmp = BMP085.BMP085()
DHT_PIN = 4




class Sensor:
	
	def __init__(self):

		h, t = dht.read_retry(dht.DHT22, DHT_PIN)
		p = bmp.read_pressure()
		self.hum = h
		self.press = p/133.3
		self.temp = t
		self.date = time.strftime('%d-%m-%y')
		self.time = time.strftime('%H:%M')
		
