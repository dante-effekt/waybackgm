# waybackgm
Implementation of retro game emulation for Raspberry Pi 4.
Autores: Arguello León Dante Moisés, Caballero Hernández Juan Daniel, Jimenez García Rodrigo Gaudencio

## Instalación de dependencias
Para instalar los requerimientos y dependencias necesarias es necesario ejecutar los siguientes comandos

En esta parte hemos implementado un script que nos automatiza la instalación del driver y el emulador por lo que se presentan las instrucciones para descargar el proyecto y ejecutar el script
finalmente las modificaciones en los servicios de acceso remoto debido a la naturaleza de la configuración de estos se requiere que se hagan de manera manual.

```bash
git clone https://github.com/dante-effekt/waybackgm.git 
cd waybackgm
chmod +x autorun.sh
./autorun.sh
```

### Instalación de xboxdrv

```bash
sudo apt-get install \
 g++ \
 libboost-dev \
 scons \
 pkg-config \
 libusb-1.0-0-dev \
 git-core \
 libx11-dev \
 libudev-dev \
 x11proto-core-dev \
 libdbus-glib-1-dev
```

Y ahora a descargar y compilar el driver 

```bash
# Descarga del repositorio oficial
git clone https://github.com/xboxdrv/xboxdrv.git
# Entramos en la carpeta del repositorio
cd xboxdrv
# Compilamos el proyecto
scons
# Instalamos este ejecutable en el sistema
make install
```

### Instalación del Snes9x

```bash
# Descarga del repositorio
wget https://github.com/snes9xgit/snes9x/archive/refs/tags/1.60.tar.gz
# Descomprimirlo
tar -xzf 1.60.tar.gz
# Entrar en la carpeta descomprimida
cd snes9x-1.60/gtk
# Uso del comando meson
meson build --buildtype=release --strip
# Ingresamos a la carpeta creada del resultado del comando anterior
cd build
# Compilacion con el comando ninja
ninja
# Resultado final,  tenemos el emulador compilado y funcionando
./snes9x-gtk
```

### Además de instalar todos los módulos necesarios del script de python con el siguiente comando

```bash
pip install -r requirements.txt
```


# Configuración en la Raspberry PI para la detección del control

Primero hay que ver que reconozca el control:

```bash
lsusb
```

Si aparece entonces podemos ejecutar xboxdrv, estando dentro del 
directorio, si da error entonces intentar con sudo.

Sin embargo si esto no aparece podemos ejecutar el siguiente comando 

```bash
ls /dev/input/by-id/
```

De aqui vamos a identificar nuestro control y copiar el que tenga 'event'
Posteriormente lo vamos  a reemplazar en el siguiente comando:

```bash
sudo xboxdrv \
    --evdev /dev/input/by-id/<REEMPLAZAR> \
    --silent \
    --detach-kernel-driver \
    --deadzone 500 \
    --mimic-xpad \
    --evdev-absmap ABS_X=x1,ABS_Y=y1,ABS_RX=x2,ABS_RY=y2,ABS_Z=lt,ABS_RZ=rt,ABS_HAT0X=dpad_x,ABS_HAT0Y=dpad_y \
    --evdev-keymap BTN_A=a,BTN_B=b,BTN_X=x,BTN_Y=y,BTN_TL=lb,BTN_TR=rb,BTN_THUMBL=tl,BTN_THUMBR=tr,BTN_MODE=guide,BTN_SELECT=back,BTN_START=start \
    --axismap -Y1=Y1,-Y2=Y2
```

Si funciona entonces ya nos dira en que event y js está disponible, pero
habra que mantenerlo abierto, si cerramos o precionamos ctrl+c puede que
lo deshabilite, para esto creamos el siguiente script init.d bash.

Creamos primero el archivo con:

```bash
sudo nano /etc/init.d/xboxdrv-startup
```

Ahora copiamos lo siguiente al archivo:

```bash
#!/bin/sh
### BEGIN INIT INFO
# Provides:          xboxdrv
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start xboxdrv on boot
### END INIT INFO

case "$1" in
    start)
        echo "Starting xboxdrv"
        /usr/local/bin/xboxdrv \
    	    --evdev /dev/input/by-id/<REEMPLAZAR> \
            --silent \
            --detach-kernel-driver \
            --deadzone 500 \
            --mimic-xpad \
            --evdev-absmap ABS_X=x1,ABS_Y=y1,ABS_RX=x2,ABS_RY=y2,ABS_Z=lt,ABS_RZ=rt,ABS_HAT0X=dpad_x,ABS_HAT0Y=dpad_y \
            --evdev-keymap BTN_A=a,BTN_B=b,BTN_X=x,BTN_Y=y,BTN_TL=lb,BTN_TR=rb,BTN_THUMBL=tl,BTN_THUMBR=tr,BTN_MODE=guide,BTN_SELECT=back,BTN_START=start \
            --axismap -Y1=Y1,-Y2=Y2\
		&
        ;;
    stop)
        echo "Stopping xboxdrv"
        killall xboxdrv
        ;;
    *)
        echo "Usage: /etc/init.d/xboxdrv-startup {start|stop}"
        exit 1
        ;;
esac

exit 0
```

