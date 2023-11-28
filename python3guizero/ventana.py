#!/usr/bin/env python3

from guizero import App, Text
import signal, os, sys, time

def def_handler(sig, frame):
    print("\n[+] Saliendo...")
    sys.exit(1)



signal.signal(signal.SIGINT, def_handler)

app = App(title="Hello world")

welcome = Text(app, text="Welcome to my app")



app.display()
