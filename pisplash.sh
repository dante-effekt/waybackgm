#!/bin/bash

#Aqui hay que colocar la ruta correcta al tema.
SPLASH_PATH=/usr/share/plymouth/themes/debian-theme 

SPLASH_PATH_BAK="$SPLASH_PATH"-bak # Es para el backup

IMGFILE=$1

if [ $IMGFILE != "restore" ]; then

    # Backup
    if [ ! -d "$SPLASH_PATH_BAK" ]; then
        sudo cp -rf $SPLASH_PATH $SPLASH_PATH_BAK
    fi
    
    # Rasoberry Pi OS
    if [ -f "$SPLASH_PATH/animation-0001.png" ]; then
        for splashimg in $SPLASH_PATH/animation*.png
            do sudo rm -rf $splashimg && sudo cp $IMGFILE $splashimg
        done
        for splashimg in $SPLASH_PATH/throbber*.png
            do sudo rm -rf $splashimg && sudo cp $IMGFILE $splashimg
        done    
    fi
    
    # LMDE
    if [ -f "$SPLASH_PATH/logo.png" ]; then
        sudo rm -rf $SPLASH_PATH/logo.png && sudo cp $IMGFILE $SPLASH_PATH/logo.png
        sudo rm -rf $SPLASH_PATH/spinner.png && sudo cp transparent.png $SPLASH_PATH/spinner.png
        sudo cp transparent.png $SPLASH_PATH/debian.png
    fi
    
else
    sudo rm -rf $SPLASH_PATH
    sudo cp -rf $SPLASH_PATH_BAK $SPLASH_PATH 
fi

sudo update-initramfs -u
