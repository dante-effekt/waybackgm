#!/bin/bash

# Instalar dependencias
sudo apt install libsdl2-dev libgtkmm-3.0-dev libepoxy-dev meson alsa-oss portaudio19-dev libminizip-dev

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
