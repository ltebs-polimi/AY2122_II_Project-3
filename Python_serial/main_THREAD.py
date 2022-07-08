#--------------------------------------------- IMPORT LIBRARIES ----------------------------------------------#

import threading 
from threading import Thread
from threading import Lock
from tkinter import *
from turtle import shape
import serial as sr
import numpy as np
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt 
import time
import sklearn
import csv
import glob
import os

TK_SILENCE_DEPRECATION=1

#------------------------------------------ VARIABLES DEFINITION --------------------------------------------#

# Global variables
global b, d, r
global update_time
global score_b, score_r, score_d
global model_rf 
global shot    
global n_packets 
global n_frame 
global send_bytes 
global mat 
global serialPort
global data
global flag_stop
global flag_reset 
global flag_start
global hit


# Variables initialization
hour, minute, second = 0, 0, 0
running = False 
flagb = False 
flagr = False 
flagd = False 
flag_start = False
flag_stop = False
flag_reset = False
BT_COM = "COM19"                                    # Bluethoot HC-06 COM port
n_packets = 40                                      # Number of packets to classify 1 gesture
n_frame = 10                                        # Each packet has n_frame
send_bytes = (12*n_frame)+2                         # Bytes within 1 packet sent by the BT 
mat = np.zeros(shape=(n_frame,6), dtype=np.float16) # Array wtih inside 1 packet of data 




#------------------------------------------ FUNCTIONS DEFINITIONS --------------------------------------------#


##############################################
# Multithreading():
# MULTITHREADING FUNCTION RUNNING IN PARALLEL
#   1. GUI activation
#   2. Data acquisition
##############################################

def Multithreading():
  global t1
  global t2
 
  t1 = Thread(target = Start_GUI)
  t2 = Thread(target = Start_acquisition)
  
  t1.start()
  t2.start()


#############################################################
# Clock():
# FUNCTION ACTIVATING THE CLOCK WHEN START BUTTON IS PRESSED
############################################################# 
  
def Clock():
  global hour, minute, second
  global update_time

  second = second + 1 

  if second == 60:
    minute += 1 
    second = 0 

  if minute == 60:
    hour += 1 
    minute = 0 
            
  string_hour = f'{hour}' if hour > 9 else f'0{hour}'
  string_minute = f'{minute}' if minute > 9 else f'0{minute}'
  string_second = f'{second}' if second > 9 else f'0{second}'
                    
  clock_timer.config(text = string_hour + ":" + string_minute + ":" + string_second)
  update_time = clock_timer.after(1000, Clock)


#############################
# Stop_GUI():
# FUNCTION FREEZING THE GUI
#############################

def Stop_GUI():
  global flag_stop
  global running
  global flagr, flagb, flagd
  global hit
  global b, d, r 

  acquisition.destroy()
  flag_stop = True

  # Stop timer updating
  if running:
    clock_timer.after_cancel(update_time)
    running = False

  # Switch off led
  box_led4 = Canvas(window, bd =0, bg = "#666699", height= 80, width = 80, highlightthickness=0)
  box_led4.grid(row = 20, columns = 7, padx = 135, sticky = "W")
  oval3 = box_led4.create_oval(25,22,55,52, fill = "red")

  # Plot the most frequent hit
  if (b > r and b > d):
    print(b)
    hit = Label(window, text = "The most frequent hit was SERVE", font = ("Orator Std", 15, 'bold'), fg = "#660033", bg = "#666699")   
    hit.grid(row = 40, columns = 8, pady = 50, padx = 160, sticky = "W")

  if (r > b and r > d):
    hit = Label(window, text = "The most frequent hit was BACKHAND", font = ("Orator Std", 15, 'bold'), fg = "#660033", bg = "#666699")   
    hit.grid(row = 40, columns = 8, pady = 50, padx = 160, sticky = "W")

  if (d > r and d > b):
    hit = Label(window, text = "The most frequent hit was FOREHAND", font = ("Orator Std", 15, 'bold'), fg = "#660033", bg = "#666699")   
    hit.grid(row = 40, columns = 8, pady = 50, padx = 160, sticky = "W")

  flagb = False
  flagd = False
  flagr = False
        

