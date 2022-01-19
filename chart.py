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

    __title: str = ""
    """Title of the chart."""
    __id: int = 0
    """ID of the chart."""
    __df: DataFrame = None
    """Data frame of loaded signal."""
    __figure: FigureCanvasTkAgg = None
    """Canvas of the chart."""
    __ax = None
    """Axes of the chart."""

    def __init__(self, df: DataFrame, title: str, id: int):
        self.__df = df
        self.__title = title
        self.__id = id
        logger.log("Created chart id = " + str(self.getId()))

    def getTitle(self) -> str:
        """Returns title of the chart.
        
        :returns: Title of the chart.
        """
        return self.__title
    
    def setTitle(self, title: str):
        """Sets title of the chart.
        
        :param title: New title of the chart.
        """
        self.__title = title

    def getDataframe(self) -> DataFrame:
        """Returns data frame of loaded signal.
        
        :returns: Data frame of loaded signal.
        """
        return self.__df

    def getId(self) -> int:
        """Returns ID of the chart.
        
        :returns: ID of the chart.
        """
        return self.__id

    def exportChart(self, filename: str):
        """Exports chart as .png file to specified destination.
        
        :param filename: Directory where canvas should be saved.
        """
        self.__figure.print_png(filename)

    def displayChart(self, display: Frame, moduleDisplayer):
        """Displays chart on screen.
        
        :param display: GUI component where chart should be displayed.
        :param moduleDisplayer: Method called in-line, that applies patches on chart from all active time series modules.
        """
        logger.log("Displaying chart id = " + str(self.getId()))

        __figure = plt.Figure(dpi=100)
        self.__ax = __figure.add_subplot(111)

        __figure = FigureCanvasTkAgg(__figure, display)
        __figure.get_tk_widget().grid(row=0)

        moduleDisplayer(self.__ax, self.getDataframe())

        self.__ax.set_title(self.getTitle())        
        self.__figure = __figure