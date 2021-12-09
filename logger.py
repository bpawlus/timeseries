from tkinter import *
import datetime

win: Text = None

def log(text: str):
    date = datetime.datetime.now()
    win.insert(END, "[" + date.strftime("%X") + "] " + text + "\n")
