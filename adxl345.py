
# In this program we log data of an accelerometer(adxl345).
# Output data is printed out in both the raw decimal value of each axis as well as the m/s^2 format.  
# To enable I2C mode: pin !CS: connected to Vdd.
# ALT ADDRESS(pin12): Vdd ---> I2C Add= 0x1D(followed by R/!W bit)
# ALT ADDRESS(pin12): GND ---> I2C Add= 0x53(followed by R/!W bit)
# To set up adxl345 we need to initialize these registers:
# BW_RATE register(add 0x2c):0x09 
# 	LOW_POWER bit= 0: normal operation
#	Output data rate: 50Hz(BW=25Hz)
# POWER_CTL(add 0x2d):0x08
#	AUTO_SLEEP: disabled
# DATA_FORMAT(add 0x31):0x08
#	Self-Test: disabled
#	Full resolution
#	+/-2g(10 bits)
#
# DATAX, DATAY, DATAZ Registes: Add 0x32 to 0x37	
#
#    Raspberry-pi		ADXL345
#    1(3.3v)	  		 Vcc 
#    3(SDA)			 SDA
#    5(SCL)			 SCL
#    6(GND)			 GND
#				 SDO	Vcc --> ADXL345_add=0x1d
#				 !CS    Vcc --> ADXL345 in i2c mode
import smbus
import time

# define addresses
adxl345_add = 0x1d
BW_Rate_reg_add = 0x2c 
PWR_CTL_reg_add = 0x2d
DATA_FORMAT_reg_add = 0x31
DATAX0_add = 0x32
DATAX1_add = 0x33
DATAY0_add = 0x34
DATAY1_add = 0x35
DATAZ0_add = 0x36
DATAZ1_add = 0x37

# Get I2C bus
bus = smbus.SMBus(1) # opens /dev/i2c-1

scale_factor_2g = 3.9 # 3.9mg/LSB
gravity_value_ms2 = 9.8 # 1g = 9.8m/s^2

def init_adxl_register():
# Initialize Registers
# Set BW_Rate Reg. to 0x09:
#       Normal operation, Output data rate= 50 Hz
	bus.write_byte_data(adxl345_add, BW_Rate_reg_add, 0x09)

# Set POWER_CTL Reg. to 0x80:
# 	Disable auto_sleep
	bus.write_byte_data(adxl345_add, PWR_CTL_reg_add, 0x08)

# Set DATA_FORMAT Reg. to 0x08:
#	Disable self_test, SPI  
# 	set to full_resolution, OutputResolution: +/-2g Range(10 bit)
#	set sensitivity mode of device to 2g --> each LSB = 3.9milli g
#	1g = 9.8m/s^2 
	bus.write_byte_data(adxl345_add, DATA_FORMAT_reg_add, 0x08)


def read_axis_data():
# Read Data from X-Axis LSB, X-Axis MSB
#X0_LSB = bus.read_byte_data(adxl345_add, DATAX0_add)
#X1_MSB = bus.read_byte_data(adxl345_add, DATAX1_add)
	x = bus.read_i2c_block_data(adxl345_add, DATAX0_add, 2)
	XAccl = (x[1] * 256) + x[0]
#	XAccl1 = (x[1]<<8) | x[0]
	if (XAccl > 511): # bit 10 is 1: XACC1 is 2's complement of a digit
		XAccl = XAccl-1024 # gives back the real negative value of XAccl
	XAccl = XAccl * scale_factor_2g
    	#XAccl = XAccl * scale_factor_2g
	XAccl1 = XAccl * gravity_value_ms2
        #XAccl1 = XAccl * gravity_value_ms2
    	
    	#XAccl1 = XAccl * gravity_value_ms2
    	#XAccl1 = XAccl * gravity_value_ms2 # result as m/s^2
	XAccl = round(XAccl,4)
	XAccl1 = round(XAccl1,4) 
# Read Data from Y-Axis LSB, Y-Axis MSB
#Y0_LSB = bus.read_byte_data(adxl345_add, DATAY0_add)
#Y1_MSB = bus.read_byte_data(adxl345_add, DATAY1_add)
	y = bus.read_i2c_block_data(adxl345_add, DATAY0_add, 2)
	YAccl = (y[1] * 256) + y[0]
	if (YAccl > 511):
		YAccl = YAccl -1024
	YAccl = YAccl * scale_factor_2g
	YAccl1 = YAccl * gravity_value_ms2 # result as m/s^2
	YAccl = round(YAccl,4)
	YAccl1 = round(YAccl1,4)
# Read Data from Z-Axis LSB, Z-Axis MSB
#Z0_LSB = bus.read_byte_data(adxl345_add, DATAZ0_add)
#Z1_MSB = bus.read_byte_data(adxl345_add, DATAZ1_add)
	z = bus.read_i2c_block_data(adxl345_add, DATAZ0_add, 2)
	ZAccl = (z[1] * 256) + z[0]
	if (ZAccl > 511):
		ZAccl = ZAccl -1024
	ZAccl = ZAccl * scale_factor_2g
	ZAccl1 = ZAccl * gravity_value_ms2 # result as m/s^2
	ZAccl = round(ZAccl,4)
	ZAccl1 = round(ZAccl1,4) 
	return(XAccl, YAccl, ZAccl, XAccl1, YAccl1, ZAccl1)

if __name__ == '__main__':
        init_adxl_register()
        time.sleep(0.5)
        while(True):
                xaxis, yaxis, zaxis, xaxis_g, yaxis_g, zaxis_g = read_axis_data()
                #print('{0:9}'.format('X-axis:'),xaxis, '{0:9}'.format('Y-axis:'),yaxis, '{0:9}'.format('Z-axis:'),zaxis)
                print('X-axis:',xaxis, ' Y-axis:',yaxis, ' Z-axis:',zaxis)
                print('X-m/s^2:',xaxis_g, ' Y-m/s^2:',yaxis_g, ' Z-m/s^2:',zaxis_g)
