# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 10:58:04 2023

@author: Escritorio
"""

import os
import tkinter as tk
import subprocess
import time
import threading
import psutil
import shutil

directorio_actual = os.getcwd()
directorio = directorio_actual

def ejecutar_snes9x(nombre_archivo):
    ruta_archivo = os.path.join(directorio, nombre_archivo)
    comando = f"-fullscreen snes9x {ruta_archivo}"
    subprocess.run(comando, shell=True)

def cargar_archivos():
    return [archivo for archivo in os.listdir(directorio) if archivo.endswith('.smc')]

def on_seleccion(event):
    widget = event.widget
    seleccionado = widget.get(widget.curselection())
    ejecutar_snes9x(seleccionado)

def salir(event):
    app.destroy()

def detectar_usb():
    dispositivos_previos = set(psutil.disk_partitions())

    while True:
        time.sleep(1)
        dispositivos_actuales = set(psutil.disk_partitions())

        dispositivo_nuevo = dispositivos_actuales - dispositivos_previos
        dispositivo_nuevo_condicion = len(dispositivos_actuales) - len(dispositivos_previos)
        if dispositivo_nuevo_condicion == 1:
            dispositivo_nuevo = dispositivo_nuevo.pop()
            # Mostrar la ventana desde el hilo principal
            app.after(0, lambda: mostrar_contenido_usb(dispositivo_nuevo))
            dispositivo_nuevo_condicion = 0

        dispositivos_previos = dispositivos_actuales

def mostrar_contenido_usb(dispositivo):
    ruta_dispositivo = os.path.join(dispositivo.device, '')
    # Copiar archivos desde la USB al directorio
    app.after(0, lambda: copiar_archivos_smc(ruta_dispositivo))
    
    if dispositivo.device in ventanas:
        return
    
    archivos = [archivo for archivo in os.listdir(ruta_dispositivo) if archivo.endswith('.smc')]
    ventana_usb = tk.Toplevel()
    ventana_usb.overrideredirect(True)

    mensaje = f'Archivos en {dispositivo.device}:\n\n'
    mensaje += '\n'.join(archivos)

    etiqueta = tk.Label(ventana_usb, text=mensaje, justify='left', anchor='w')
    etiqueta.pack()

    ventanas[dispositivo.device] = ventana_usb

    def cerrar_ventana(event):
        ventanas.pop(dispositivo.device, None)
        ventana_usb.destroy()
        actualizar_lista_archivos()

    ventana_usb.bind("<Tab>", cerrar_ventana)

    ventana_usb.update_idletasks()
    ancho_ventana = ventana_usb.winfo_width()
    alto_ventana = ventana_usb.winfo_height()
    x_pantalla = (ventana_usb.winfo_screenwidth() // 2) - (ancho_ventana // 2)
    y_pantalla = (ventana_usb.winfo_screenheight() // 2) - (alto_ventana // 2)
    ventana_usb.geometry('+{}+{}'.format(x_pantalla, y_pantalla))

    ventana_usb.mainloop()

def copiar_archivos_smc(desde_usb, a_directorio=directorio):
    try:
        if not os.path.exists(a_directorio):
            os.makedirs(a_directorio)

        archivos_smc = [archivo for archivo in os.listdir(desde_usb) if archivo.endswith('.smc')]

        for archivo in archivos_smc:
            origen = os.path.join(desde_usb, archivo)
            destino = os.path.join(a_directorio, archivo)
            shutil.copy(origen, destino)
            print(f"Archivo '{archivo}' copiado exitosamente.")
            
    except FileNotFoundError:
        print(f"Error: El directorio '{desde_usb}' no existe.")
    except Exception as e:
        print(f"Error al copiar archivos: {e}")

def actualizar_lista_archivos():
    menu.delete(0, tk.END)
    archivos = cargar_archivos()

    for archivo in archivos:
        menu.insert(tk.END, archivo)

ventanas = {}

archivos = cargar_archivos()

app = tk.Tk()
app.attributes("-fullscreen", True)

menu = tk.Listbox(app, selectbackground="lightblue", bg="white", fg="black", font=("Courier", 14))
menu.pack(side="left", fill="both", expand=True)

for archivo in archivos:
    menu.insert(tk.END, archivo)

menu.bind("<ButtonRelease-1>", on_seleccion)
app.bind("<Escape>", salir)

hilo_usb = threading.Thread(target=detectar_usb)
hilo_usb.start()

app.mainloop()