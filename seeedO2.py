# Program to manipulate seeedstudio dissolved oxygen optical sensor
# Needs either a USB-RS485 converter or a microcontroller programmed as passthrougth
# J Flye-Sainte-Marie 
# 03/2025
# 
# 


#!/usr/bin/env python3

import serial
import minimalmodbus
from time import sleep



class SeeedO2_sensor(minimalmodbus.Instrument):
    def __init__(self, port='/dev/ttyUSB0', slave_address=55, baudrate=9600):
        super().__init__(port, slave_address)
        self.serial.baudrate = baudrate  # baudrate
        self.serial.bytesize = 8
        self.serial.parity   = serial.PARITY_NONE
        self.serial.stopbits = 1
        self.serial.timeout  = 0.1      # seconds
        self.address = slave_address
        self.mode = minimalmodbus.MODE_RTU # rtu or ascii mode
        self.clear_buffers_before_each_transaction = True
        self.close_port_after_each_call = True
        
    def read_raw_values(self):
        """
        Read temperature, DO, and Oxygen saturation values.
        Return a list with:
           - temperature x 10
           - DO x 100
           - Sat x 10
        """
        return self.read_registers(256, 3)
    
    def calibrate_100(self):
        """
        Calibration of the 100% saturation in air-saturated water,
        returns calibration slope
        """
        self.write_register(4099, 0, number_of_decimals=0, functioncode=6)
        return self.read_registers(4099, 1)[0] / 100
	
    def calibrate_0(self):
        """
        Calibration of the 0% in anaerobic water (you can use sodium sulfite in water),
        returns the 0 offset
        Note that after zero calibration the sensor will always return a 0.04mg/L value of DO (and 0.4% saturation)
        """
        self.write_register(4097, 0, number_of_decimals=0, functioncode=6)
        return self.read_registers(4097, 1)[0]
    
    def calibrate_temp(self, temp_cal):
        """
        Temperature calibration

        Parameter:
        Temperature of the calibration solution

        Returns the calibration offset

        When calibrating in solution, the written data is the actual temperature value × 10;
        the read data is the temperature calibration offset × 10.
        """
        self.write_register(4096, temp_cal * 10, number_of_decimals=0, functioncode=6)
        sleep(1)
        return self.read_registers(4096, 1)[0] / 10
    
    def set_sensor_add(self, address):
        """
        Set sensor Modbus address

        Parameter:
        Modbus address from 1 to 127, default is 55
        """
        if 1 <= address <= 127:
            print(f"Address {address} is valid.")
            self.write_register(8192, address, number_of_decimals=0, functioncode=6)
        else:
            print(f"Address {address} is invalid.")

    def reset_sensor(self):
        """
        Reset sensor 

        The calibration value is restored to the default value.
        Note: After the sensor is reset, it needs to be calibrated again before it can be used
        """
        self.write_register(8224, 0, number_of_decimals=0, functioncode=6)
            
    def correct_values(self, oxy_sens_values):
        """
        Converts raw values read from the Seeedstudio DO sensor
        - temperature (divided by 10),
        - dissolved oxygen (DO, divided by 100),
        - oxygen saturation (SatO2, divided by 100).

        Parameters:
        oxy_sens_values (list): A list of sensor values. The list must contain at least 3 elements.
                                [Temp, DO, SatO2].

        Returns:
            list: A list containing the formatted values [Temp, DO, SatO2], all divided by their respective factors.
        """
        Temp = oxy_sens_values[0] / 10  # Convert temp
        DO = oxy_sens_values[1] / 100   # Convert DO
        SatO2 = oxy_sens_values[2] / 10  # Convert oxygen saturation
        return [Temp, DO, SatO2]
        
    def set_baudrate(self, baudrate):
        """
        Set sensor communication baudrate

        The default value is 9600. Write 0 to 4800; Write 1 to 9600; Write 2 to 19200

        Note that the modification will only take effect after restarting the sensor

        Warning: if you use a microcontroller to get data from the sensor, take care to 
        set adequate microcontroller baudrate communication with sensor
        """
        if baudrate == 4800: 
            self.write_register(8195, 0, number_of_decimals=0, functioncode=6)
            print('Done')
        elif baudrate == 9600:
            self.write_register(8195, 1, number_of_decimals=0, functioncode=6)
        elif baudrate == 19200:
            self.write_register(8195, 2, number_of_decimals=0, functioncode=6)
        else:
            print(f"Baudrate {baudrate} is invalid.")
        
        sleep(1)
        print(self.read_registers(8195, 1))
        
    def format_oxy_sens_values(self, to_format):
        """
        Formats converted Seeedstudio DO sensor values for display
        """
        return "Temp:" + str(to_format[0]) + "°C, DO: " + str(to_format[1]) + "mg/L, Sat: " + str(to_format[2]) + '%'

    def format_to_write(self, to_format):
        """
        Formats converted Seeedstudio DO sensor values for saving in file
        """
        return str(to_format[0]) + ";°C;" + str(to_format[1]) + ";mg/L;" + str(to_format[2]) + ';%;'
          
    def read_values(self) :
        """
        Reads ans correct the sensor values
        """  
        values = self.read_raw_values()
        corr_values = self.correct_values(values)
        return corr_values

        
    def print_values(self):
        """
        Reads and corrects the sensor values and print with units
        """
        values = self.correct_values(self.read_raw_values())
        print(self.format_oxy_sens_values(values))

    def write_values(self):
        """
        Reads and format the sensor values to write them in a file
        """
        values = self.correct_values(self.read_raw_values())
        return self.format_to_write(values)
        




    



	








	











