import seeedO2
from time import sleep
from datetime import datetime

sens = seeedO2.SeeedO2_sensor('/dev/ttyUSB1')

while True : 
	sleep(1)
	line_to_write = datetime.now().strftime("%m/%d/%Y %H:%M:%S")+ ";" + sens.write_values() +"\n"
	print(line_to_write)
	with open("datalog.csv", "a") as f:
   		f.write(line_to_write)


