#!/bin/bash

function menuPrincipal(){
  ans=$(whiptail --title "Seleccione un juego que quiera" \
                 --menu "Elige una opción" 15 60 5 \
                 "1" "Call of Duty" \
                 "2" "Plants vs Zombies" \
                 "3" "Tetris" \
                 "4" "Crazy Taxi" \
                 "5" "Pero que ha pasao" \
                 3>&1 1<&2 2>&3)

  case "$ans" in
    1) echo "Se ejecuta Duty";;
    2) echo "PVZ";;
    3) echo "Crazy Taxi";;
    *) echo -e "Error";;
  esac
}

menuPrincipal
