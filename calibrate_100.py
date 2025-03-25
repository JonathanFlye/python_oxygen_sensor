import seeedO2
from time import sleep
sens = seeedO2.SeeedO2_sensor('/dev/ttyUSB0')

print('Values BEFORE calibration :')
for i in range(1,10):
    sleep(1)
    sens.print_values()


cal_slope = sens.calibrate_100()
print('Calibration slope :' + str(cal_slope))

print('Values AFTER calibration:')
for i in range(1,10):
    sleep(1)
    sens.print_values()
