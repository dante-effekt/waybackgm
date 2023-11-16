#!/bin/python3
from tkinter import *

def fnSumar():
    n1 = text1.get()
    n2 = text2.get()
    res = float(n1) + float(n2)
    text3.delete(0,'end')
    text3.insert(0,str(res))

# La ventana completa
raiz=Tk()
raiz.title("Selecciona el juego que desees:")
# raiz.resizable(True,False)
raiz.geometry("700x300")
# raiz.config(bg="blue")


# Un label dentro del sistema
lbl = Label(raiz, text="Primer numero", bg="yellow")
lbl.place(x=15, y=10, width=120, height=30)
text1 = Entry(raiz, bg="cyan")
text1.place(x=150, y=10, width=120, height=30)
btn = Button(raiz, text="Suma", command=fnSumar)
btn.place(x=300, y=20, width=100, height=50)

lbl2= Label(raiz, text="Segundo numero", bg="yellow")
lbl2.place(x=15, y=50, width=120, height=30)
text2 = Entry(raiz, bg="cyan")
text2.place(x=150, y=50, width=120, height=30)

lbl3= Label(raiz, text="Resultado: ", bg="red")
lbl3.place(x=15, y=120, width=120, height=30)
text3 = Entry(raiz, bg="cyan")
text3.place(x=150, y=120, width=120, height=30)

#btn = Button(raiz, text="Presiona este boton para mensaje", command=mensaje)
#btn.place(x=205, y=10, width=200, height=50)
# btn.pack() # De igual manera esto es para mostrar en sí el label



raiz.mainloop()
