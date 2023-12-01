# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 13:28:28 2023

@author: DERECHO
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 13:13:55 2023

@author: DERECHO
"""

import os
import tkinter as tk
import time
import threading
import psutil

# Diccionario para almacenar las ventanas creadas
ventanas = {}

def detectar_usb():
    # Lista de dispositivos disponibles en el sistema
    dispositivos_previos = set(psutil.disk_partitions())

    while True:
        time.sleep(1)
        dispositivos_actuales = set(psutil.disk_partitions())

        # Verificar si hay un nuevo dispositivo conectado
        dispositivo_nuevo = dispositivos_actuales - dispositivos_previos
        dispositivo_nuevo_condicion = len(dispositivos_actuales) - len(dispositivos_previos)
        if dispositivo_nuevo_condicion == 1:
            dispositivo_nuevo = dispositivo_nuevo.pop()
            mostrar_contenido_usb(dispositivo_nuevo)
            dispositivo_nuevo_condicion = 0

        dispositivos_previos = dispositivos_actuales

def mostrar_contenido_usb(dispositivo):
    # Ruta completa al dispositivo
    ruta_dispositivo = os.path.join(dispositivo.device, '')

    # Verificar si ya hay una ventana con el mismo nombre
    if dispositivo.device in ventanas:
        return

    # Lista de archivos en el dispositivo
    archivos = os.listdir(ruta_dispositivo)

    # Crear y mostrar la ventana
    ventana = tk.Tk()
    ventana.title(f'Contenido de {dispositivo.device}')

    mensaje = f'Archivos en {dispositivo.device}:\n\n'
    mensaje += '\n'.join(archivos)

    # Alinea el texto a la izquierda
    etiqueta = tk.Label(ventana, text=mensaje, justify='left', anchor='w')
    etiqueta.pack()

    # Almacena la ventana en el diccionario
    ventanas[dispositivo.device] = ventana

    ventana.mainloop()

# Crear la ventana principal antes de iniciar el hilo
ventana_principal = tk.Tk()

# Iniciar la detección de USB en un hilo separado
hilo_usb = threading.Thread(target=detectar_usb)
hilo_usb.start()

# Mantener el programa principal en ejecución
ventana_principal.mainloop()
