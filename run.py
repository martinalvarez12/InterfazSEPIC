#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCHIVO: run.py
Autor: Ing. Mauro Maldonado
Fecha: 31/07/2019
Descripción: Este archivo lanza el programa
"""
import tkinter as tk
import Sepic

root = tk.Tk()
app = Sepic.Application(master=root)


app.mainloop()