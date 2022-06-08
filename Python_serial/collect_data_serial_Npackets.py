from turtle import shape
import numpy as np
import serial as sr
import pandas as pd
import csv 

n_packets = 40 #numero di pacchetti da mandare (ciascuno con 10 frame)
mat = np.zeros(shape=(10,6), dtype=np.float16) #array con dentro 1 pacchetto di dati

label = np.full(shape=(n_packets*10,1), fill_value = 2) #colonna label per il file csv
# 0 = DRITTO
# 1 = ROVESCIO 
# 2 = BATTUTA

#connessione a Bluetooth HC05 = COM19 (o UART_Debug = COM17)
serialPort = sr.Serial(port = "COM17", baudrate=57600) 


for packets in range(0,n_packets):

    #lettura di 1 pacchetto (con 10 frame)
    data=serialPort.read(122) 

    #controllo header e tail per ogni pacchetto
    if ((data[0] == 0XA0) and (data[0+121] == 0XC0)):

        for r in range(0,10): #per ogni frame nel pacchetto (tot 10)
            c=0
            for i in range (1,12,2): 
                col = np.float16((data[i+12*(r)]<<8) + data[(i+1)+12*(r)])
                mat[r,c] = col
                c+=1 

        #conversione FSR
        for k in range(0,3):  
            mat[:,k] = mat[:,k]*(4/65535)-2 # +-2 g
        for j in range(3,6): 
            mat[:,j] = mat[:,j]*(500/65535)-250 # +-250 dps

    if (packets == 0):     
        mat_big = mat

        
    else:
        mat_big = np.concatenate((mat_big,mat), axis=0)

#aggiunta 7° colonna per la label 
mat_big = np.concatenate([mat_big,label], axis=1)


pd.DataFrame(mat_big).to_csv('nome_cognome_data_LABEL=2.csv', 
                            header=["ACC_X", "ACC_Y", "ACC_Z", "GYR_X", "GYR_Y", "GYR_Z", "label"], 
                            index=False)


#if (flag_ready):
    #serialPort.reset_input_buffer()
    #flag_ready = 0

#organizing the data collected -> TO DO