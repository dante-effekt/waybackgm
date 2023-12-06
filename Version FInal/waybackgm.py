#!/usr/bin/python3
# -*- coding: utf-8 -*-
# waybackgm.py
#
# Authors: Arguello León Dante Moisés, Caballero Hernández Juan Daniel, Jimenez García Rodrigo Gaudencio
# Date: 2023.11.16
# License: MIT
#
# WaybackGM allows you to use a Raspberry Pi as a retro console that uses the open source emulator 
# Snes9x, this program allows you to display a graphical interface with your available roms, detect 
# the presence of USB devices with new games and copy them. It also allows you to restart or turn off 
# your console. 
# It allows you to control the graphical interface through a PS3 controller using the xboxdrv module.

#=============================================================================
#================================MODULOS NECESARIOS===========================
#=============================================================================
import tkinter as tk
from tkinter import PhotoImage
import subprocess as sp
import time
import threading
import psutil
import shutil
import os
import pyudev
from evdev import InputDevice, ecodes
import evdev
import pyautogui
import sys
from PIL import Image, ImageTk

global anchoVentana
global altoVentana
# Permite el rapido movimiento del cursor
pyautogui.FAILSAFE = False

# Vamos a obtener el directorio actual del archivo menu.py
#directorio_actual = os.getcwd()
directorio_actual = "/home/fipy/Documents/Pruebas"
directorio = directorio_actual
usb = 0
dispositivo = 0
#directorio_usb = '/media/fipy/SAMSUNG USB'


# Busca el dispositivo de entrada del joystick
joystick = None

for device in [InputDevice(fn) for fn in evdev.list_devices()]:
    #capabilities = device.capabilities(verbose=True)
    if evdev.ecodes.EV_ABS in device.capabilities():
        joystick = device
        break

if joystick:
    print(f"Joystick detectado: {joystick.name}")
else:
    print("No se encontró un joystick.")
    sys.exit(1)


def ejecutar_snes9x(nombre_archivo):
    ruta_archivo = os.path.join(directorio, nombre_archivo)
    #comando = f"/home/fipy/Documents/snes9x-1.60/gtk/build/snes9x-gtk {ruta_archivo}"
    comando = f'/home/fipy/Documents/snes9x-1.60/gtk/build/snes9x-gtk "{ruta_archivo}"'  
    sp.run(comando, shell=True)

def cargar_archivos():
    return sorted([archivo for archivo in os.listdir(directorio) if (archivo.endswith('.smc') or archivo.endswith('.sfc'))])

def on_tecla_arriba():
    selected_index = menu.curselection()
    if selected_index:
        new_index = selected_index[0] - 1
        menu.selection_clear(0, tk.END)  # Limpiar la selección actual
        menu.selection_set(new_index)    # Establecer nueva selección
        menu.see(new_index)              # Hacer visible el nuevo ítem si está fuera de la vista

def on_tecla_abajo():
    selected_index = menu.curselection()
    if selected_index and selected_index[0] < menu.size() - 1:
        new_index = selected_index[0] + 1
        menu.selection_clear(0, tk.END)
        menu.selection_set(new_index)
        menu.see(new_index)


def on_seleccion(event):
    widget = event.widget
    seleccionado = widget.get(widget.curselection())
    ejecutar_snes9x(seleccionado)


def on_clic_izquierdo():
    selected_index = menu.curselection()
    if selected_index:
        seleccionado = menu.get(selected_index[0])
        ejecutar_snes9x(seleccionado)

def apagar():
    os.system("shutdown now")

def reiniciar():
    os.system("reboot")

def salir(event):
    app.destroy()
    sys.exit(0)

def joystick_control():
    # Lógica para controlar el menú con el joystick izquierdo
    #pyautogui.moveTo(-10,y)
    y = 20
    x = 0
    global anchoVentana
    global altoVentana
    for event in joystick.read_loop():
        if event.type == ecodes.EV_ABS and event.code == 17:
            y += 20 if event.value == 1 else -20
            print('cruz abajo' if event.value == 1 else 'cruz arriba')
            pyautogui.moveTo(x, y)
            print(pyautogui.position())
        elif event.type == ecodes.EV_ABS and event.code == 16:
            if event.value == 1:
                x = max(1, x - 60)
                print('cruz izquierda')
            elif event.value == -1:
                x = min(anchoVentana - 30, x + 60)
                print('cruz derecha')
            pyautogui.moveTo(x, y)
            print(pyautogui.position())
        elif event.type == ecodes.EV_KEY and event.code == 545 and event.value == 1:
            y += 20
            print('cruz abajo')
            pyautogui.moveTo(x, y)
            print(pyautogui.position())
        elif event.type == ecodes.EV_KEY and event.code == 311 and event.value == 1:
            print('BOTON DERECHO/CLICK DERECHO')
            pyautogui.rightClick()
        elif event.type == ecodes.EV_KEY and event.code == 310 and event.value == 1:
            print('BOTON IZQUIERDO/CLICK IZQUIERDO')
            pyautogui.click()
        elif event.type == ecodes.EV_KEY and event.code == 544 and event.value == 1:
            y -= 20
            print('cruz arriba')
            pyautogui.moveTo(x, y)
            print(pyautogui.position())
        elif event.type == ecodes.EV_KEY and event.code == 546 and event.value == 1:
            x = max(1, x - 60)
            print('cruz izquierda')
            pyautogui.moveTo(x, y)
            print(pyautogui.position())
        elif event.type == ecodes.EV_KEY and event.code == 547 and event.value == 1:
            x = min(anchoVentana - 30, x + 60)
            print('cruz derecha')
            pyautogui.moveTo(x, y)
            print(pyautogui.position())
        elif event.type == ecodes.EV_KEY and event.code == 316 and event.value == 1:
            print('Botón XBOX presionado')
        elif event.type == ecodes.EV_KEY and event.code == 307 and event.value == 1:
            print('Botón X presionado')
        elif event.type == ecodes.EV_KEY and event.code == 305 and event.value == 1:
            print('Botón B presionado')
        elif event.type == ecodes.EV_KEY and event.code == 317 and event.value == 1:
            print('Se presiono THUMBL')
            pyautogui.press('tab')

                


