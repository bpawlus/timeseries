from tkinter import *
import datetime

appconfig = None
directories = None
lang = None

win: Text = None

def log(text: str):
    date = datetime.datetime.now()
    win.insert(END, "[" + date.strftime("%X") + "] " + text + "\n")

def exportLogs(dir: str):
    pass

def postConfigInit(_appconfig, _directories, _lang):
    global appconfig, directories, lang
    appconfig, directories, lang = _appconfig, _directories, _lang