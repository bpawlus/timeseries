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

    lagentryvar = None
    """The length of the lag."""

    def displayModule(self, ax, plotdf: DataFrame):
        """Processes analyzing module and displays results on chart's axes.

        :param ax: Reference to plot's axes.
        :param plotdf: Data frame with original signal.
        """
        if self.lagentryvar.get() > 0: 
            self.outputDataframe[loader.lang["modules"]["autocorrelations"]["lag"]] = [i+1 for i in range(0, int(self.lagentryvar.get()))]
        acft = acf([v[1] for v in plotdf.values], nlags=self.lagentryvar.get()).tolist()
        pacft = pacf([v[1] for v in plotdf.values], nlags=self.lagentryvar.get()).tolist()
        acft.pop(0)
        pacft.pop(0)
        self.outputDataframe[loader.lang["modules"]["autocorrelations"]["acorr"]] = acft
        self.outputDataframe[loader.lang["modules"]["autocorrelations"]["partacorr"]] = pacft

    def buildConfig(self, section: ttk.Frame):
        """Provides GUI elements for time series module configuration.

        :param section: GUI component where module configuration should be displayed.
        """
        lablag = Label(section, text=loader.lang["modules"]["autocorrelations"]["lag"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        lablag.grid(row=1)
        if not self.lagentryvar:
            self.lagentryvar = IntVar()
            self.lagentryvar.set(2)
        vcmd = (section.register(entryvalidators.validate_digit),'%P')
        lagentry = Entry(section, textvariable=self.lagentryvar, validate='all', validatecommand=vcmd, width=int((section.winfo_width()-13)/7)+1)
        lagentry.grid(row=2)