#Definimos las funciones necesarias para detectar la USB

#Función para imprimir las propiedades de un dispositivo
def print_dev_info(device):
    print("Device sys_path: {}".format(device.sys_path))
    print("Device sys_name: {}".format(device.sys_name))
    print("Device sys_number: {}".format(device.sys_number))
    print("Device subsystem: {}".format(device.subsystem))
    print("Device device_type: {}".format(device.device_type))
    print("Device is_initialized: {}".format(device.is_initialized))

#Función para obtener el punto de montaja de un dispositivo USB
def get_mount_point(path):
    args = ["findmnt", "-unl", "-S", path]
    cp = sp.run(args, capture_output=True, text=True)
    out = cp.stdout.split(" ")[0]
    return out

#Funcion manejadora de eventos asociada al Monitor-Observer, que cambia una bandera en caso de insertar o remover una usb
def check_dev_events(action, device): 
    global usb
    global dispositivo
    if (action == "add"): #Si se añade una usb
        usb = 1
        print_dev_info(device)
        dispositivo = device #Pasar el objeto dispositivo a la variable global
    if (action == "remove"): #Si se retira una usb
        usb = 0


def detectar_usb():
    global usb
    global dispositivo
    while True:
        time.sleep(4) #Espera un poco para dar tiempo de montaje a la USB
        if (usb == 1):
            time.sleep(4)
            usb_nuevo = get_mount_point("/dev/" + dispositivo.sys_name)
            print("La ruta del dispositivo es: " + usb_nuevo)
            mostrar_contenido_usb(usb_nuevo)
            usb = 0 #Reinicia la bandera
        pass

        
def mostrar_contenido_usb(ruta_dispositivo):
    global dispositivo

    # Copiar archivos desde la USB al directorio
    app.after(0, lambda: copiar_archivos_smc(ruta_dispositivo))
    
    #if dispositivo in ventanas:
    #    return
    
    print("La ruta del dispositivo es: " + ruta_dispositivo)
    archivos = [archivo for archivo in os.listdir(ruta_dispositivo) if (archivo.endswith('.smc') or archivo.endswith('.sfc'))]
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

        archivos_smc = [archivo for archivo in os.listdir(desde_usb) if (archivo.endswith('.smc') or archivo.endswith('.sfc'))]

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
anchoVentana = app.winfo_screenwidth()
altoVentana = app.winfo_screenheight()

icono_apagar = PhotoImage(file="/home/fipy/Documents/Pruebas/icons/apagadoScale.png")  
icono_reiniciar = PhotoImage(file="/home/fipy/Documents/Pruebas/icons/restartScale.png") 

# Botón de apagar
btn_apagar = tk.Button(app, text="Apagar", command=apagar, bg="red", fg="white", image=icono_apagar, compound="right")
btn_apagar.pack(side=tk.RIGHT, padx=10, pady=10)

# Botón de reiniciar
btn_reiniciar = tk.Button(app, text="Reiniciar", command=reiniciar, bg="yellow", fg="black", image=icono_reiniciar, compound="right")
btn_reiniciar.pack(side=tk.RIGHT, padx=10, pady=10)


# Cargar imagen debajo de los botones
imagen_debajo = Image.open("/home/fipy/Documents/Pruebas/icons/instrucciones.png")  # Reemplaza con la ruta de tu imagen
imagen_debajo = ImageTk.PhotoImage(imagen_debajo)

# Para colocar la imagen
label_imagen = tk.Label(app, image=imagen_debajo)
#label_imagen.pack(side=tk.RIGHT, anchor='sw')
label_imagen.place(relx=0.9, rely=0.95, anchor='s')

menu = tk.Listbox(app, selectbackground="lightblue", bg="white", fg="black", font=("Courier", 14))
menu.pack(side="left", fill="both", expand=True)

for archivo in archivos:
    menu.insert(tk.END, archivo)

menu.bind("<ButtonRelease-1>", on_seleccion)
app.bind("<Escape>", salir)

#Líneas que relacionan el Monitor-Observer del contexto del hardware con tal de observar cambios en los dispositivos
context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem="block", device_type="partition")        
observer = pyudev.MonitorObserver(monitor, check_dev_events, name='monitor-observer')
observer.daemon #MonitorObserver sera un hilo demonio
observer.start()

#Inicia un hilo para la detección de las USB
hilo_usb = threading.Thread(target=detectar_usb)
hilo_usb.daemon #Es importante que este hilo sea demonio
hilo_usb.start()


# Inicia un hilo para el control del joystick
hilo_joystick = threading.Thread(target=joystick_control)
hilo_joystick.daemon
hilo_joystick.start()


app.mainloop()
