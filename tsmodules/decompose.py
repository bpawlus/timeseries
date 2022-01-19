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
    __outvarLag = None
    """The length of the lag."""
    __outvarModel = None
    """Model of time series to decompose."""
    __selectedComponents = None
    """Selected components of explanatory parts of time series."""
    __allComponents = None
    """Components of explanatory parts of time series."""

    def displayModule(self, ax, plotdf: DataFrame):
        """Processes analyzing module and displays results on chart's axes.

        :param ax: Reference to plot's axes.
        :param plotdf: Data frame with original signal.
        """
        if self.__outvarLag.get() > 0:
            self.outputDf[plotdf.columns[0]]= plotdf[plotdf.columns[0]]

            series = pd.Series(x for x in plotdf[plotdf.columns[1]])
            res = sm.tsa.seasonal_decompose(series.values, period=self.__outvarLag.get(), model=self.__modelDict[self.__outvarModel.get()], extrapolate_trend='freq')
            reslist = [res.seasonal, res.trend, res.resid]
            i=0

            for comp in self.__allComponents:
                if self.__selectedComponents[i].get():
                    self.outputDf[plotdf.columns[1] + " " + loader.lang["modules"]["decompose"][comp]] = reslist[i]
                i+=1
        
        if len(self.outputDf.columns) > 1:
            origdf = self.outputDf[[col for col in self.outputDf.columns]].groupby(self.outputDf.columns[0]).sum()
            origdf = self.outputDf.dropna()
            origdf.plot(kind='line', legend=True, ax=ax, color=self.getDisplayColor(),marker='o', fontsize=4, markersize=2)

    def buildConfig(self, section: ttk.Frame):
        """Provides GUI elements for time series module configuration.

        :param section: GUI component where module configuration should be displayed.
        """
        labelLag = Label(section, text=loader.lang["modules"]["decompose"]["lag"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labelLag.grid(row=1)

        if not self.__outvarLag:
            self.__outvarLag = IntVar()
            self.__outvarLag.set(1)
        vcmd = (section.register(entryvalidators.validate_int_pos),'%P')
        entryLag = Entry(section, textvariable=self.__outvarLag, validate='all', validatecommand=vcmd, width=int((section.winfo_width()-13)/7)+1)
        entryLag.grid(row=2)

        labelModels = Label(section, text=loader.lang["modules"]["decompose"]["model"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labelModels.grid(row=3)
        if not self.__outvarModel:
            self.__outvarModel = StringVar()
        comboboxModels = ttk.Combobox(section, state="readonly", textvariable=self.__outvarModel, width=int((section.winfo_width()-13)/7)+1)
        comboboxModels.grid(row=4)
        comboboxModels['values'] = [loader.lang["modules"]["decompose"]["additive"], loader.lang["modules"]["decompose"]["multiplicative"]]
        comboboxModels.set(loader.lang["modules"]["decompose"]["additive"])

        i = 0
        for comp in self.__allComponents:
            labelComponent = Label(section, text=loader.lang["modules"]["decompose"]["show"]+" "+loader.lang["modules"]["decompose"][comp], pady=5, width=int((section.winfo_width()-13)/7)+1)
            labelComponent.grid(row=(i*2)+5)
            if len(self.__selectedComponents) != len(self.__allComponents):
                self.__selectedComponents.append(BooleanVar())
            checkComponent = Checkbutton(section ,variable=self.__selectedComponents[i], onvalue=1, offvalue=0)
            checkComponent.grid(row=(i*2)+6)
            i+=1

    def __init__(self, name) -> None:
        super().__init__(name)
        self.__selectedComponents = []
        self.__allComponents = ["seasonal", "trend", "resid"]
        self.__modelDict = {
            loader.lang["modules"]["decompose"]["additive"]: "additive",
            loader.lang["modules"]["decompose"]["multiplicative"]: "multiplicative",
        }
