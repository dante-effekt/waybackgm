# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 10:38:00 2023

@author: RGJG
"""

#=============================================================================
#================================MODULOS NECESARIOS===========================
#=============================================================================
import tkinter as tk
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

# Permite el rapido movimiento del cursor
pyautogui.FAILSAFE = False

# Vamos a obtener el directorio actual del archivo menu.py
directorio_actual = os.getcwd()
directorio = directorio_actual
usb = 0
dispositivo = 0
#directorio_usb = '/dev/sda1'
#directorio_usb = device.device_node


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
    comando = f'snes9x-gtk "{ruta_archivo}"'  
    sp.run(comando, shell=True)

def cargar_archivos():
    return [archivo for archivo in os.listdir(directorio) if (archivo.endswith('.smc') or archivo.endswith('.sfc'))]

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


def salir(event):
    app.destroy()
    sys.exit(0)

def joystick_control():
    # Lógica para controlar el menú con el joystick izquierdo
    #pyautogui.moveTo(-10,y)
    y = 21
    for event in joystick.read_loop():
        
        
        if event.type == ecodes.EV_ABS and event.code == 17:
            if event.value == 1:
                y = y + 20
                print('cruz abajo')
                pyautogui.moveTo(0,y)
                print(pyautogui.position())
                
                # Lógica para hacer que se desplace hacia abajo
                # menu.yview_scroll(1, "units")
                #on_tecla_abajo()
            elif event.value == -1:
                print('cruz arriba')
                y = y - 20
                pyautogui.moveTo(0, y)
                print(pyautogui.position())
                # Lógica para hacer que se desplace hacia arriba
                #menu.yview_scroll(-1, "units")
                #on_tecla_arriba()
        elif event.type == ecodes.EV_KEY and event.code == 545:
            if event.value == 1:
                y = y + 20
                print('cruz abajo')
                pyautogui.moveTo(0,y)
                print(pyautogui.position())
                
                
                
                
        elif event.type == ecodes.EV_KEY and event.code == 311:
            if event.value == 1:
                print('BOTON DERECHO/CLICK DERECHO')
                pyautogui.rightClick()
        
        elif event.type == ecodes.EV_KEY and event.code == 310:  # Código para el GATILLO IZQUIERDO 
            if event.value == 1:
                print('BOTON IZQUIERDO/CLICK IZQUIERDO')
                pyautogui.click()
                
                
                
        elif event.type == ecodes.EV_KEY and event.code == 544:
            if event.value == 1:
                print('cruz arriba')
                y = y - 20
                pyautogui.moveTo(0, y)
                print(pyautogui.position())
                
        elif event.type == ecodes.EV_KEY and event.code == 316:  # Código para el botón A
            if event.value == 1:
                #pyautogui.click()
                print('Botón XBOX presionado')
                # Lógica para hacer lo mismo que el clic izquierdo del mouse
                #on_clic_izquierdo()
                
        elif event.type == ecodes.EV_KEY and event.code == 307:  # Código para el botón A
            if event.value == 1:
                print('Botón X presionado')
                # Lógica para hacer lo mismo que el clic izquierdo del mouse
                #app.destroy()
                #sys.exit(0)
        elif event.type == ecodes.EV_KEY and event.code == 305:  # Código para el botón A
            if event.value == 1:
                print('Botón B presionado')
                #pyautogui.rightClick()
                # Lógica para hacer lo mismo que el clic izquierdo del mouse
                #ventana_usb.destroy()
                #cerrar_ventana()
                


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
    #if (action == "remove"): #Si se retira una usb
    #    usb = 0


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
# --------------------------
def copy_games(source, destination):
    try:
        for root, dirs, files in os.walk(source):
            for file in files:
                if file.lower().endswith(".smc"):
                    source_file = os.path.join(root, file)

                    destination_file = os.path.join(destination, file)
                    shutil.copy2(source_file, destination_file)

                if file.lower().endswith(".sfc"):
                    source_file = os.path.join(root, file)

                    destination_file = os.path.join(destination, file)
                    shutil.copy2(source_file, destination_file)
        print("Se han copiado")

    except Exception as e:
        print("error en la copia")



def usb_detect():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor = filter_by(subsystem='block',  device_type='disk')
    connected_usn = None

    for dusb in iter(monitor.poll, None):
        if dusb.action == 'add':
            print(f"Usb conectada: {dusb.device_node}")
            sou_dir= device.device_node
            destination_dir = os.getcwd()

            try: 
                copy_games(sou_dir, destination_file)
                connected_usn = device.device_node
            except Exception as e:
                print("Error de montura xd")
        elif dusb.action == 'remove'and connected_usn == device.device_node:
            print("Se ha desconectado")
            connected_usn = None

# ----------------------------------------

        
def mostrar_contenido_usb(ruta_dispositivo):
    global directorio_usb

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

menu = tk.Listbox(app, selectbackground="lightblue", bg="white", fg="black", font=("Courier", 14))
menu.pack(side="left", fill="both", expand=True)

for archivo in archivos:
    menu.insert(tk.END, archivo)

menu.bind("<ButtonRelease-1>", on_seleccion)
app.bind("<Escape>", salir)

#Líneas que relacionan el Monitor-Observer del contexto del hardware con tal de observar cambios en los dispositivos
context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem="block", device_type="disk")        
observer = pyudev.MonitorObserver(monitor, check_dev_events, name='monitor-observer')
observer.daemon #MonitorObserver sera un hilo demonio
observer.start()

#Inicia un hilo para la detección de las USB
hilo_usb = threading.Thread(target=usb_detect)
hilo_usb.daemon #Es importante que este hilo sea demonio
hilo_usb.start()


# Inicia un hilo para el control del joystick
hilo_joystick = threading.Thread(target=joystick_control)
hilo_joystick.daemon
hilo_joystick.start()


app.mainloop()
