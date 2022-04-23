#!/usr/bin/python3
import threading

from logwriter import LogWriter
from bot import start_bot


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
