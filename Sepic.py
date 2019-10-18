#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCHIVO: sepic.py
Autor: Ing. Mauro Maldonado
Fecha: 31/07/2019
Descripción: Este módulo contiene solo la GUI
"""

import tkinter as tk
from tkinter import ttk
import conexion
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('Ensayo de Paneles Solares')
        self.config(width=1366, height=768)
        self.crea_widgets()
    
    def crea_widgets(self):
        self.tab_control = ttk.Notebook(self.master)
        self.pestaña1 = ttk.Frame(self.tab_control)
        self.pestaña2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.pestaña1, text='Ensayo')
        self.tab_control.add(self.pestaña2, text='Configuración')
        self.tab_control.pack(expand=1, fill='both')

        self.marco_elec = ttk.Frame(self.pestaña1)
        self.marco_elec.config(width=500, height=300, relief=tk.GROOVE, borderwidth=2)
        self.marco_elec.grid(row=0, column=0, sticky=tk.N)
        self.marco_elec.grid_anchor()
        self.lbl_elec = tk.Label(self.marco_elec, text="Características Eléctricas Estándar")
        self.lbl_elec.config(relief=tk.GROOVE, borderwidth=2, bg='paleturquoise')
        self.lbl_Voc = tk.Label(self.marco_elec, text="Tensión a Ciruito Abierto (Voc)")
        self.tension_voc = tk.Label(self.marco_elec, text="-,--", bg='white')
        self.uni_voc = tk.Label(self.marco_elec, text="(V)")
        self.lbl_vmp = tk.Label(self.marco_elec, text="Tensión Óptima de Operación (Vmp)")
        self.tension_vmp = tk.Label(self.marco_elec, text="-,--", bg='white')
        self.uni_vmp = tk.Label(self.marco_elec, text="(V)")
        self.lbl_icc = tk.Label(self.marco_elec, text="Corriente de Corto Circuito (Isc)")
        self.corriente_icc = tk.Label(self.marco_elec, text="-,--", bg='white')
        self.uni_icc = tk.Label(self.marco_elec, text="(A)")
        self.lbl_imp = tk.Label(self.marco_elec, text="Corriente Óptima de Operación (Imp)")
        self.corriente_imp = tk.Label(self.marco_elec, text="-,--", bg='white')
        self.uni_imp = tk.Label(self.marco_elec, text="(A)")
        self.lbl_pmax = tk.Label(self.marco_elec, text="Potencia Máxima (Pmax)")
        self.potencia_pmax = tk.Label(self.marco_elec, text="-,--", bg='white')
        self.uni_pmax = tk.Label(self.marco_elec, text="(Wp)")

        self.lbl_elec.grid(row=0, column=0, columnspan=3)
        
        self.lbl_Voc.grid(row=1, column=0, sticky=tk.W)
        self.tension_voc.grid(row=1, column=1)
        self.uni_voc.grid(row=1, column=2)
        
        self.lbl_vmp.grid(row=2, column=0, sticky=tk.W)
        self.tension_vmp.grid(row=2, column=1)        
        self.uni_vmp.grid(row=2, column=2)
        
        self.lbl_icc.grid(row=3, column=0, sticky=tk.W)
        self.corriente_icc.grid(row=3, column=1)
        self.uni_icc.grid(row=3, column=2)
        
        self.lbl_imp.grid(row=4, column=0, sticky=tk.W)
        self.corriente_imp.grid(row=4, column=1)
        self.uni_imp.grid(row=4, column=2)
        
        self.lbl_pmax.grid(row=5, column=0, sticky=tk.W)
        self.potencia_pmax.grid(row=5, column=1)
        self.uni_pmax.grid(row=5, column=2)

        self.lbl_temperatura = tk.Label(self.marco_elec, text="Coeficientes de Temperatura")
        self.lbl_temperatura.config(relief=tk.GROOVE, borderwidth=2, bg='lightgreen')
        self.lbl_temperatura.grid(row=6, column=0, columnspan=3)

        self.lbl_beta = tk.Label(self.marco_elec, text="Coeficiente de Temperatura de Voc")
        self.txt_beta = tk.Label(self.marco_elec, text="-,--",bg='white')
        self.uni_beta = tk.Label(self.marco_elec, text="(%/ºC)")
        self.lbl_alfa = tk.Label(self.marco_elec, text="Coeficiente de Temperatura de Isc")
        self.txt_alfa = tk.Label(self.marco_elec, text="-,--", bg='white')
        self.uni_alfa = tk.Label(self.marco_elec, text="(%/ºC)")
        self.lbl_beta.grid(row=7, column=0, sticky=tk.W)
        self.txt_beta.grid(row=7, column=1)
        self.uni_beta.grid(row=7, column=2)
        self.lbl_alfa.grid(row=8, column=0, sticky=tk.W)
        self.txt_alfa.grid(row=8, column=1)
        self.uni_alfa.grid(row=8, column=2)

        self.lbl_sel_ensayo = tk.Label(self.marco_elec, text="Selección de ensayo")
        self.lbl_sel_ensayo.config(relief=tk.GROOVE, borderwidth=2, bg='white')
        self.lbl_sel_ensayo.grid(row=9, column=0, columnspan=3)

        self.selected = tk.IntVar()
        self.radio3 = tk.Radiobutton(self.marco_elec,text='Paramentros normalizados a partir de ensayos anteriores',variable=self.selected, value=3, command=lambda: conexion.selector(self))
        self.radio3.grid(row=10, column=0, sticky=tk.W)
        
        self.radio1 = tk.Radiobutton(self.marco_elec,text='Paramentros normalizados a partir de ensayo', variable=self.selected, value=1, command=lambda: conexion.selector(self))
        self.radio1.grid(row=11, column=0, sticky=tk.W)

        self.radio2 = tk.Radiobutton(self.marco_elec,text='Paramentros normalizados a partir de catalogo',variable=self.selected, value=2, command=lambda: conexion.selector(self))
        self.radio2.grid(row=12, column=0, sticky=tk.W)

        alfa_cat = tk.DoubleVar()
        self.lbl_alfa_cat = tk.Label(self.marco_elec, text="Alfa de catalogo (1/°C): ")
        self.val_alfa_cat = tk.Entry(self.marco_elec, textvariable=alfa_cat, bg='white')
        self.lbl_alfa_cat.grid(row=13, column=0)
        self.val_alfa_cat.grid(row=13, column=1)

        beta_cat = tk.DoubleVar()
        self.lbl_beta_cat = tk.Label(self.marco_elec, text="Beta de catalogo (1/°C): ")
        self.val_beta_cat = tk.Entry(self.marco_elec, textvariable=beta_cat, bg='white')
        self.lbl_beta_cat.grid(row=14, column=0)
        self.val_beta_cat.grid(row=14, column=1)

        self.boton_conectar = tk.Button(self.pestaña1, text="Conectar", command=lambda: conexion.btn_conectar(self))
        self.boton_conectar.grid(row=1, column=0, sticky=tk.SW)
        self.boton_iniciar = tk.Button(self.pestaña1, text="Iniciar", command=lambda:conexion.btn_iniciar(self))
        self.boton_iniciar.grid(row=1, column=0, sticky=tk.SE)

        #Dibuja ek marco para el grafico P-V
        self.marco_PV = tk.Frame(self.pestaña1)
        self.marco_PV.config(width=600, height=225, bg='white', borderwidth=2)
        self.marco_PV.config(relief='ridge')   # relieve del frame hundido
        self.marco_PV.grid(row=0, column=1)

        #Dibuja ek marco para el grafico I-V
        self.marco_IV=tk.Frame(self.pestaña1)
        self.marco_IV.config(width=600, height=225, bg='white', borderwidth=2)
        self.marco_IV.config(relief='sunken')   # relieve del frame hundido
        self.marco_IV.grid(row=1, column=1)
        
#--------------------Creo la primera figura para la grafica---------------------------------
        self.fig1 = Figure(figsize=(6,2.25), dpi=100)
        self.AX = self.fig1.add_subplot(111)
        self.AX.set_ylabel('Corriente (A)')
        self.AX.set_xlabel('Tension (V)')
        
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.marco_IV)  # CREAR AREA DE DIBUJO DE TKINTER.
        self.canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#-----------------------AÑADIR BARRA DE HERRAMIENTAS--------------------------
        toolbar = NavigationToolbar2Tk(self.canvas1, self.marco_IV)# barra de iconos
        toolbar.update()
        self.canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#--------------------Creo la segunda figura para la grafica---------------------------------
        self.fig2 = Figure(figsize=(6,2.25), dpi=100)
        self.AY = self.fig2.add_subplot(111)
        self.AY.set_ylabel('Potencia (W)')
        self.AY.set_xlabel('Tension (V)')
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.marco_PV)  # CREAR AREA DE DIBUJO DE TKINTER.
        self.canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#-----------------------AÑADIR BARRA DE HERRAMIENTAS--------------------------
        toolbar = NavigationToolbar2Tk(self.canvas2, self.marco_PV)# barra de iconos
        toolbar.update()
        self.canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#________Segunda pestaña____________________________________________________________________

        self.marco_config = ttk.Frame(self.pestaña2)
        self.marco_config.config(width=500, height=300, relief=tk.GROOVE, borderwidth=2)
        self.marco_config.grid(row=0, column=0, sticky=tk.N)
        self.marco_config.grid_anchor()

        self.lbl_config = tk.Label(self.marco_config, text="Características Eléctricas Estándar")
        self.lbl_config.config(relief=tk.GROOVE, borderwidth=2, bg='paleturquoise')
        self.lbl_config.grid(row=0, column=0, columnspan=2)

        global HR40002
        HR40002 = tk.IntVar()
        self.lbl_HR40002 = tk.Label(self.marco_config, text="Cantidad de muestras antes de guardar los valores (HR2): ")
        self.val_HR40002 = tk.Entry(self.marco_config, textvariable=HR40002, bg='white')
        self.lbl_HR40002.grid(row=1, column=0, sticky=tk.W)
        self.val_HR40002.grid(row=1, column=1)

        HR40003 = tk.IntVar()
        self.lbl_HR40003 = tk.Label(self.marco_config, text="Cantidad de muestras tomadas de V e I (HR3): ")
        self.val_HR40003 = tk.Entry(self.marco_config, textvariable=HR40003, bg='white')
        self.lbl_HR40003.grid(row=2, column=0, sticky=tk.W)
        self.val_HR40003.grid(row=2, column=1)

        HR40004 = tk.IntVar()
        self.lbl_HR40004 = tk.Label(self.marco_config, text="(HR4) - Tiempo de espera (HH:MM:SS): ")
        self.val_HR40004 = tk.Entry(self.marco_config, textvariable=HR40004, bg='white')
        self.lbl_HR40004.grid(row=3, column=0, sticky=tk.W)
        self.val_HR40004.grid(row=3, column=1)

        HR40006 = tk.IntVar()
        self.lbl_HR40006 = tk.Label(self.marco_config, text="(HR6) - Delta de Temperatura (°C): ")
        self.val_HR40006 = tk.Entry(self.marco_config, textvariable=HR40006, bg='white')
        self.lbl_HR40006.grid(row=5, column=0, sticky=tk.W)
        self.val_HR40006.grid(row=5, column=1)

        self.boton_escribir = tk.Button(self.pestaña2, text="Escribir Registros", command=lambda: conexion.btn_escribir(self))
        self.boton_escribir.grid(row=6, column=0, sticky=tk.SW)
        self.boton_leer = tk.Button(self.pestaña2, text="Leer Registros", command=lambda: conexion.btn_leer(self))
        self.boton_leer.grid(row=6, column=0, sticky=tk.SE)
