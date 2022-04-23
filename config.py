# имена файлов
FILENAME = 'meteo'
DIRNAME = 'Base'

# переменные ведения лога
SLEEP_TIMEOUT = 5 # время между считыванием показаний
MAXFILESIZE = 150 # размер файла для копирования в архив

# переменные датчиков
bmp = BMP085.BMP085()
DHT_PIN = 4
