import tkinter as tk
from tkinter import PhotoImage
import os

def apagar():
    os.system("shutdown now")

def reiniciar():
    os.system("reboot")

# Crear la app principal
app = tk.Tk()
app.title("Menú de Apagado")
app.attributes("-fullscreen", True)

# Íconos
icono_apagar = PhotoImage(file="./icons/apagadoN.png")  # Reemplaza "apagar_icono.png" con la ruta de tu propio ícono
icono_reiniciar = PhotoImage(file="./icons/restartN.png")  # Reemplaza "reiniciar_icono.png" con la ruta de tu propio ícono

# Botón de apagar
btn_apagar = tk.Button(app, text="Apagar", command=apagar, bg="red", fg="white", image=icono_apagar, compound="left")
btn_apagar.pack(pady=10)

# Botón de reiniciar
btn_reiniciar = tk.Button(app, text="Reiniciar", command=reiniciar, bg="yellow", fg="black", image=icono_reiniciar, compound="left")
btn_reiniciar.pack(pady=10)

# Ejecutar el bucle de la interfaz gráfica
app.mainloop()


