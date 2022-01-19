from pandas.core.frame import DataFrame
from tsmodules import basemod
from tkinter import *
from tkinter import ttk
import loader
import entryvalidators
from statsmodels.graphics.tsaplots import acf, pacf

class AutocorrelationsModule(basemod.TSModule):
    """Class implementing autocorrelation and partial autocorrelation time series module.
    """

    __outvarLag = None
    """The length of the lag."""

    def displayModule(self, ax, plotdf: DataFrame):
        """Processes analyzing module and displays results on chart's axes.

        :param ax: Reference to plot's axes.
        :param plotdf: Data frame with original signal.
        """
        
        if self.__outvarLag.get() > 0: 
            self.outputDf[loader.lang["modules"]["autocorrelations"]["lag"]] = [i+1 for i in range(0, int(self.__outvarLag.get()))]
        acft = acf([v[1] for v in plotdf.values], nlags=self.__outvarLag.get()).tolist()
        pacft = pacf([v[1] for v in plotdf.values], nlags=self.__outvarLag.get()).tolist()
        acft.pop(0)
        pacft.pop(0)
        self.outputDf[loader.lang["modules"]["autocorrelations"]["acorr"]] = acft
        self.outputDf[loader.lang["modules"]["autocorrelations"]["partacorr"]] = pacft

    def buildConfig(self, section: ttk.Frame):
        """Provides GUI elements for time series module configuration.

        :param section: GUI component where module configuration should be displayed.
        """
        labelLag = Label(section, text=loader.lang["modules"]["autocorrelations"]["lag"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labelLag.grid(row=1)
        if not self.__outvarLag:
            self.__outvarLag = IntVar()
            self.__outvarLag.set(2)
        vcmd = (section.register(entryvalidators.validate_int_pos),'%P')
        entryLag = Entry(section, textvariable=self.__outvarLag, validate='all', validatecommand=vcmd, width=int((section.winfo_width()-13)/7)+1)
        entryLag.grid(row=2)