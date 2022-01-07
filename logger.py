from tkinter import *
import datetime

win: Text = None
"""Text component where logs are stored."""

def log(text: str):
    """Logs a message to a component.

    :param text: Text to log.
    """
    date = datetime.datetime.now()
    win.insert(END, "[" + date.strftime("%X") + "] " + text + "\n")
