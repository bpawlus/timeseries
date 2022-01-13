from pandas.core.frame import DataFrame
from tsmodules import basemod
from tkinter import *
from tkinter import ttk
import loader
import entryvalidators

class DifferentiationModule(basemod.TSModule):
    """Class implementing differentiation time series module.
    """

    __lagentryvar = None
    """The length of the lag."""

    def displayModule(self, ax, plotdf: DataFrame):
        """Processes analyzing module and displays results on chart's axes.

        :param ax: Reference to plot's axes.
        :param plotdf: Data frame with original signal.
        """
        self.outputDataframe[plotdf.columns[0]] = [v[0] for v in plotdf.values]
        df = plotdf.rename(columns={f'{plotdf.columns[1]}': f'{plotdf.columns[1]} {loader.lang["modules"]["differentiation"]["diffdisplay"]} {loader.lang["modules"]["differentiation"]["lag"]} {self.__lagentryvar.get()}'})
        df = df[[col for col in df.columns]].groupby(df.columns[0]).sum()
        df = df.diff(periods=self.__lagentryvar.get())
        self.outputDataframe[df.columns[0]] = [v[0] for v in df.values]
        df.plot(kind='line', legend=True, ax=ax, color=self.getDisplayColor(),marker='o', fontsize=5, markersize=2)

    def buildConfig(self, section: ttk.Frame):
        """Provides GUI elements for time series module configuration.

        :param section: GUI component where module configuration should be displayed.
        """
        lablag = Label(section, text=loader.lang["modules"]["differentiation"]["lag"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        lablag.grid(row=1)
        if not self.__lagentryvar:
            self.__lagentryvar = IntVar()
            self.__lagentryvar.set(1)
        vcmd = (section.register(entryvalidators.validate_digit),'%P')
        lagentry = Entry(section, textvariable=self.__lagentryvar, validate='all', validatecommand=vcmd, width=int((section.winfo_width()-13)/7)+1)
        lagentry.grid(row=2)