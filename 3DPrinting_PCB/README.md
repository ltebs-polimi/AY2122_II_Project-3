## Electronic Technologies and Biosensors Lab - Project 3
## Academic Year 2021/2022 - II Semester

# CASE DESIGN with FUSION360 


**PREREQUISITES**

The ideal case should be:
-  positioned in a spot on the racket that could not be hit by ball strikes during the game session;
- the least bulky as possible.

To pursue these goals, we thought of print 2 components:
1. a main body for PCB housing 🡪 to be attached to the handle of the racket, with a geometry compatible with the size of the PCB;
2. an end cap 🡪 that would allow to open the case to possibly change PCB and its components. 

The main body presents also two holes, one for a switch button to use to activate the device, one for an LED to signal that the device is running. However, these 2 components were not used in the final device. 

We used the Fusion360 to create the design, by following the steps reported below. 

----------------------------------------

**STEPS**

1. MAIN BODY FOR PCB HOUSING

- Create the sketch consisting of a rectangle with sides 50 mm x 60 mm.
- Extrude the sketch from two sides, one to create a hollow parallelepiped of 40 mm height and 3 mm thickness that would fit perfectly to the racket handle, the other to create a parallelepiped of 100 mm height and 2 mm wall thickness that would contain the PCB. 
- Create the 1 mm thick guides on the two side faces of the parallelepiped, starting with 3.6 mm of the middle of the side face. The guides are used to hold the PCB in place.
- Create two holes 0.8 mm and 0.5 mm in diameter at 50 mm and 60 mm from the base for the led and button, respectively.  

2. END CAP

- Divide the body intended to hold the PCB through a dividing plane, at the height of 20 mm from the bottom, thus obtaining two bodies, one upper and one lower.
- Create an intermediate plane between the two outer faces of the upper body.
- Create a sketch on the plane just found.
- Project the whole lower body onto the sketch.
- Establish an interlocking tolerance of 0.5 mm.
- Draw the interlock, by projecting the height of the toggle equal to 7mm.
- Create an extrusion profile of symmetrical type, width equal to 5 mm.
- Create the sketch on the face where the interlock is to be created.
- Project the interlock onto the wall to create the seat of the interlock.
- Set a tolerance offset for the interlock.
- Extrude along the full length of the body thus creating the interlock seat.


