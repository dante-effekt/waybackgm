#!/usr/bin/bash
#

function installxbox(){
  echo -e "[!] Instalando dependencias para el driver del control Xbox 360"
  sleep 2
  cd ~/ 
  sudo apt-get install -y \
   g++ \
   libboost-dev \
   scons \
   pkg-config \
   libusb-1.0-0-dev \
   git-core \
   libx11-dev \
   libudev-dev \
   x11proto-core-dev \
   libdbus-glib-1-dev \
   scons
  
  pip install evdev
  pip install pyautogui

  echo -e "[!] Clonando el repositorio xboxdrv "
  sleep 2
  git clone https://github.com/xboxdrv/xboxdrv
  cd xboxdrv
  scons

  echo -e "[+] Se ha instalado el driver"
}

function snes9x (){
  echo -e "[!] Instalando dependencias para el emulador"
  sleep 2
  # Instalar dependencias
  sudo apt install libsdl2-dev libgtkmm-3.0-dev libepoxy-dev meson alsa-oss portaudio19-dev libminizip-dev
  echo -e "[!] Descargando e instalando el emulador"
  sleep 2
  # Descargar el código fuente de snes9x
  wget https://github.com/snes9xgit/snes9x/archive/refs/tags/1.60.tar.gz
  # Descomprimir el archivo
  tar -xzf 1.60.tar.gz
  # Cambiar al directorio snes9x
  cd snes9x-1.60/gtk
  # Configurar y compilar el proyecto con meson
  meson build --buildtype=release --strip
  # Cambiar al directorio de compilación
  cd build
  # Compilar con ninja
  ninja
  echo -e "[+] Se ha instalado el emulador"
}



function main(){
  installxbox
  snes9x
}


main
