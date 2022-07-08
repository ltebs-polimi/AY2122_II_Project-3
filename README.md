# Electronic Technologies and Biosensors Lab - Project 3
# Academic Year 2021/2022 - II Semester

## Smart tennis racket able to monitor and classify technical tennis movements


**GOAL**

Classification of the three main tennis shots (forehand, backhand and serve) using a tennis racket equipped with an IMU sensor.



**PROJECT SPECIFICATIONS** 

To pursue this goal we had to: 

*	Acquire and process raw accelerometer and gyroscope data from an IMU sensor.
*   Use a Bluetooth module for real-time communication between the microcontroller and the PC to make the device pluggable on a real racket.
*   Program a classification algorithm for gesture recognition.
*	Provide the end player with a Graphical User Interface to visualize in real-time the type of shots predicted during the match. 
*	Print the custom PCB to reduce instrumentation bulkiness. 
*	Design a 3D printed case that includes the microcontroller and the whole instrumentation. 



**CLINICAL NEEDS**

This project addresses the following clinical needs: 

* Sport performance 🡪 Recognizing and taking memory of shots is a feature that could simplify the work of tennis trainers, that still take notes manually, to understand if the athletes are developing some fundamentals at expenses of the others. 
In the future, associating the information about the type of shot with the corresponding number of points scored by the player can be useful to understand which are the strengths and the weaknesses of the player and therefore to better target the training. 

* Prevention 🡪 Epicondylitis is an inflammation of the wrist extensor muscles, at their point of insertion.
It is a consequence of repeated microtraumas over time, typical of those who play tennis.
Some experts state that from 10% to 50% of cases this pathology is due to an incorrect technique of execution of the backhand. 
Therefore, the number of backhand shots made by the tennis player could be a useful information for this purpose.



**HARDWARE** 

On the custom PCB are plugged the following components: 

* PSoC microcontroller 🡪 3.3V - 5V of power supply
* 9V battery
* Voltage regulator LM7805 (9V to 5V)
* MPU9250 9-axis IMU sensor 🡪 5V of power supply
* Bluetooth module HC-06 🡪 3.3V - 5V power supply 



**DEVICE DESIGN** 

Two 3D printed components, fixed together: 

* Housing of the PCB to be interlocked to the handle of the tennis racket.
* Cap of the case.



**PROBLEMS ENCOUNTERED** 

* The FIFO buffer was not used: the datasheet of the MPU9250 was cryptic, and the implementation very difficult and time consuming. So, we decided to read the data from the IMU continuously by using an interrupt. 

* We could not use the switch button: the problem was in the interrupt used to read the data, that did not allow the button to change its state. We partially fixed this problem by adding a button on the GUI. 

* We could not use the LED on the PCB: the problem was with the PCB trace that linked the LED with the ground plane. We partially solved this problem by adding a LED on the GUI. 



**FUTURE DEVELOPMENTS**

The system we have obtained up to now can be further improved by:
* Combining the intertial measurements with dynamic force sensor measurements (FSR), so as to fully characterize the tennis stroke.
* Calculate meaningful parameters from accelerations through more in-depth data post-processing, useful for biomechanical analysis.
* Visualization of the obtained data plots on the GUI.


-----------------

**Organization of the Github repository**

* *3DPrinting_PCB* 🡪 design of the 3D prints with Fusion 360
* *Acquisitions* 🡪 CSV files and Python code to train the classifier
* *Biblio* 🡪 literature
* *Datasheets* 🡪 HW components' datasheets
* *PCB* 🡪 design of the custom PCB with Eagle
* *PSOC_firmware* 🡪 C code to program PSOC microcontroller and HW components 
* *Python_serial* 🡪 Python code to acquire, decode, classify and display data on a GUI
