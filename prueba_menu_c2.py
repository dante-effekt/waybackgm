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
import pyudev
import subprocess as sp

directorio_actual = os.getcwd()
directorio = directorio_actual
usb = 0  # Flag para saber si hay una USB conectada
dispositivo = 0  # Mutará de int a objeto device cuando se inserte una USB

def ejecutar_snes9x(nombre_archivo):
    ruta_archivo = os.path.join(directorio, nombre_archivo)
    comando = f"/home/fipy/Documents/snes9x-1.60/gtk/build/snes9x-gtk {ruta_archivo}"
    subprocess.run(comando, shell=True)

def cargar_archivos():
    return [archivo for archivo in os.listdir(directorio) if archivo.endswith('.smc')]

def on_seleccion(event):
    widget = event.widget
    seleccionado = widget.get(widget.curselection())
    ejecutar_snes9x(seleccionado)

def salir(event):
    app.destroy()


#Definimos las funciones necesarias para detectar la USB
def dev_stats(path):
    photos = []
    for file in os.listdir(path):
        if file.endswith(".jpg") \
        or file.endswith(".png"):
            photos.append(path+"/"+file)
    print("{} has {} photos.".format(path, len(photos)))
    return photos


def print_dev_info(device):
    print("Device sys_path: {}".format(device.sys_path))
    print("Device sys_name: {}".format(device.sys_name))
    print("Device sys_number: {}".format(device.sys_number))
    print("Device subsystem: {}".format(device.subsystem))
    print("Device device_type: {}".format(device.device_type))
    print("Device is_initialized: {}".format(device.is_initialized))


def auto_mount(path):
    args = ["udisksctl", "mount", "-b", path]
    sp.run(args)


def get_mount_point(path):
    args = ["findmnt", "-unl", "-S", path]
    cp = sp.run(args, capture_output=True, text=True)
    out = cp.stdout.split(" ")[0]
    return out


def check_dev_events(action, device): #Funcion manejadora de eventos
    global usb
    global dispositivo
    if (action == "add"): #Si se añade una usb
        usb = 1
        print_dev_info(device)
        dispositivo = device #Pasar el objeto dispositivo a la variable global
    if (action == "remove"): #Si se retira una usb
        usb = 0

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem="block", device_type="partition")        
observer = pyudev.MonitorObserver(monitor, check_dev_events, name='monitor-observer')
observer.daemon #MonitorObserver sera un hilo demonio
observer.start()


def detectar_usb():
    global dispositivo
    while True:
        if (usb==0):
            print("NO se ha ingresado un usb")
            time.sleep(1)
        if (usb==1):
            usb_nuevo = get_mount_point("/dev/" + dispositivo.sys_name)
            print("La ruta del dispositivo es: " + usb_nuevo)
            mostrar_contenido_usb(usb_nuevo)


def mostrar_contenido_usb(ruta_dispositivo):
    global dispositivo
    #ruta_dispositivo = os.path.join(dispositivo, ruta_dispositivo)
    # Copiar archivos desde la USB al directorio
    app.after(0, lambda: copiar_archivos_smc(ruta_dispositivo))
    
    if dispositivo in ventanas:
        return
    
    print("La ruta del dispositivo es: " + ruta_dispositivo)
    archivos = [archivo for archivo in os.listdir(ruta_dispositivo) if archivo.endswith('.smc')]
    ventana_usb = tk.Toplevel()
    ventana_usb.overrideredirect(True)

    mensaje = f'Archivos en {dispositivo}:\n\n'
    mensaje += '\n'.join(archivos)

    etiqueta = tk.Label(ventana_usb, text=mensaje, justify='left', anchor='w')
    etiqueta.pack()

    ventanas[dispositivo] = ventana_usb

    def cerrar_ventana(event):
        ventanas.pop(dispositivo, None)
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
hilo_usb.daemon
hilo_usb.start()

app.mainloop()
