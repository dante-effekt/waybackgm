#!/bin/bash

function menuPrincipal(){
  ans=$(whiptail --title "Seleccione un juego que quiera" \
                 --menu "Elige una opción" 15 60 5 \
                 "1" "Zelda" \
                 "2" "Plants vs Zombies" \
                 "3" "Tetris" \
                 "4" "Crazy Taxi" \
                 "5" "Pero que ha pasao" \
                 3>&1 1<&2 2>&3)

  case "$ans" in
    1) xinit /home/fipy/SNES/snes9x-1.60/gtk/build/snes9x-gtk /home/fipy/Proyecto/waybackgm/pisnes/roms/Zelda.zip $* -- :0 vt$XDG_VTNR;;
    2) echo "PVZ";;
    3) echo "Crazy Taxi";;
    *) echo -e "Error";;
  esac
}

menuPrincipal

