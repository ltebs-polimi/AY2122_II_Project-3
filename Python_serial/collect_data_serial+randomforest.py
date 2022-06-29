# Import libraries
from turtle import shape
import numpy as np
import serial as sr
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn
import csv
import glob
import os

#-------------------------------------- COLLECTION OF DATA ------------------------------------


n_packets = 40 #number of packets to send to acquisition_csv_file 
#n_packets = 40 -> 1 SINGLE ACQUISITION
#n_packets = 200 -> 25 s SESSION
#n_packets = 400 -> 50 s SESSION

n_frame = 10 #each packet has n_frame
send_bytes = (12*n_frame)+2 #bytes within 1 packet sent by the BT 
mat = np.zeros(shape=(n_frame,6), dtype=np.float16) #array wtih inside 1 packet of data 

acquisition_file = 'NOME_COGNOME_XX.06.22.csv'
prediction_file = 'NOME_COGNOME_XX.06.22_PREDICTED.csv'

# Connection to Bluetooth HC05 = COM19, baudrate fixed at 57600 
serialPort = sr.Serial(port = "COM19", baudrate=57600) 

# Acquire data of n_packets (should be changed according to button status)
for packets in range(0,n_packets): 

    # Reading 1 packet (with n_frame inside) 
    data=serialPort.read(send_bytes) 

    # FCheck for header and tail 
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
            mat[:,k] = mat[:,k]*(4/65535)-2 # +-2 g for accelerometer
        for j in range(3,6): 
            mat[:,j] = mat[:,j]*(500/65535)-250 # +-250 dps for gyroscope

    if (packets == 0):     
        mat_big = mat
 
    else:
        mat_big = np.concatenate((mat_big,mat), axis=0)


# Creating acquisition_csv_file with the data of n_packets (400x6)
pd.DataFrame(mat_big).to_csv(acquisition_file, 
                            header=["ACC_X", "ACC_Y", "ACC_Z", "GYR_X", "GYR_Y", "GYR_Z"], 
                            index=False)
                            


#--------------------------------- BUILDING THE CLASSSIFIER -----------------------------------------
#---------------------------------- move it into a function -----------------------------------------

# Each dataframe contains 30 acquisition_csv_file, 10 for each shot, acquired with the same protocol (400x7 each)
filepaths_Aurora = [f for f in os.listdir(".") if f.endswith('Aurora.csv')]
df_Aurora = pd.concat(map(pd.read_csv, filepaths_Aurora))
filepaths_Letizia = [f for f in os.listdir(".") if f.startswith('Letizia')]
df_Letizia = pd.concat(map(pd.read_csv, filepaths_Letizia))
filepaths_Natalia = [f for f in os.listdir(".") if f.endswith('Natalia.csv')]
df_Natalia = pd.concat(map(pd.read_csv, filepaths_Natalia))
filepaths_Adelaide = [f for f in os.listdir(".") if f.endswith('Adelaide.csv')]
df_Adelaide = pd.concat(map(pd.read_csv, filepaths_Adelaide))
filepaths_noshot = [f for f in os.listdir(".") if f.endswith('_NOSHOT.csv')]
df_noshot = pd.concat(map(pd.read_csv, filepaths_noshot))

# Cleaning the dataset, removing infinte and NaN values
df_all = pd.concat([df_Aurora, df_Natalia,df_Letizia,df_Adelaide, df_noshot] , axis = 0)
df_all.replace([np.inf, -np.inf], np.nan, inplace=True)
df_all.dropna(inplace=True)
df_all = df_all.reset_index(drop=True) # final shape = (47785, 7)

# Target variable = type of shot {0,1,2,3}
y = df_all["label"]

# Explanatory variables = "ACC_X", "ACC_Y", "ACC_Z", "GYR_X", "GYR_Y", "GYR_Z"
X = df_all.drop("label", axis=1) 


# SPLITTING TRAIN & TEST SET

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size = 0.30,   
                                                    stratify = y,        
                                                    random_state = 123) 


# MODEL FIT WITH RANDOM FOREST 

from sklearn.ensemble import RandomForestClassifier

# best hyperparameters according to GridSearch
model_rf = RandomForestClassifier(n_estimators=30, 
                                  criterion='entropy', 
                                  max_depth=15, 
                                  min_samples_split=5, 
                                  min_samples_leaf=2)

model_rf.fit(X_train, y_train)


#----------------------------------------------- PREDICITONS -----------------------------------

# Dataframe of the single acquisition (#400x6) to classify
df_single_totest = pd.read_csv(acquisition_file) 

# Cleaning the dataframe 
df_single_totest.replace([np.inf, -np.inf], np.nan, inplace=True) # Replace infinite updated data with NaN
df_single_totest.dropna(inplace=True) # Drop rows with NaN
df_single_totest = df_single_totest.reset_index(drop=True) # Reset indeces

# Predictions of the single acquisition made
y_test_pred = model_rf.predict(df_single_totest)

# Creating file with predictions
y_test_pred_col = pd.DataFrame(y_test_pred)
df_single_predictions = pd.concat([df_single_totest, y_test_pred_col] , axis = 1)
df_single_predictions.columns = ['ACC_X','ACC_Y','ACC_Z','GYR_X','GYR_Y','GYR_Z', 'pred']
df_single_predictions.to_csv(prediction_file)

# SHOT PREDICTED during 1 single acquisition 
# most frequent value  
shot = df_single_predictions['pred'].value_counts().idxmax()
# 0 = forehand (DRITTO)
# 1 = backhand (ROVESCIO)
# 2 = serve (BATTUTA)
# 3 = no shot (ALTRO)





