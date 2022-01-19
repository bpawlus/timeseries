from pandas.core.frame import DataFrame
from tsmodules import basemod
from tkinter import *
from tkinter import ttk, messagebox
import loader
import entryvalidators
from ruptures.metrics import *

class RupturesEvaluation(basemod.TSModule):
    """Class implementing change point detection evaluation in time series modules.
    Evaluations include Hausdorff metric, rand index, precision and recall.
    """

    __outvarOrigset = None
    """First (original) set of change point indexes."""
    __outvarEstset = None
    """Second (predicted) set of change point indexes."""
    __outvarMargin = None
    """Margin value used to calculate true positives."""

    def __argError(self):
        """Method displayed when sets have been wrongly filled."""
        self.outputDf[loader.lang["modules"]["evaluation"]["set1"]] = ["Err"]
        self.outputDf[loader.lang["modules"]["evaluation"]["set2"]] = ["Err"]
        self.outputDf[loader.lang["modules"]["evaluation"]["hausdorff"]] = ["Err"]
        self.outputDf[loader.lang["modules"]["evaluation"]["randindex"]] = ["Err"]
        self.outputDf[loader.lang["modules"]["evaluation"]["precision"]] = ["Err"]
        self.outputDf[loader.lang["modules"]["evaluation"]["recall"]] = ["Err"]
        messagebox.showerror(loader.lang["messagebox"]["error"], loader.lang["modules"]["evaluation"]["wrongset"])

    def displayModule(self, ax, plotdf: DataFrame):
        """Processes analyzing module and displays results on chart's axes.

        :param ax: Reference to plot's axes.
        :param plotdf: Data frame with original signal.
        """

        set1split = self.__outvarOrigset.get().split(",")
        set2split = self.__outvarEstset.get().split(",")
        try:
            set1 = list(map(int, set1split))
            set2 = list(map(int, set2split))

            if(len(set1) >= 2 and len(set2) >= 2):
                self.outputDf[loader.lang["modules"]["evaluation"]["set1"]] = [self.__outvarOrigset.get()]
                self.outputDf[loader.lang["modules"]["evaluation"]["set2"]] = [self.__outvarEstset.get()]
                self.outputDf[loader.lang["modules"]["evaluation"]["hausdorff"]] = [hausdorff(set1, set2)]
                self.outputDf[loader.lang["modules"]["evaluation"]["randindex"]] = [randindex(set1, set2)]
                p, r = precision_recall(set1, set2, margin=self.__outvarMargin.get())
                self.outputDf[loader.lang["modules"]["evaluation"]["precision"]] = [p]
                self.outputDf[loader.lang["modules"]["evaluation"]["recall"]] = [r]
            else:
                self.__argError()
        except ValueError as e:
            self.__argError()

    def buildConfig(self, section: ttk.Frame):
        """Provides GUI elements for time series module configuration.

        :param section: GUI component where module configuration should be displayed.
        """  
        labelOrigset = Label(section, text=loader.lang["modules"]["evaluation"]["set1"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labelOrigset.grid(row=1)
        if not self.__outvarOrigset:
            self.__outvarOrigset = StringVar()
            self.__outvarOrigset.set("")
        entryOrigset = Entry(section, textvariable=self.__outvarOrigset, width=int((section.winfo_width()-13)/7)+1)
        entryOrigset.grid(row=2)

        labelEstset = Label(section, text=loader.lang["modules"]["evaluation"]["set2"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labelEstset.grid(row=3)
        if not self.__outvarEstset:
            self.__outvarEstset = StringVar()
            self.__outvarEstset.set("")
        entryEstset = Entry(section, textvariable=self.__outvarEstset, width=int((section.winfo_width()-13)/7)+1)
        entryEstset.grid(row=4)

        labelMargin = Label(section, text=loader.lang["modules"]["evaluation"]["margin"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labelMargin.grid(row=5)
        if not self.__outvarMargin:
            self.__outvarMargin = IntVar()
            self.__outvarMargin.set(10.0)
        vcmd = (section.register(entryvalidators.validate_int_pos),'%P')
        entryMargin = Entry(section, textvariable=self.__outvarMargin, validate='all', validatecommand=vcmd, width=int((section.winfo_width()-13)/7)+1)
        entryMargin.grid(row=6)