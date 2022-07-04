#################################### GUI CLASS ####################################

import tkinter as tk
import threading 
import time 
from threading import Thread
from random import randint


TK_SILENCE_DEPRECATION = 1

class GUI():

    def __init__ (self):
        #Thread.__init__(self)

    #inizializzo delle variabili 
        global b, d, r
        global ora, minuto, secondo
        global update_time
        ora, minuto, secondo = 0, 0, 0
        global running 
        running = False
        global window 
        global cronometro
        global clock
        global start_acquisition
        global stop_acquisition 
        global reset 
        global flagb, flagd, flagr
        global punteggio_b, punteggio_r, punteggio_d
        global signal_case1, signal_case2, signal_case3
        global tabellone
        global w 
   

    #creo la window
        window = tk.Tk() 
        window.geometry("600x600")  
        window.title("Section")
        window.resizable(False, False)
        window.config(background = "#666699")

    #creo il cronometro
        cronometro = tk.Label(window, text = "00:00:00", bg = "black", fg = "#ffccff", font = ("Helvetica", 30, 'bold'))
        cronometro.grid(row = 20, columns = 400, padx = 460, sticky = "NE", pady = 20)

    #creo il led

        w = tk.Canvas(window, bd =0, bg = "#666699", height= 80, width = 80, highlightthickness=0)
        w.grid(row = 20, columns = 7, padx = 180, sticky = "W")
        oval = w.create_oval(25,48,55,78, fill = "light green")
        led = w.create_text(40, 35, text = "LED", fill= "#660033", font = ('olivier', 20, 'bold'))

        acquisition = tk.Label(window, text = "GAME STARTED", font = ("Orator Std", 40, 'bold'), fg = "#666699", bg = "#666699")
        acquisition.grid(row = 40, columns =8, pady = 50, padx = 160, sticky = "W")



       

    #funzione clock
        def clock():
            global ora, minuto, secondo

            secondo = secondo + 1

            if secondo == 60:
                minuto += 1 
                secondo = 0 

            if minuto == 60:
                ora += 1 
                minuto = 0 

    
            ora_stringa = f'{ora}' if ora > 9 else f'0{ora}'
            minuto_stringa = f'{minuto}' if minuto > 9 else f'0{minuto}'
            secondo_stringa = f'{secondo}' if secondo > 9 else f'0{secondo}'

            
            cronometro.config(text = ora_stringa + ":" + minuto_stringa + ":" + secondo_stringa)
            global update_time
            update_time = cronometro.after(1000, clock)

    #funzione start_acquisition
        def start_acquisition():

            w.destroy()
        
            global running 
            if not running:
                clock()
                running = True 


            w2 = tk.Canvas(window, bd =0, bg = "#666699", height= 80, width = 80, highlightthickness=0)
            w2.grid(row = 20, columns = 7, padx = 180, sticky = "W")
            oval2 = w2.create_oval(25,48,55,78, fill = "red")
            led2 = w2.create_text(40, 35, text = "LED", fill= "#660033", font = ('Orator Std', 20, 'bold'))
    
            acquisition = tk.Label(window, text = "GAME STARTED", font = ("Orator Std", 40, 'bold'), fg = "#660033", bg = "#666699")
            acquisition.grid(row = 40, columns =8, pady = 10, padx = 160, sticky = "w")


    #funzione stop acquisition
        def stop_acquisition():
    
            global update_time
            global running
            if running:
                cronometro.after_cancel(update_time)
                running = False

            w3 = tk.Canvas(window, bd =0, bg = "#666699", height= 80, width = 80, highlightthickness=0)
            w3.grid(row = 20, columns = 7, padx = 180, sticky = "W")
            oval3 = w3.create_oval(25,48,55,78, fill = "light green")
            led3 = w3.create_text(40, 35, text = "LED", fill= "#660033", font = ('Orator Std', 20, 'bold'))
    
            acquisition = tk.Label(window, text = "GAME STARTED", font = ("Orator Std", 40, 'bold'), fg = "#666699", bg = "#666699")
            acquisition.grid(row = 40, columns =8, pady = 50, padx = 160, sticky = "W")

   
    #funzione reset
        def reset():
            global running 
            if running:

                cronometro.after_cancel(update_time)

            global ora, minuto, secondo 
            ora, minuto, secondo = 0, 0, 0
            cronometro.config(text = "00:00:00")
    
    
    

    #aggiungo i bottoni
        start = tk.Button(text = "START", command = start_acquisition, bd= 0, font = ("Orator Std", 30, 'bold'), fg = "#660033")
        start.grid(row = 20, column =0, padx = 20, pady = 20, sticky = "NW") 

        stop = tk.Button( text = " STOP ", command = stop_acquisition, bd = 0, font = ("Orator Std", 30, 'bold'), fg = "#660033")
        stop.grid(row = 21, column = 0, padx = 20, pady = 5, sticky= "NW")

        reset = tk.Button(text = "RESET", command = reset, bd = 0, font = ("Orator Std", 20, 'bold'), fg = "#660033")
        reset.grid(row = 21, columns = 400)


    #aggiungo le componenti battuta
        signal_case1 = tk.Canvas(window, bg = "#666699", height = 230, width = 186)
        signal_case1.grid(row = 42, columns = 7, sticky = "w", padx = 16)
        battuta = signal_case1.create_text(93,32, text = "BATTUTA", fill = "#660033", font = ('Orator Std', 30, 'bold'))
        b = 0
        stringa_b = f'{b}'
        punteggio_b = tk.Label(signal_case1, bg = "#666699", text = stringa_b, fg = "#ffccff", font = ('Helvetica', 90, 'bold'))
        punteggio_b.grid(row=42, columns = 7, padx =70, pady = 80)


    #aggiungo le componenti dritto
        signal_case2 = tk.Canvas(window, bd = 0, bg = "#666699", height = 230, width = 186)
        signal_case2.grid(row = 42, columns = 8, sticky = "W", padx = 202)
        dritto = signal_case2.create_text(93,32, text = "DRITTO", fill = "#660033", font = ('Orator Std', 30, 'bold'))
        d = 0
        stringa_d = f'{d}'
        punteggio_d = tk.Label(signal_case2, bg = "#666699", text = stringa_d, fg = "#ffccff", font = ('Helvetica', 90, 'bold'))
        punteggio_d.grid(row = 42, columns = 8, padx = 70, pady = 80)

    #aggiungo le componenti dritto
        signal_case3 = tk.Canvas(window, bd = 0, bg = "#666699", height = 230, width = 186)
        signal_case3.grid(row = 42, columns = 9, sticky = "W", padx = 388)
        rovescio = signal_case3.create_text(93,32, text = "ROVESCIO", fill = "#660033", font = ('Orator Std', 30, 'bold'))
        r = 0
        stringa_r = f'{r}'
        punteggio_r = tk.Label(signal_case3, text = stringa_r, bg = "#666699", fg = "#ffccff", font = ('Helvetica', 90, 'bold'))
        punteggio_r.grid(row = 42, columns = 9, padx = 70, pady = 80)


    #aggiungo la funzione tabellone
        def tabellone():
    
            global b, d, r
            stringa_b = f'{b}'
            stringa_d = f'{d}'
            stringa_r = f'{r}'
    
      
            if flagb: 
                b = b + 1
        
            if flagd:
                d = d + 1
        
            if flagr:
                r = r + 1
        
        
            punteggio_b.config(text = stringa_b)
            global update_tabellone1
            update_time1 = signal_case1.after(1000, tabellone)
            flagb = False
    
            punteggio_d.config(text = stringa_d)
            global update_tabellone2
            update_time2 = signal_case2.after(1000, tabellone)
            flagd = False
    
            punteggio_r.config(text = stringa_r)
            global update_tabellone3
            update_time3 = signal_case3.after(1000, tabellone)
            flagr = False
        
       
