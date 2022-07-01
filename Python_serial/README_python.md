# Electronic Technologies and Biosensors Lab - Project 3
# Academic Year 2021/2022 - II Semester


## PYTHON code 

This code allows to:
1.  Collect via Bluetooth the raw data from the IMU MPU9250 sensor placed on the smart tennis racket;
2.	Classify the tennis shot according to the measurements obtained;
3.	Display the type of the different shots made on a GUI.


--------------------------------------------

**DATA COLLECTION**

Once the battery is connected, the device sends the array containing the raw data to the PC via Bluetooth module HC-06 (baud rate 57600 bps). 

Acquisition is done by reading *N_PACKETS* and decoding the corresponding array of data, thus creating the corresponding CSV file.

With *N_PACKETS* = 40, the acquisition takes about 5 seconds (including the time to open COM port), which is approximatively equal to the duration of one tennis shot.

Each packet contains 122 bytes: 
-	1 HEADER = 0XA0
-	120 bytes =  10 frames of data: each frame contains 12 bytes corresponding to accelerometer and gyroscope readings, with 2 bytes (high and low bits) for each ACCX, ACCY, ACCZ, GYRX, GYRY, GYRZ.
-	1 TAIL = 0XC0

Data decoding is done by filling by creating a *mat_big* matrix (400x6) 
-	rows -> *N_FRAME* * *N_PACKETS* = 10*40 
-	columns -> raw data: ACCX, ACCY, ACCZ, GYRX, GYRY, GYRZ (merging high bytes & low bytes for each measurement and converting the acceleration and gyroscope values to the right FSR (+-2g, +-250 dps).

This matrix is then exported to the CSV file named *acquisition_file.csv*.



--------------------------------------------

**RANDOM FOREST CLASSIFIER**

* TRAINING

Random Forest multiclass classifier has been trained with 55415 values (*training_dataset.csv* opportunely cleaned). For more details see  the *ACQUISITION_PROTOCOL.pdf* file.

The proportion for training-test splitting has been set to 70-30%.


*  MAKE PREDICTIONS

The *acquisition_file.csv*, processed as the training dataset (removing NaN and infinte values) thus containing approximately 400 values, is fed into the classifier that returns as target variable the type of shot corresponding to that pattern of accelerometer and gyroscope measurements.

The variable *shot* is then given to the GUI that in turn updates the shots’ counts accordingly.

--------------------------------------------

**GUI**
