import seeedO2
from time import sleep
sens = seeedO2.SeeedO2_sensor('/dev/ttyUSB0')

while True :
    sleep(1)
    sens.print_values()

