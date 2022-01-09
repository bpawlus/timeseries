from datetime import date
import tkinter as tk
from tkinter.ttk import Frame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame

import logger

class Chart:
    """Class contains loaded time series data in form of charts.
    """

    df: DataFrame = None
    """Data frame of loaded signal."""
    title: str = ""
    """Title of the chart."""
    id: int = 0
    """ID of the chart."""

    figure: FigureCanvasTkAgg = None
    """Canvas of the chart."""
    ax = None
    """Axes of the chart."""

    def __init__(self, df: DataFrame, title: str, id: int):
        self.df = df
        self.title = title
        self.id = id
        logger.log("Created chart id = " + str(self.id))

    def exportChart(self, filename: str):
        """Exports chart as .png file to specified destination.
        
        :param filename: Directory where canvas should be saved.
        """
        self.figure.print_png(filename)

    def displayChart(self, display: Frame, moduleDisplayer):
        """Displays chart on screen.
        
        :param display: GUI component where chart should be displayed.
        :param moduleDisplayer: Method called in-line, that applies patches on chart from all active time series modules.
        """
        logger.log("Displaying chart id = " + str(self.id))

        figure = plt.Figure(dpi=100)
        self.ax = figure.add_subplot(111)

        figure = FigureCanvasTkAgg(figure, display)
        figure.get_tk_widget().grid(row=0)

        moduleDisplayer(self.ax, self.df)

        self.ax.set_title(self.title)        
        self.figure = figure