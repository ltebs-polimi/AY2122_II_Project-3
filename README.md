# Electronic Technologies and Biosensors Lab - Project 3
# Academic Year 2021/2022 - II Semester


**GOAL**

Classification of the three main tennis strokes (forehand, backhand and serve) using a tennis racket equipped with an IMU sensor.



**CLINICAL NEEDS**

* Sport performance 🡪 Recognizing shots is a feature that could simplify the work of tennis of tennis schools, that still take notes manually, to understand if the students are developing some fundamentals at expenses of the others. 
In the future, associating the information about the type of shot with the corresponding number of points scored by the player can be useful, to understand which the strengths and the weaknesses are and therefore to better target training. 

* Prevention 🡪 Epicondylitis is an inflammation of the wrist extensor muscles, at their point of insertion.
It is a consequence of repeated microtraumas over time, typical of those who play tennis.
Some experts state that from 10% to 50% of cases this pathology is due to an incorrect technique of execution of the backhand. 
So, the number of backhand shots made by the tennis player could be useful information for this purpose.



**HARDWARE COMPONENTS ON THE PCB** 

* PSoC 🡪 3.3V - 5V of power supply. 

* 9V battery. 

* Voltage regulator LM7805 (from 9V to 5V). 

* 9-axis IMU 🡪 5V of power supply. 

* Bluetooth module HC-06 🡪 3.3V - 5V power supply. 



**DEVICE DESIGN** 

Two 3D printed components, fixed together: 

* Component to be interlocked to the handle of the tennis racket. 

* Housing of the PCB, equipped with the microcontroller, the sensor, the BT module and the battery. 



**PROJECT SPECIFICATION** 
* The collected data, from the accelerometer and from the gyroscope of the IMU module, allow to identify the racket movement. 
We distinguish among the three main shoots, by means of a classifier. 

* The collected data are sent to the computer by means of the Bluetooth module, in real time. 

* The Graphical User Interface allows the user to visualize the number of the three different shots done by the player in a game session, in real time.



**PROBLEMS ENCOUNTERED** 

* The FIFO buffer was not used: the datasheet of the MPU9250 was cryptic, and the implementation very difficult and time consuming. 
So, we decided to read the data from the IMU continuously by using an interrupt. 

* We could not use the switch button: the problem was in the interrupt used to read the data, that did not allow the button to change its state. 
We partially fixed this problem by adding a button on the GUI. 

* We could not use the LED on the PCB: the problem was with the PCB trace that linked the LED with the ground plane. 
We partially solved this problem by adding a LED on the GUI. 
