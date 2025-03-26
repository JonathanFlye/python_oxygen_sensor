# python_oxygen_sensor
Python library to manipulate seeedstudio dissolved oxygen sensor.

The use of this library assumes that you can communicate with the sensor 
trougth a computer serial port. To do so you can either use a USB->RS485 converter
or a microcontroller programmed as passthrougth (with a ttl->RS485 converter)

Note that the sensor has to be powered with 12V (12->24V)

## Files
- seeedO2.py is a module that allows to create an oxygen sensor class, it contains functions to read, calibrate, and make the possible settings of the sensor
- read_print_seeed02.py : is an example of use of the module that allow to read and print data from the sensor
- calibrate_100.py : is an exemple of code that allow to calibrate the 100% saturation (ideally in air-saturated water)
- log_data_seeed02.py : is an example that allows to read, print and log the data in a file with a timestamp

