from datetime import date
import tkinter as tk
from tkinter.ttk import Frame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame

import modules
import logger

appconfig = None
directories = None
lang = None

allcharts = []
id = 0

class Chart:
    display: Frame = None
    df: DataFrame = None
    figure: FigureCanvasTkAgg = None
    title: str = ""
    id: int = 0

    @staticmethod
    def addChart(self):
        global allcharts
        allcharts.append(self)

    def __init__(self, df: DataFrame, title: str):
        global id
        self.df = df
        self.title = title
        self.id = id
        id += 1
        Chart.addChart(self)
        logger.log("Created chart id = " + str(self.id))

    def exportChart(self, filename: str):
        self.figure.print_png(filename)

    def displayChart(self, display: Frame):
        logger.log("Displaying chart id = " + str(self.id))

        figure = plt.Figure(dpi=100)
        ax = figure.add_subplot(111)

        figure = FigureCanvasTkAgg(figure, display)
        figure.get_tk_widget().grid(row=0)

        modules.ChartModule.displayModules(ax, self.df)
        ax.set_title(self.title)
        
        self.figure = figure

def postConfigInit(_appconfig, _directories, _lang):
    global appconfig, directories, lang
    appconfig, directories, lang = _appconfig, _directories, _lang