#############################
# Reset():
# FUNCTION FOR RESET THE GUI
#############################

def Reset():
  global flag_reset
  global b,d,r
  global flagr, flagb, flagd
  global hour, minute, second
  global b, r, d
  global hit

  hit.destroy()
  acquisition.destroy()

  flag_reset = True

  # Reset scores
  if running:
    clock_timer.after_cancel(update_time)
    score_b.after_cancel(update_scoreboard1)
    score_d.after_cancel(update_scoreboard2)
    score_r.after_cancel(update_scoreboard3)

  flagb = False
  flagd = False
  flagr = False

  # Reset clock time
  hour, minute, second = 0, 0, 0
  b, r, d = 0, 0, 0
  clock_timer.config(text = "00:00:00")
  score_b.config(text="0")
  score_r.config(text="0")
  score_d.config(text="0")

  # Swith OFF led
  box_led3 = Canvas(window, bd =0, bg = "#666699", height= 80, width = 80, highlightthickness=0)
  box_led3.grid(row = 20, columns = 7, padx = 135, sticky = "W" )
  oval3 = box_led3.create_oval(25,22,55,52, fill = "red")


#########################################################
# Scoreboard():
# FUNCTION FOR UPDATE THE SCOREBOARD WITH SHOT PREDICTED
#########################################################

def Scoreboard():
  global b, d, r
  global flagb, flagd, flagr
  global update_scoreboard1, update_scoreboard2, update_scoreboard3
            
  if flagb: 
    b = b + 1
    flagb = False
                
  if flagd:
    d = d + 1
    flagd = False
                
  if flagr:
    r = r + 1
    flagr = False           
                
  score_b.config(text = b)
  update_scoreboard1 = signal_case1.after(4000, Scoreboard)
            
  score_d.config(text = d)
  update_scoreboard2 = signal_case2.after(4000, Scoreboard)
            
  score_r.config(text = r)
  update_scoreboard3 = signal_case3.after(4000, Scoreboard)


#######################################
# System_Initialization():
# FUNCTION FOR INITIALIZING THE SYSTEM: 
#   > Open serial COM port
#   > Training the classifier
#######################################

def System_Initialization(): 
  global serialPort

  # Connection to Bluetooth HC06, baudrate fixed at 57600 
  serialPort = sr.Serial(port = BT_COM, baudrate=57600) 
  
  # Classifier training
  Classifier_Training()


######################################
# Classifier_Training():
# FUNCTION FOR TRAINING THE CLASSIFIER 
######################################

def Classifier_Training():
  global model_rf
  
  # Import data collected
  df_all = pd.read_csv('training_dataset.csv') #(140,19)

  # Cleaning the dataset, removing infinte and NaN values
  df_all.replace([np.inf, -np.inf], np.nan, inplace=True)
  df_all.dropna(inplace=True)
  df_all = df_all.reset_index(drop=True) #(140,19)

  # Target variable = type of gesture {0,1,2,3}
  y = df_all["label"]

  # New statistics explanatory variables: 1° quantile, median, 3° quantile for each of the 6 IMU measurements 
  X = df_all.drop("label", axis=1) 

  # Split in training & test dataset
  from sklearn.model_selection import train_test_split
  X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                      test_size = 0.30,   
                                                      stratify = y,        
                                                      random_state = 123) 

  # Model fit with Random Forest 
  from sklearn.ensemble import RandomForestClassifier

  # Best hyperparameters according to GridSearchCV
  model_rf = RandomForestClassifier(n_estimators=10, 
                                    criterion='gini', 
                                    max_depth=15, 
                                    min_samples_split=3, 
                                    min_samples_leaf=2)
  # Model fit
  model_rf.fit(X_train, y_train)


#####################################################
# Start_GUI():
# FUNCTION MODIFYING GUI WHEN START BUTTON IS PRESSED:  
#   > Activate clock
#   > Display "Game started"
#   > Switch on LED
#####################################################

