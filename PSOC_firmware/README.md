## Electronic Technologies and Biosensors Lab - Project 3
## Academic Year 2021/2022 - II Semester


# PSoC CODE

This code allows to use a MPU9250 9-axis IMU sensor with a PSoC microcontroller to acquire and transmit accelerometer and gyroscope data using a Bluetooth module. 	

*AnnotationLibrary_lib* is necessary to use the components' APIs and run the code.


--------------------------------------------

**DEFAULT IMU SETTINGS**

- Accelerometer and gyroscope data from the IMU are read when the "Data Ready" internal interrupt is triggered, reporting that "New data is available to be read from Sensors Registers".

- The sample rate is set to 200 Hz by scaling the internal sample rate equal to 1kHz with a sample rate divider equal to 4: SMPLRT = INT_SMPLRT / (1 + SMPLRT_DIV)

- The accelerometer data is expressed in &#177;2 g while the gyroscope data is expressed in &#177;250 dps (degrees per second).

In the *MPU9250.c* file are present all the functions to handle the IMU registers and the FIFO buffer (not used at the end).
The function used to opportunely set the IMU registers in order to follow these settings is *MPU9250_Start()*.


**CODE**

In MPU9250, for each axis of each measurement there are 2 registers containing high and low bytes, for a total of 12 bytes.

We set up the reading settings as follows:

* 1 frame (*data*) containing &#x2192; 12 bytes: contents of the registers related to accelerometer and gyroscope measurements.

* 1 packet (*packet_to_send*) containing &#x2192; (*N_FRAME* * 12 + 2 ) bytes: 
    -	1 HEADER = 0XA0
    -	*N_FRAME* * 12 
    -	1 TAIL = 0XC0

After reading *N_FRAME*, the packet is sent to the PC via HC-06 Bluetooth module (baud rate = 57600 bps).

We set *N_FRAME* = 10, thus creating packets made of 122 bytes.