Vemos donde esta instalado xboxdrv con el siguiente comando:

```bash
which xboxdrv
```

Copiamos la ruta y verificamos que sea la misma que tenemos en el script
sino la reemplazamos y damos permisos:

```bash
sudo chmod +x /usr/local/bin/xboxdrv
```

Si todo está bien entonces podremos iniciar el servicio con:

```bash
sudo /etc/init.d/xboxdrv-startup start
```

Para detenerlo basta con poner: 

```bash
sudo /etc/init.d/xboxdrv-startup stop
```

Para probar que funcione el mapeo entonces se hace con:

```bash
evtest /dev/input/event9
```

# Configuración de las Raspberry para acceso remoto

Hay que configurar primero como AP y el DHCP, a continuacion 
listo todo lo que se necesita:

```bash
sudo apt-get install dnsmasq hostapd
sudo pip3 install -U python-magic

sudo systemctl stop dnsmasq
sudo systemctl stop hostapd
```

Ahora nos dirigimos a /etc/dhcpcd.conf

Creamos el arcivo si es necesario.*
```bash
interface wlan0
static ip_address=192.168.28.254/24
nohook wpa_supplicant

sudo service dhcpcd restart
```

Ahora nos dirigimos a /etc/dnsmasq.conf
```bash
\# Use the require wireless interface - usually wlan0
interface=wlan0
\# Reserve 20 IP addresses, set the subnet mask, and lease time
dhcp-range=192.168.28.200,192.168.28.220,255.255.255.0,24h

systemctl start dnsmasq
```

Ahora nos dirigimos a /etc/hostapd/hostapd.conf y colocamos:

```bash
# Wireless interface
interface=wlan0
# Specification: IEEE802.11
driver=nl80211
# The SSID or name of the network
ssid=fipy-DDR
# Password of the network
wpa_passphrase=12345678
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
# Mode and frequency of operation
hw_mode=g
# Broadcast channel
channel=5
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
rsn_pairwise=CCMP
```

Ahora edite el archivo /etc/default/hostapd y reemplace la línea que comienza con #DAEMON\_CONF con:
DAEMON\_CONF="/etc/hostapd/hostapd.conf"

```bash
Ejecutamos killall wpa_supplicant
```

y los siguientes

```bash
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
Verifique que los servicios se están ejecutando
sudo systemctl status hostapd
sudo systemctl status dnsmasq
```

Ahora ya hay que activar SSH y VNC Server en la raspberry

En el cliente abrimos VNC Connect, ingresamos la ip de la raspberry,
nos pide el usuario y contraseña.

Ahora revisamos la resolucion de la pantalla:
Inicio > Preferencias > Raspberry Pi Configuration > Display

Ahora configuramos la localizacion y zona horaria:  
Inicio > Preferencias > Raspberry Pi Configuration > Localization

Reiniciamos la raspberry pi

Fillezilla solo necesita el cliente poner la ip de la rasp
usuario, contraseña y el puerto 22.

# Configuración para que las Raspberry tenga sonido al encender

Hay que poner el archivo .wav en la carpeta soundboot
instalar el siguiente en caso de no tenerlo:

```bash
sudo apt-get install alsa-utils
```

Ajustar archivo.sh de acuerdo a la ruta en que está.

Luego  abrir la terminal y ejecutar lo siguiente:

```bash
sudo nano /etc/rc.local
```

Añadir hasta el final, antes de return 0;, la siguiente linea:

```bash
/usr/bin/aplay /home/fipy/Desktop/soundboot/jing.wav
```

Cerramos el archivo y reiniciamos

# Ajuste de la imagen de inicio

La imagen debe ser PNG en tamaño 100x100 px
Se puede escalar con imagemagick, si no se tiene se instala con:

```bash
sudo apt-get install imagemagick
```

Para escalar forzadamente es con el siguiente:

```bash
convert splash.png -resize 100x100\! splash2.png
```

Copiamos la carpeta pisplash, sugiero tener las imagenes dentro de ese
directorio. Nos colocamos dentro del directorio para poder ejecutarlo, 
pero antes hay que cambiar los permisos.

```bash
chmod +x pisplash.sh
```

Para reemplazar la imagen hay que antes revisar que la ruta del path
sea la correcta, en ese caso uso debian-theme y sé que tiene dos imagenes
relevantes, debian.png y logo.png.

El tema tambien debe configurarse en el siguiente archivo:
```bash
sudo nano  /etc/plymouth/plymouthd.conf
```

Ya con eso, entonces nos colocamos en el directorio desde terminal
y ejecutamos el siguiente:

```bash
bash pisplash.sh /home/fipy/Desktop/pisplash/splash3.png
//bash pisplash.sh [img.png]
```

Se va a actualizar automaticamente initframs, luego de eso procedemos
a reiniciar y listo.