def Start_GUI():
  global running
  global acquisition

  if not running:
    Clock()
    running = True 
  
  box_led2 = Canvas(window, bd = 0, bg = "#666699", height = 80, width = 80, highlightthickness= 0)
  box_led2.grid(row = 20, columns = 7, padx = 135, sticky = "W")
  oval2 = box_led2.create_oval(25,22,55,52, fill = "light green")
           
  acquisition = Label(window, text = "GAME STARTED", font = ("Orator Std", 20, 'bold'), fg = "#660033", bg = "#666699")
  acquisition.grid(row = 40, columns = 8, pady = 50, padx = 240, sticky = "w")


#########################################
# Predict_Data_Packet():
# FUNCTION FOR DATA READING & PREDICTION   
#   > Reading 1 packet of data via serial
#   > Data prediction with RF classifier
#   > Update of the GUI
#########################################

def Predict_Data_Packet(): 
  global flagb, flagr, flagd
  global mat_big

  for packets in range(0,n_packets): 

    # Reading 1 packet (with n_frame inside) 
    data = serialPort.read(send_bytes) 

    # Check for header and tail 
    if ((data[0] == 0XA0) and (data[0+(send_bytes-1)] == 0XC0)):

      # For each frame of the packet create the matrix containing the 6 registers' values
      for r in range(0,n_frame): 
        c=0
        for i in range (1,12,2): 
            col = np.float16((data[i+12*(r)]<<8) + data[(i+1)+12*(r)])
            mat[r,c] = col
            c+=1 

      # FSR conversion
      for k in range(0,3):  
        mat[:,k] = mat[:,k]*(4/65535)-2     # +-2 g for accelerometer
      for j in range(3,6): 
        mat[:,j] = mat[:,j]*(500/65535)-250 # +-250 dps for gyroscope

    if (packets == 0):     
      mat_big = mat

    else:
      mat_big = np.concatenate((mat_big,mat), axis=0)

  # Dataframe of the single acquisition (400x6) to be classified
  df = pd.DataFrame(mat_big, 
                    columns = ["ACC_X", "ACC_Y", "ACC_Z", "GYR_X", "GYR_Y", "GYR_Z"])

  # Cleaning the dataframe 
  df.replace([np.inf, -np.inf], np.nan, inplace=True) # Replace infinite updated data with NaN
  df.dropna(inplace=True)                             # Drop rows with NaN
  df = df.reset_index(drop=True)                      # Reset indexes

  # Creating new explanatory variables: 1°, 2°, 3° quantiles
  X_quantiles = np.empty((1,18))

  for i in range(18):
    if (i==0) or (i%3 == 0): Q = 0.25
    if (i==1) or (i==4) or (i==7) or (i==10) or (i==13) or (i==16): Q = 0.5
    if (i==2) or (i==5) or (i==8) or (i==11) or (i==14) or (i==17): Q = 0.75

    if (i<=2):  
      X_quantiles[0,i] = np.quantile(df['ACC_X'],Q)
    if (i>2) and (i<=5):  
      X_quantiles[0,i] = np.quantile(df['ACC_Y'],Q)
    if (i>5) and (i<=8):  
      X_quantiles[0,i] = np.quantile(df['ACC_Z'],Q)
    if (i>8) and (i<=11): 
      X_quantiles[0,i] = np.quantile(df['GYR_X'],Q)
    if (i>11) and (i<=14):  
      X_quantiles[0,i] = np.quantile(df['GYR_Y'],Q)
    if (i>14) and (i<=17):  
      X_quantiles[0,i] = np.quantile(df['GYR_Z'],Q)
  

  # Dataframe of the single acquisition (1x18) to be classified
  df_to_test = pd.DataFrame(X_quantiles, columns = ['ACCX_25', 'ACCX_50','ACCX_75',
                                                    'ACCY_25', 'ACCY_50','ACCY_75',
                                                    'ACCZ_25', 'ACCZ_50','ACCZ_75',
                                                    'GYRX_25', 'GYRX_50','GYRX_75',
                                                    'GYRY_25', 'GYRY_50','GYRY_75',
                                                    'GYRZ_25', 'GYRZ_50','GYRZ_75'])

  # Prediction for the single acquisition made
  shot = model_rf.predict(df_to_test)

  # Update GUI scoreboard
  if (shot == 0): flagd = True
  if (shot == 1): flagr = True
  if (shot == 2): flagb = True
  
  Scoreboard() 


