#!/bin/python3
#
# waybackgm.py
#
# Authors: Arguello Dante, Caballero Daniel, Jimenez Rodrigo 
# Date: 2023.11.16
# License: MIT
#
# Skeleton for waybackgm, this mounts an USB device, and play video and images with VLC.

import vlc
import time
import signal, sys
import os
import pyudev
import threading
import subprocess as sp

stop_event = threading.Event()

def def_handler(sig, frame):
	sys.exit(1)

signal.signal(signal.SIGINT, def_handler)
signal.signal(signal.SIGTSTP, def_handler)

ruta_img_usb = []  # Rutas de las imágenes USB
usb = 0  # Flag para saber si hay una USB conectada
dispositivo = 0  # Mutará de int a objeto device cuando se inserte una USB

# Empieza con 20 segundos de video con volumen gradual
player = vlc.MediaPlayer()
video = vlc.Media('/home/fipy/Documents/pi/videos/video.mp4')
video.add_option("start-time=0")
video.add_option("stop-time=20")
player.set_media(video)
player.audio_set_volume(0)  # Comienza con volumen en 0
player.play()

# Función para ajustar gradualmente el volumen
def adjust_volume(volume, target_volume, duration):
	step = (target_volume - volume) / (duration * 10)
	for _ in range(int(duration * 10)):
		time.sleep(0.1)
		volume += step
		player.audio_set_volume(int(volume))

# Aumentar volumen gradualmente durante los primeros 5 segundos
adjust_volume(0, 100, 5)

# Mantener el volumen máximo durante 10 segundos
time.sleep(10)

# Disminuir volumen gradualmente durante los últimos 5 segundos
adjust_volume(100, 0, 5)

# Inicio en 0
startT = time.time()
while player.is_playing():
	currentT = time.time()
	if currentT - startT > 20:
		break

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


context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem="block", device_type="partition")
def check_dev_events(action, device): #Funcion manejadora de eventos
	global usb
	global dispositivo
	if (action == "add"): #Si se añade una usb
		usb = 1
		dispositivo = device #Pasar el objeto dispositivo a la variable global
	if (action == "remove"): #Si se retira una usb
		usb = 0
observer = pyudev.MonitorObserver(monitor, check_dev_events, name='monitor-observer')
observer.daemon #MonitorObserver sera un hilo demonio
observer.start()

with open ("/home/fipy/Documents/pi/pictures/playlist.m3u", "r") as lista:
	imagen = str(lista.read()).split("\n")
	imagen.pop()
lista.close()

while (player.is_playing):
	if (usb==0):
		#Mostrar imagenes locales
		for elemento in imagen:
			if (usb == 1): #Para hacer un cambio a las imagenes de USB sin ejecutar todo el for
				break
			foto = vlc.Media(elemento)
			player.set_media(foto)
			player.play()
			time.sleep(3)
	else:
		#Mostrar imagenes de dispositivo
		print_dev_info(dispositivo)
		auto_mount("/dev/" + dispositivo.sys_name)
		mp = get_mount_point("/dev/" + dispositivo.sys_name)
		print("Mount point: {}".format(mp))
		photos=dev_stats(mp)
		ruta_img_usb = photos
		for elemento in ruta_img_usb:
			if (usb == 0): #Deja de ejecutar el for si se retira la USB
				break
			foto = vlc.Media(elemento)
			player.set_media(foto)
			player.play()
			time.sleep(3)
			
