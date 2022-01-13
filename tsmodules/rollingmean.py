from pandas.core.frame import DataFrame
from tsmodules import basemod
from tkinter import *
from tkinter import ttk
import loader

class RollingMeanModule(basemod.TSModule):
    """Class implementing rolling mean time series module.
    """
    __rollCount = 5
    "Quanity of rolling value."

    def displayModule(self, ax, plotdf: DataFrame):
        """Processes analyzing module and displays results on chart's axes.

        :param ax: Reference to plot's axes.
        :param plotdf: Data frame with original signal.
        """
        dfrolling = plotdf.rename(columns={f'{plotdf.columns[1]}': f'{plotdf.columns[1]} {loader.lang["modules"]["rollingmean"]["rollingdisplay"]} {self.__rollCount}'})
        self.outputDataframe[plotdf.columns[0]] = [v[0] for v in plotdf.values]
        dfrolling = dfrolling[[col for col in dfrolling.columns]].groupby(dfrolling.columns[0]).sum()
        dfrolling = dfrolling.rolling(self.__rollCount).mean()
        self.outputDataframe[dfrolling.columns[0]] = [v[0] for v in dfrolling.values]
        dfrolling.plot(kind='line', legend=True, ax=ax, color=self.getDisplayColor(),marker='o', fontsize=5, markersize=2)

    def buildConfig(self, section: ttk.Frame):
        """Provides GUI elements for time series module configuration.

        :param section: GUI component where module configuration should be displayed.
        """
        labroll = Label(section, text=loader.lang["modules"]["rollingmean"]["count"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labroll.grid(row=1)
        __rollCountScale = Scale(section, from_=2, to=16, tickinterval=7, orient=HORIZONTAL, length=int(section.winfo_width()))
        __rollCountScale.set(self.__rollCount)
        __rollCountScale.grid(row=2)

        def updateChangePointCount(event):
            self.__rollCount = int(__rollCountScale.get())

        __rollCountScale.bind("<ButtonRelease-1>", updateChangePointCount)
    