from datetime import date
import tkinter as tk
from tkinter.ttk import Frame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame

import logger

class Chart:
    df: DataFrame = None
    title: str = ""
    id: int = 0

    figure: FigureCanvasTkAgg = None
    display: Frame = None
    ax = None

    def __init__(self, df: DataFrame, title: str, id: int):
        self.df = df
        self.title = title
        self.id = id
        logger.log("Created chart id = " + str(self.id))

    def exportChart(self, filename: str):
        self.figure.print_png(filename)

    def displayChart(self, display: Frame, moduleDisplayer):
        logger.log("Displaying chart id = " + str(self.id))

        figure = plt.Figure(dpi=100)
        self.ax = figure.add_subplot(111)

        figure = FigureCanvasTkAgg(figure, display)
        figure.get_tk_widget().grid(row=0)

        moduleDisplayer(self.ax, self.df)

        self.ax.set_title(self.title)        
        self.figure = figure