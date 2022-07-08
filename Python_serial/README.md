## Electronic Technologies and Biosensors Lab - Project 3
## Academic Year 2021/2022 - II Semester


# PYTHON code 

This code allows to:
1.  Collect via Bluetooth the raw data from an MPU9250 9-axis IMU sensor mounted on a smart tennis racket;
2.	Classify the tennis shot made according to the accelerometer & gyroscope measurements obtained;
3.	Display on a GUI the type of shot predicted in real-time.

> IMPORTANT:
* *BT_COM* needs to be specified according to your PC settings.
* *training_dataset.csv* file must be present in the same folder as this code.

--------------------------------------------

**GUI WINDOW & WIDGETS**

In order to create the GUI we have used *Tkinter Python Library* and to make it communicate with the Classification Algorithm we used *Threading Python Library*. 

The GUI contains the following widgets: 

* Timer, which keeps track of the time of the acquisition session.

* LED, which turns green or red depending on the acquisition phase.

* Scoreboard, containing the scores related to the different shots predicted by the Classification Algorithm: *serve*, *forehand* and *backhand*.

* Buttons: 
    * COM 🡪 to open the serial port (COM) and build the Random Forest Classifier.
    * START 🡪 to enable the Timer and to activate the 2 threads: *Start_GUI()* and *Start_acquisition()*.
    * STOP 🡪 to disable the Timer and to block the acquisitions, thus showing the number of shots made up to that moment.
    * RESET 🡪 to reset Timer and Scoreboard in order to prepare them for another session (to be used after pushing the STOP button).


--------------------------------------------

**DATA COLLECTION**

Once the COM button is pressed, the *BT_COM* port of the Bluetooth module HC-06 is open at baudrate = 57600 bps.
When the START button is pressed, the 2° thread (*Start_acquisition()*) calls the function *Predict_Data_Packet()* which allows to acquire and classify the data from the IMU. 

Each acquisition is done by reading *N_PACKETS* and decoding the corresponding array of data (*data*).
With *N_PACKETS* = 40, the acquisition takes about 4 seconds, which is approximatively equal to the duration of one tennis shot during a match.

Each packet contains 122 bytes: 
-	1 HEADER = 0XA0
-	120 bytes, representing 10 frames of data: each frame contains 12 bytes corresponding to accelerometer and gyroscope data registers, with 2 bytes (high and low bits) for each ACCX, ACCY, ACCZ, GYRX, GYRY, GYRZ reading.
-	1 TAIL = 0XC0

Data decoding is done by creating a *mat_big* matrix with:
-	400 rows 🡪 *N_FRAME* * *N_PACKETS* = 10*40 
-	6 columns 🡪 raw data: ACCX, ACCY, ACCZ, GYRX, GYRY, GYRZ (obtained by merging high bytes & low bytes for each measurement and converting the acceleration and gyroscope values to the right FSR (&#177;2g, &#177;250 dps)).

This matrix is then given to the Classification Algorithm that, about every 4 seconds, predicts the type of shot.


--------------------------------------------

**RANDOM FOREST CLASSIFIER**

TRAINING

The *Classifier_Training()* function is run just once when the COM button is pressed. 
The Random Forest Classifier has been trained with 140 acquisitions (*training_dataset.csv*). 
One acquisition is given by the 1°, 2° and 3° quantiles values of the 6 IMU measurements.

For more details about acquistions and choice of the classifier see the *acquisition_protocol.pdf* file.

MAKING PREDICTIONS

In the *Predict_Data_Packet()* function, from the *mat_big* matrix (representing one acquisition) the 1° (0.25), 2° (0.5 = median) and 3° (0.75) quantiles of each IMU measurement are extracted and used to guess the shot made with the Random Forest classifier. 
The label *shot* returned by the Classification Algorithm is then used to updates the shots' counts in the Scoreboard: 
- shot = 0 🡪 Forehand
- shot = 1 🡪 Backhand
- shot = 2 🡪 Serve
- shot = 3 🡪 "no shot" 

