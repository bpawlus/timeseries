from pandas.core.frame import DataFrame
from tsmodules import basemod
import numpy as np
import ruptures as rpt
import math
import matplotlib.patches as patches
import loader
import entryvalidators
from tkinter import *
from tkinter import ttk

class RupturesModule(basemod.TSModule):
    """Class implementing change point detection algorithms in time series modules.
    """

    costDict = None
    """Dictionary of cost functions, that can be used to in change point detection algorithms."""
    costcbvar = None
    """Chosen cost function, that can be used to in change point detection algorithms."""
    penaltyvar = None
    """Linear penalty parameter. Value determines how many change points might detection algorithms find."""
    cpointsconsidervar = None
    """If number of change points is known, number of change points is taken as an argument instead of penalty value in change point detection algorithms."""
    cpointsvar = None
    """How many change points should be found in algorithm."""


    def displayModule(self, ax, plotdf: DataFrame):
        """Processes analyzing module and displays results on chart's axes.

        :param ax: Reference to plot's axes.
        :param plotdf: Data frame with original signal.
        """
        signal = np.array(plotdf[plotdf.columns[1]])
        cps = self.calculateChangePoints(signal)
        cps.insert(0,0)
        cps[len(cps)-1]
        cpstarts = []
        cpends = []
        means = []
        sigmas = []
        for c in range(len(cps)-1):
            mean = np.mean([signal[i] for i in range(cps[c], cps[c+1])])
            sum = 0
            for i in range(cps[c], cps[c+1]):
                sum += math.pow((signal[i] - mean),2)
            sum = sum/(cps[c+1]-cps[c]+1)
            sum = math.sqrt(sum)
            
            means.append(mean)
            sigmas.append(sum)
            cpstarts.append(plotdf[plotdf.columns[0]][cps[c]])
            cpends.append(plotdf[plotdf.columns[0]][cps[c+1]-1])

            start = plotdf[plotdf.columns[0]][cps[c]]
            width = plotdf[plotdf.columns[0]][cps[c+1]-1]-plotdf[plotdf.columns[0]][cps[c]]

            rect = patches.Rectangle((start, mean-sum), width, sum*2, linewidth=1, edgecolor=self.getDisplayColor(), facecolor='none')
            ax.add_patch(rect)

        self.outputDataframe[loader.lang["modules"]["changepoints"]["cpstart"]] = cpstarts
        self.outputDataframe[loader.lang["modules"]["changepoints"]["cpend"]] = cpends
        self.outputDataframe[loader.lang["modules"]["changepoints"]["means"]] = means
        self.outputDataframe[loader.lang["modules"]["changepoints"]["sigmas"]] = sigmas

    def calculateChangePoints(self, signal) -> list:
        """Method meant to be overwritten.
        Calculates change point indexes.

        :param signal: Time series data.
        :returns: Indexes of change points.
        """
        return []

    def buildConfig(self, section: ttk.Frame):
        """Provides GUI elements for time series module configuration.

        :param section: GUI component where module configuration should be displayed.
        """
        labcost = Label(section, text=loader.lang["modules"]["changepoints"]["costfcs"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labcost.grid(row=1)
        if not self.costcbvar:
            self.costcbvar = StringVar()
            self.costcbvar.set(loader.lang["modules"]["changepoints"]["costs"]["l1"])
        costcb = ttk.Combobox(section, state="readonly", textvariable=self.costcbvar, width=int((section.winfo_width()-13)/7)+1)
        costcb.grid(row=2)
        costcb['values'] = list(self.costDict.keys())
        

        labpenalty = Label(section, text=loader.lang["modules"]["changepoints"]["penalty"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labpenalty.grid(row=3)
        if not self.penaltyvar:
            self.penaltyvar = DoubleVar()
            self.penaltyvar.set(5.0)
        vcmd = (section.register(entryvalidators.validate_floatentries),'%P')
        penaltyentry = Entry(section, textvariable=self.penaltyvar, validate='all', validatecommand=vcmd, width=int((section.winfo_width()-13)/7)+1)
        cpyval = self.penaltyvar.get()
        penaltyentry.grid(row=4)

        labactive = Label(section, text=loader.lang["modules"]["changepoints"]["cpoints"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labactive.grid(row=5)
        if not self.cpointsconsidervar:
            self.cpointsconsidervar = BooleanVar()
        moduleCheck = Checkbutton(section ,variable=self.cpointsconsidervar, onvalue=1, offvalue=0)
        moduleCheck.grid(row=6)

        labcpoints = Label(section, text=loader.lang["modules"]["changepoints"]["cpointsconsider"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labcpoints.grid(row=7)
        if not self.cpointsvar:
            self.cpointsvar = IntVar()
            self.cpointsvar.set(1)
        vcmd = (section.register(entryvalidators.validate_digit),'%P')
        cpointsentry = Entry(section, textvariable=self.cpointsvar, validate='all', validatecommand=vcmd, width=int((section.winfo_width()-13)/7)+1)
        cpointsentry.grid(row=8)

        algoParams = Frame(section, width=section.winfo_width())
        algoParams.grid(row=9)

        algoParams.update()
        self.buildConfigAlgoParams(algoParams)

    def buildConfigAlgoParams(self, section: ttk.Frame):
        """Method meant to be overwritten.
        Provides GUI elements for specific change point detection algorithms' parameters.

        :param section: GUI component where specific parameters should be displayed.
        """

    def __init__(self, name) -> None:
        super().__init__(name)
        self.costDict = {
            loader.lang["modules"]["changepoints"]["costs"]["l1"]: "l1",
            loader.lang["modules"]["changepoints"]["costs"]["l2"]: "l2",
            loader.lang["modules"]["changepoints"]["costs"]["normal"]: "normal",
            loader.lang["modules"]["changepoints"]["costs"]["rbf"]: "rbf",
            loader.lang["modules"]["changepoints"]["costs"]["rank"]: "rank"
        }


class RupturesPeltModule(RupturesModule):
    """Class implementing Pelt algorithm that detects change points.
    """

    def calculateChangePoints(self, signal) -> list:
        """Calculates change point indexes.

        :param signal: Time series data.
        :returns: Indexes of change points.
        """
        algo = rpt.Pelt(model=self.costDict[self.costcbvar.get()]).fit(signal)
        if self.cpointsconsidervar.get():
            result = algo.predict(n_bkps=self.cpointsvar.get())
        else:
            result = algo.predict(pen=self.penaltyvar.get())
        return result
 
class RupturesBinsegModule(RupturesModule):
    """Class implementing Binary segmentaton algorithm that detects change points.
    """
    def calculateChangePoints(self, signal) -> list:
        """Calculates change point indexes.

        :param signal: Time series data.
        :returns: Indexes of change points.
        """
        algo = rpt.Binseg(model=self.costDict[self.costcbvar.get()]).fit(signal)
        if self.cpointsconsidervar.get():
            result = algo.predict(n_bkps=self.cpointsvar.get())
        else:
            result = algo.predict(pen=self.penaltyvar.get())
        return result

class RupturesWindowModule(RupturesModule):
    """Class implementing Window algorithm that detects change points.
    """

    widthvar = None
    """Length of the window."""

    def calculateChangePoints(self, signal) -> list:
        """Calculates change point indexes.

        :param signal: Time series data.
        :returns: Indexes of change points.
        """
        algo = rpt.Window(width=40, model=self.costDict[self.costcbvar.get()]).fit(signal)
        if self.cpointsconsidervar.get():
            result = algo.predict(n_bkps=self.cpointsvar.get())
        else:
            result = algo.predict(pen=self.penaltyvar.get())
        return result

    def buildConfigAlgoParams(self, section: ttk.Frame):
        """Provides GUI elements for specific change point detection algorithms' parameters.

        :param section: GUI component where specific parameters should be displayed.
        """
        labwidth = Label(section, text=loader.lang["modules"]["changepoints"]["window"]["width"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labwidth.grid(row=1)
        if not self.widthvar:
            self.widthvar = IntVar()
            self.widthvar.set(7)
        vcmd = (section.register(entryvalidators.validate_digit),'%P')
        widthentry = Entry(section, textvariable=self.widthvar, validate='all', validatecommand=vcmd, width=int((section.winfo_width()-13)/7)+1)
        widthentry.grid(row=2)

class RupturesBottomUpModule(RupturesModule):
    """Class implementing Bottom-Up algorithm that detects change points.
    """

    jumpvar = None
    """Value of Bottom-Up's grid size."""

    def calculateChangePoints(self, signal) -> list:
        """Calculates change point indexes.

        :param signal: Time series data.
        :returns: Indexes of change points.
        """
        algo = rpt.BottomUp(model=self.costDict[self.costcbvar.get()]).fit(signal)
        if self.cpointsconsidervar.get():
            result = algo.predict(n_bkps=self.cpointsvar.get())
        else:
            result = algo.predict(pen=self.penaltyvar.get())
        return result
