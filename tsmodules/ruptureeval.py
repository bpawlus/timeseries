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

    set1var = None
    """First set of change point indexes."""
    set2var = None
    """Second set of change point indexes."""
    marginvar = None
    """Margin value used to calculate true positives."""

    def argError(self):
        """Method displayed when sets have been wrongly filled."""
        self.outputDataframe[loader.lang["modules"]["evaluation"]["set1"]] = ["Err"]
        self.outputDataframe[loader.lang["modules"]["evaluation"]["set2"]] = ["Err"]
        self.outputDataframe[loader.lang["modules"]["evaluation"]["hausdorff"]] = ["Err"]
        self.outputDataframe[loader.lang["modules"]["evaluation"]["randindex"]] = ["Err"]
        self.outputDataframe[loader.lang["modules"]["evaluation"]["precision"]] = ["Err"]
        self.outputDataframe[loader.lang["modules"]["evaluation"]["recall"]] = ["Err"]
        messagebox.showerror(loader.lang["messagebox"]["error"], loader.lang["modules"]["evaluation"]["wrongset"])

    def displayModule(self, ax, plotdf: DataFrame):
        """Processes analyzing module and displays results on chart's axes.

        :param ax: Reference to plot's axes.
        :param plotdf: Data frame with original signal.
        """

        set1split = self.set1var.get().split(",")
        set2split = self.set2var.get().split(",")
        try:
            set1 = list(map(int, set1split))
            set2 = list(map(int, set2split))

            if(len(set1) >= 3, len(set2) >= 3):
                self.outputDataframe[loader.lang["modules"]["evaluation"]["set1"]] = [self.set1var.get()]
                self.outputDataframe[loader.lang["modules"]["evaluation"]["set2"]] = [self.set2var.get()]
                self.outputDataframe[loader.lang["modules"]["evaluation"]["hausdorff"]] = [hausdorff(set1, set2)]
                self.outputDataframe[loader.lang["modules"]["evaluation"]["randindex"]] = [randindex(set1, set2)]
                p, r = precision_recall(set1, set2, margin=self.marginvar.get())
                self.outputDataframe[loader.lang["modules"]["evaluation"]["precision"]] = [p]
                self.outputDataframe[loader.lang["modules"]["evaluation"]["recall"]] = [r]
            else:
                self.argError()
        except ValueError:
            self.argError()

    def buildConfig(self, section: ttk.Frame):
        """Provides GUI elements for time series module configuration.

        :param section: GUI component where module configuration should be displayed.
        """  
        labset1 = Label(section, text=loader.lang["modules"]["evaluation"]["set1"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labset1.grid(row=1)
        if not self.set1var:
            self.set1var = StringVar()
            self.set1var.set("")
        set1entry = Entry(section, textvariable=self.set1var, width=int((section.winfo_width()-13)/7)+1)
        set1entry.grid(row=2)

        labset2 = Label(section, text=loader.lang["modules"]["evaluation"]["set2"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labset2.grid(row=3)
        if not self.set2var:
            self.set2var = StringVar()
            self.set2var.set("")
        set2entry = Entry(section, textvariable=self.set2var, width=int((section.winfo_width()-13)/7)+1)
        set2entry.grid(row=4)

        labmargin = Label(section, text=loader.lang["modules"]["evaluation"]["margin"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labmargin.grid(row=5)
        if not self.marginvar:
            self.marginvar = IntVar()
            self.marginvar.set(10.0)
        vcmd = (section.register(entryvalidators.validate_digit),'%P')
        marginentry = Entry(section, textvariable=self.marginvar, validate='all', validatecommand=vcmd, width=int((section.winfo_width()-13)/7)+1)
        marginentry.grid(row=6)