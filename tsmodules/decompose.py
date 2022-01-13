from pandas.core.frame import DataFrame
from tsmodules import basemod
from tkinter import *
from tkinter import ttk
import statsmodels.api as sm
import pandas as pd
import loader
import entryvalidators

class DecomposeModule(basemod.TSModule):
    """Class implementing decomposition of time series.
    """

    __modelDict = None
    """Dictionary of decompose models, that can be used in seasonal decomposition function."""
    __lagentryvar = None
    """The length of the lag."""
    __modelscbvar = None
    """Model of time series to decompose."""
    __componentsvarlist = []
    """Selected components of explanatory parts of time series."""
    __componentslist = ["seasonal", "trend", "resid"]
    """Components of explanatory parts of time series."""

    def displayModule(self, ax, plotdf: DataFrame):
        """Processes analyzing module and displays results on chart's axes.

        :param ax: Reference to plot's axes.
        :param plotdf: Data frame with original signal.
        """
        if self.__lagentryvar.get() > 0:
            self.outputDataframe[plotdf.columns[0]]= plotdf[plotdf.columns[0]]

            series = pd.Series(x for x in plotdf[plotdf.columns[1]])
            res = sm.tsa.seasonal_decompose(series.values, period=self.__lagentryvar.get(), model=self.__modelDict[self.__modelscbvar.get()], extrapolate_trend='freq')
            reslist = [res.seasonal, res.trend, res.resid]
            i=0

            for comp in self.__componentslist:
                if self.__componentsvarlist[i].get():
                    self.outputDataframe[plotdf.columns[1] + " " + loader.lang["modules"]["decompose"][comp]] = reslist[i]
                i+=1
        
        if len(self.outputDataframe.columns) > 1:
            origdf = self.outputDataframe[[col for col in self.outputDataframe.columns]].groupby(self.outputDataframe.columns[0]).sum()
            origdf = self.outputDataframe.dropna()
            origdf.plot(kind='line', legend=True, ax=ax, color=self.getDisplayColor(),marker='o', fontsize=4, markersize=2)

    def buildConfig(self, section: ttk.Frame):
        """Provides GUI elements for time series module configuration.

        :param section: GUI component where module configuration should be displayed.
        """
        lablag = Label(section, text=loader.lang["modules"]["decompose"]["lag"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        lablag.grid(row=1)

        if not self.__lagentryvar:
            self.__lagentryvar = IntVar()
            self.__lagentryvar.set(1)
        vcmd = (section.register(entryvalidators.validate_digit),'%P')
        lagentry = Entry(section, textvariable=self.__lagentryvar, validate='all', validatecommand=vcmd, width=int((section.winfo_width()-13)/7)+1)
        cpyval = self.__lagentryvar.get()
        lagentry.grid(row=2)

        labmodels = Label(section, text=loader.lang["modules"]["decompose"]["model"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labmodels.grid(row=3)
        if not self.__modelscbvar:
            self.__modelscbvar = StringVar()
        modelscb = ttk.Combobox(section, state="readonly", textvariable=self.__modelscbvar, width=int((section.winfo_width()-13)/7)+1)
        modelscb.grid(row=4)
        modelscb['values'] = [loader.lang["modules"]["decompose"]["additive"], loader.lang["modules"]["decompose"]["multiplicative"]]
        modelscb.set(loader.lang["modules"]["decompose"]["additive"])

        i = 0
        for comp in self.__componentslist:
            labcomp = Label(section, text=loader.lang["modules"]["decompose"]["show"]+" "+loader.lang["modules"]["decompose"][comp], pady=5, width=int((section.winfo_width()-13)/7)+1)
            labcomp.grid(row=(i*2)+5)
            if len(self.__componentsvarlist) != len(self.__componentslist):
                self.__componentsvarlist.append(BooleanVar())
            compbtn = Checkbutton(section ,variable=self.__componentsvarlist[i], onvalue=1, offvalue=0)
            compbtn.grid(row=(i*2)+6)
            i+=1

    def __init__(self, name) -> None:
        super().__init__(name)
        self.__modelDict = {
            loader.lang["modules"]["decompose"]["additive"]: "additive",
            loader.lang["modules"]["decompose"]["multiplicative"]: "multiplicative",
        }