##############################################
# Start_acquisition():
# FUNCTION ENABLING DATA READING & PREDICTION
##############################################

def Start_acquisition():

  flag_start = True

  while(flag_start):
    Predict_Data_Packet()

    if (flag_stop):
      flag_start = False
      break

    if (flag_reset):
      flag_start = False
      break


#----------------------------------------------- GUI CREATION ------------------------------------------------#

# Window
window = Tk()
window.geometry("700x600")
window.title("Section")
window.resizable(False, False)
window.config(background = "#666699")

# Timer
clock_timer = Label(window, text = "00:00:00", bg = "black", fg = "#ffccff", font = ("Helvetica", 30, 'bold'))
clock_timer.grid(row = 20, columns = 400, padx = 500, sticky = "NE", pady = 20)

# Led
box_led = Canvas(window, bd = 0, bg = "#666699", height = 80, width = 80, highlightthickness=0)
box_led.grid(row = 20, columns = 7, padx = 135, sticky = "W")
oval = box_led.create_oval(25,22,55,52, fill="red")

# "Game started" label
acquisition = Label(window, text = "GAME STARTED", font = ("Orator Std", 20, 'bold'), fg = "#666699", bg = "#666699" )
acquisition.grid(row = 40, columns = 8, pady = 50, padx = 160, sticky = "W")

# Buttons
start = Button(window, text = "START", command = Multithreading,  bd= 0, font = ("Orator Std", 20, 'bold'), fg = "#660033")
start.grid(row = 20, column =0, padx = 20, pady = 20, sticky = "NW")

stop = Button(window, text = " STOP ", command = Stop_GUI, bd = 0, font = ("Orator Std", 20, 'bold'), fg = "#660033")
stop.grid(row = 21, column = 0, padx = 20, pady = 5, sticky = "NW")

resets = Button(window, text = "RESET", command = Reset, bd = 0, font = ("Orator Std", 15, 'bold'), fg = "#660033")
resets.grid(row = 21, columns = 400)

com = Button(window, text = "COM", command = System_Initialization, bd = 0, font = ("Orator Std", 15, 'bold'), fg = "#660033")
com.grid(row = 22, columns = 400, padx = 560, pady = 0, sticky = "NW")

# "Serve" scores
signal_case1 = Canvas(window, bg = "#666699", height = 230, width = 186)
signal_case1.grid(row = 42, columns = 7, sticky = "W", padx = 50)
serve = signal_case1.create_text(93,32, text = "SERVE", fill = "#660033", font = ('Orator Std', 20, 'bold'))
b = 0
score_b = Label(signal_case1, bg = "#666699", text = b, fg = "#ffccff", font = ('Helvetica', 80, 'bold'))
score_b.grid(row=42, columns = 7, padx =60, pady = 60)

# "Forehand" scores
signal_case2 = Canvas(window, bd = 0, bg = "#666699", height = 230, width = 186)
signal_case2.grid(row = 42, columns = 8, sticky = "W", padx = 245)
forehand = signal_case2.create_text(93,32, text = "FOREHAND", fill = "#660033", font = ('Orator Std', 20, 'bold'))
d = 0
score_d = Label(signal_case2, bg = "#666699", text = d, fg = "#ffccff", font = ('Helvetica', 80, 'bold'))
score_d.grid(row = 42, columns = 8, padx = 60, pady = 60)

# "Backhand" scores
signal_case3 = Canvas(window, bd = 0, bg = "#666699", height = 230, width = 186)
signal_case3.grid(row = 42, columns = 9, sticky = "W", padx = 438)
backhand = signal_case3.create_text(93,32, text = "BACKHAND", fill = "#660033", font = ('Orator Std', 20, 'bold'))
r = 0
score_r = Label(signal_case3, text = r, bg = "#666699", fg = "#ffccff", font = ('Helvetica', 80, 'bold'))
score_r.grid(row = 42, columns = 9, padx = 60, pady = 60)

window.mainloop()


