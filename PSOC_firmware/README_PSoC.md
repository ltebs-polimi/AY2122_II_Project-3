# Electronic Technologies and Biosensors Lab - Project 3
# Academic Year 2021/2022 - II Semester


## PSoC CODE

This code allows to use a MPU9250 IMU sensor with a PSoC device to acquire and transmit accelerometer and gyroscope data using I2C protocol. 	

*AnnotationLibrary_lib* is necessary to use the components APIs and run the code.


--------------------------------------------

**DEFAULT IMU SETTINGS**

Accelerometer and gyroscope data are read and sent via Bluetooth when the "Data Ready" interrupt internal to the IMU is triggered ("New data is available to be read from Sensors Registers").

The sample rate is set to 200 Hz by scaling the internal sample rate equal to 1kHz with a sample rate divider equal to 4:
SMPLRT = INT_SMPLRT / (1 + SMPLRT_DIV)

The accelerometer data is expressed in +-2g while the gyroscope data is expressed in +-250 dps (degrees per second).

The function used to opportunely set the IMU registers is *MPU9250_Start()*.


**DATA READING**

The reading of the registers containing data respects the following setting: 

* 1 frame (*data[]*) contains -> 12 bytes: contents of the IMU MPU9250 registers related to accelerometer and gyroscope reads

* 1 packet (*packet_to_send[]*) contains -> (*N_FRAME* * 12 + 2 ) bytes: 
    -	1 HEADER = 0XA0
    -	*N_FRAME* * 12 
    -	1 TAIL = 0XC0

After reading *N_FRAME*, the packet is sent serially via Bluetooth module HC-06 to the PC (baud rate = 57600 bps).



