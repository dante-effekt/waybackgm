# waybackgm
Implementation of retro game emulation for Raspberry Pi 4.

## Instalación de dependencias
Para instalar los requerimientos y dependencias necesarias es necesario ejecutar los siguientes comandos

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
