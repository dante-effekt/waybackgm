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

  echo -e "[+] Se ha instalado todo!"
}




function main(){
  installxbox

}


main
