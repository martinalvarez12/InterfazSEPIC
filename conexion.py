#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCHIVO: conexion.py
Autor: Ing. Mauro Maldonado
Fecha: 31/07/2019
Descripción: Este módulo sólo las funciones a ejecutar
"""
import minimalmodbus
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import scipy.io
import threading 
import time
import datetime
import serial

def btn_conectar(gui):
    global modbus
    
    if portIsUsable('COM3') == True:
        modbus = minimalmodbus.Instrument('COM3', 1,mode='rtu')
        modbus.serial.baudrate  = 9600
        modbus.serial.bytesize  = 8
        modbus.serial.parity=minimalmodbus.serial.PARITY_NONE
        modbus.serial.stopbits  = 1
        modbus.serial.timeout   = 5
        if modbus.serial.is_open == False:
            modbus.serial.open()
        gui.boton_conectar.config(text="Conectado")
    else:
        modbus.serial.close()
        gui.boton_conectar.config(text="Conectar")
        return

def portIsUsable(portName):
    try:
       serial.Serial(port=portName)
       return True
    except:
       return False

def btn_iniciar(gui):
    
    if gui.selected.get() == 1:
        if portIsUsable('COM3') == True:
            if messagebox.askyesno('Alerta', 'Puerto COM desconectado, ¿Conectar?'):
                btn_conectar(gui)
            else:
                return
            
        modbus.write_bit(0, 1, functioncode=5)    

    elif gui.selected.get() == 2:
        if portIsUsable('COM3') == True:
            if messagebox.askyesno('Alerta', 'Puerto COM desconectado, ¿Conectar?'):
                btn_conectar(gui)
            else:
                return

        if gui.val_alfa_cat.get() == 0:
            messagebox.showerror(message="No cargaron valores de ALFA y BETA", title="Error")  
            return
        
        modbus.write_bit(0, 1, functioncode=5)    
        
        if gui.selected.get() == 1:
            modbus.write_bit(1, 1, functioncode=5) 
           
        while modbus.read_bit(0, functioncode=1) == 1:
            time.sleep(2)
            continue

    elif gui.selected.get() == 3:
        pass
    else:
        return


    
    btn_plot(gui)

def btn_escribir(gui):
    if portIsUsable('COM3') == True:
        if messagebox.askyesno('Alerta', 'Puerto COM desconectado, ¿Conectar?'):
            btn_conectar(gui)
        else:
            return

    modbus.write_register(2, np.int(gui.val_HR40002.get()), numberOfDecimals=0, functioncode=16, signed=False)
    modbus.write_register(3, np.int(gui.val_HR40003.get()), numberOfDecimals=0, functioncode=16, signed=False)
    tiempo =  datetime.datetime.strptime(np.str(gui.val_HR40004.get()),'%H:%M:%S')
    x = time.strptime(tiempo.strftime('%H:%M:%S').split(',')[0],'%H:%M:%S')
    tiempo2 = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()*1000
    a = int(tiempo2)>>8
    b = (int(tiempo2))- (a<<8)
    modbus.write_register(4, b, numberOfDecimals=0, functioncode=16, signed=False)
    modbus.write_register(5, a, numberOfDecimals=0, functioncode=16, signed=False)
    modbus.write_register(6, int(np.float(gui.val_HR40006.get())) *3276/9.99, numberOfDecimals=0, functioncode=16, signed=False)

def btn_leer(gui):
    
    if portIsUsable('COM3') == True:
        if messagebox.askyesno('Alerta', 'Puerto COM desconectado, ¿Conectar?'):
            btn_conectar(gui)
        else:
            return

    gui.val_HR40002.delete(0,tk.END)
    gui.val_HR40003.delete(0,tk.END)
    gui.val_HR40004.delete(0,tk.END)
    gui.val_HR40006.delete(0,tk.END)

    gui.val_HR40002.insert(0, modbus.read_register(2, numberOfDecimals=0, functioncode=3, signed=False))
    gui.val_HR40003.insert(0, modbus.read_register(3, numberOfDecimals=0, functioncode=3, signed=False))
    
    LS = modbus.read_register(4, numberOfDecimals=0, functioncode=3, signed=False)
    MS = modbus.read_register(5, numberOfDecimals=0, functioncode=3, signed=False)
    Delta =  (((MS<<16)+LS)/modbus.read_register(1, numberOfDecimals=0, functioncode=3, signed=False)) / 1000  
    delta_ms = time.strftime('%H:%M:%S', time.gmtime(Delta))
    gui.val_HR40004.insert(0, delta_ms)
    gui.val_HR40006.insert(0, (modbus.read_register(6, numberOfDecimals=0, functioncode=3, signed=False)*100/32767))

def selector(gui):
    if  (gui.selected.get() == 1) or ( gui.selected.get() == 3):
        gui.val_alfa_cat.config(state='disabled')
        gui.val_beta_cat.config(state='disabled')
    elif    (gui.selected.get() == 2):  
        gui.val_alfa_cat.config(state='normal')
        gui.val_beta_cat.config(state='normal')   
    else:
        pass 

def btn_plot(gui):
    
    if gui.selected.get() == 1:
        Muestras = modbus.read_register(3, numberOfDecimals=0, functioncode=3, signed=False)
        Mtotal = Muestras*8
        V1      = np.multiply(modbus.read_registers(0, Muestras, functioncode=4),np.divide(66,32767))
        I1      = np.multiply(modbus.read_registers(Muestras, Muestras, functioncode=4),np.divide(10.97,32767))
        T1      = np.multiply(modbus.read_registers(Muestras*2, Muestras, functioncode=4),np.divide(110,32767))
        R1      = np.multiply(modbus.read_registers(Muestras*3, Muestras, functioncode=4),np.divide(1159,32767)) 
        Voc1    = V1[0]
        Isc1    = np.multiply(modbus.read_register((Mtotal + 1), numberOfDecimals=0, functioncode=4, signed=False),np.divide(10.97,32767)) 
        Temp1   = np.multiply(modbus.read_register((Mtotal + 2), numberOfDecimals=0, functioncode=4, signed=False),np.divide(110,32767)) 
        Rad1    = np.multiply(modbus.read_register((Mtotal + 3), numberOfDecimals=0, functioncode=4, signed=False),np.divide(1159,32767)) 
        V2      = np.multiply(modbus.read_registers(Muestras*4, Muestras, functioncode=4),np.divide(66,32767))  
        I2      = np.multiply(modbus.read_registers(Muestras*5, Muestras, functioncode=4),np.divide(10.97,32767))
        T2      = np.multiply(modbus.read_registers(Muestras*6, Muestras, functioncode=4),np.divide(110,32767))
        R2      = np.multiply(modbus.read_registers(Muestras*7, Muestras, functioncode=4),np.divide(1159,32767))    
        Voc2    = V2[0]
        Isc2    = I2[0]#np.multiply(modbus.read_register((Mtotal + 5), numberOfDecimals=0, functioncode=4, signed=False),np.divide(10.97,32767)) 
        Temp2   = T2[0] #np.multiply(modbus.read_register((Mtotal + 6), numberOfDecimals=0, functioncode=4, signed=False),np.divide(110,32767)) 
        Rad2    = R2[0]#np.multiply(modbus.read_register((Mtotal + 7), numberOfDecimals=0, functioncode=4, signed=False),np.divide(1159,32767)) 
        alfa    = 0.00001 #((Isc2/Isc1)*(Rad1/Rad2)-1)/(Temp2 - Temp1)  #0.00037
        beta    =  ((Voc2/Voc1)-1)/(Temp2 - Temp1)                          #-0.0034

    elif gui.selected.get() == 2:
        Muestras = modbus.read_register(3, numberOfDecimals=0, functioncode=3, signed=False)
        Mtotal = Muestras*8
        V1      = np.multiply(modbus.read_registers(0, Muestras, functioncode=4),np.divide(66,32767))
        I1      = np.multiply(modbus.read_registers(Muestras, Muestras, functioncode=4),np.divide(10.97,32767))
        T1      = np.multiply(modbus.read_registers(Muestras*2, Muestras, functioncode=4),np.divide(110,32767))
        R1      = np.multiply(modbus.read_registers(Muestras*3, Muestras, functioncode=4),np.divide(1159,32767)) 
        Voc1    = V1[0]
        Isc1    = I1[Muestras - 1]
        Temp1   = T1[Muestras - 1]
        Rad1    = R1[Muestras - 1]
        alfa    = np.float(gui.val_alfa_cat.get())
        beta    = np.float(gui.val_beta_cat.get())
    
    elif gui.selected.get() == 3:
        mat = scipy.io.loadmat(askopenfilename(filetypes = (("Matlab files","*.mat"),("all files","*.*"))))
        Muestras = 40       
    
        V1      = mat['Tension1']
        V1      = V1[0]
        I1      = mat['Corriente1']
        I1      = I1[0]
        T1      = mat['Temperatura1'] 
        R1      = mat['Radiacion1']
        Voc1    = V1[0]
        Isc1    = I1[Muestras-1]
        Temp1   = T1[0][0]
        Rad1    = R1[0][0]
    
        V2      = mat['Tension2']  
        V2      = V2[0]     
        I2      = mat['Corriente2']     
        I2      = I2[0]
        T2      = mat['Temperatura2']
        R2      = mat['Radiacion2']    
        Voc2    = V2[0]
        Isc2    = I2[Muestras - 1]
        Temp2   = T2[0][0]
        Rad2    = R2[0][0]
        alfa    = ((Isc2/Isc1)*(Rad1/Rad2)-1)/(Temp2 - Temp1)  #0.00037    #0.00001
        beta    =  ((Voc2/Voc1)-1)/(Temp2 - Temp1)                          #-0.0034

    else:
        pass
        
    In = (I1*1000/Rad1)*(1/(1+(alfa*(Temp1-25))))
    Vn = V1 / (1+(beta*(Temp1-25)))
    Pn = In*Vn

    Iscn    = In[Muestras-1] 
    Vocn    = Vn[0]
    Pmaxn   = np.amax(Pn)
        
    x = np.where(Pn==Pmaxn)
    Vmaxpn  = np.float64(Vn[x[0]])
    Imaxpn  = np.float64(In[x[0]])
    
    if (gui.selected.get() == 1) or  (gui.selected.get() == 2):
        nombre = datetime.datetime.now().strftime('%d-%m-%y__%H.%M')
        scipy.io.savemat(  'Ensayo_' + nombre + '.mat', {'V1': V1,'I1': I1,'T1': T1,'R1': R1, 'Voc1': Voc1,'Isc1': Isc1,'Temp1': Temp1,'Rad1': Rad1,
                                                     'Vn': Vn,'In': In,'Pn': Pn,'Iscn': Iscn,'Vocn': Vocn,'Pmaxn': Pmaxn,'Vmaxpn': Vmaxpn,'Imaxpn': Imaxpn})
    else:
        pass

#------------------------------CREAR GRAFICA-------------------------------

    gui.AX.clear()          #Limpio Grafica
    gui.AX.plot(Vn,In)      #Asigno vectores
    gui.AX.axes.grid(True)  #Creo Grilla    
    gui.canvas1.draw()      #Dibujo
    gui.AY.clear()
    gui.AY.plot(Vn,Pn)      #AÑADIR "subbplot"
    gui.AY.axes.grid(True)
    gui.canvas2.draw()

    gui.txt_alfa.config(text=(alfa*100))#.__round__(decimals=4))
    gui.txt_beta.config(text=(beta*100))#.__round__(decimals=4))
    gui.tension_voc.config(text=(Vocn))     #.round(decimals=3)))
    gui.corriente_icc.config(text=(Iscn))   #.round(decimals=3)))
    gui.potencia_pmax.config(text=(Pmaxn))  #.round(decimals=3)))
    gui.tension_vmp.config(text=(Vmaxpn))   #.__round__(decimals=3)))
    gui.corriente_imp.config(text=(Imaxpn)) #.__round__(decimals=3)))