from pandas.core.frame import DataFrame
from tsmodules import basemod
import numpy as np
import ruptures as rpt
import math
import matplotlib.patches as patches
import loader
import entryvalidators
from tkinter import *
from tkinter import ttk, messagebox

class RupturesModule(basemod.TSModule):
    """Class implementing change point detection algorithms in time series modules.
    """

    __dictCost = None
    """Dictionary of cost functions, that can be used to in change point detection algorithms."""
    __outvarCost = None
    """Chosen cost function, that can be used to in change point detection algorithms."""
    __outvarPenalty = None
    """Linear penalty parameter. Value determines how many change points might detection algorithms find."""
    __outvarCPointsConsider = None
    """If number of change points is known, number of change points is taken as an argument instead of penalty value in change point detection algorithms."""
    __outvarCPoints = None
    """How many change points should be found in algorithm."""

    def getCostFunction(self) -> str:
        """ Returns chosen cost function, that can be used to in change point detection algorithms.
        
        :returns: Chosen cost function, that can be used to in change point detection algorithms.
        """
        if self.__dictCost and self.__outvarCost:
            return self.__dictCost[self.__outvarCost.get()]
        else:
            return "l1"

    def shouldConsiderCPoints(self) -> bool:
        """ Returns the indicator if number of change should be taken as an argument instead of penalty value in change point detection algorithms.
        
        :returns: The indicator if number of change should be taken as an argument instead of penalty value in change point detection algorithms.
        """
        return self.__outvarCPointsConsider.get()

    def getCPointsCount(self) -> int:
        """ Returns how many change points should be found in algorithm.
        
        :returns: How many change points should be found in algorithm.
        """
        return self.__outvarCPoints.get()

    def getLinearPenalty(self) -> float:
        """ Returns linear penalty parameter. Value determines how many change points might detection algorithms find.
        
        :returns: Linear penalty parameter. Value determines how many change points might detection algorithms find.
        """
        return self.__outvarPenalty.get()

    def displayModule(self, ax, plotdf: DataFrame):
        """Processes analyzing module and displays results on chart's axes.

        :param ax: Reference to plot's axes.
        :param plotdf: Data frame with original signal.
        """
        signal = np.array(plotdf[plotdf.columns[1]])
        if not self.shouldConsiderCPoints() or (self.shouldConsiderCPoints() and self.__outvarCPoints.get() <= np.size(signal)/10):
            cps = self.calculateChangePoints(signal)

            cps.insert(0,0)
            cps[len(cps)-1] -= 1
            cpstarts = []
            cpends = []
            cpstartsidx = []
            cpendsidx = []
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
                cpstartsidx.append(cps[c])
                cpends.append(plotdf[plotdf.columns[0]][cps[c+1]-1])
                cpendsidx.append(cps[c+1]-1)

                start = cps[c]
                width = cps[c+1]-cps[c]

                rect = patches.Rectangle((start, mean-sum), width, sum*2, linewidth=1, edgecolor=self.getDisplayColor(), facecolor='none')
                ax.add_patch(rect)

            self.outputDf[loader.lang["modules"]["changepoints"]["cpstart"]] = cpstarts
            self.outputDf[loader.lang["modules"]["changepoints"]["cpstartidx"]] = cpstartsidx
            self.outputDf[loader.lang["modules"]["changepoints"]["cpend"]] = cpends
            self.outputDf[loader.lang["modules"]["changepoints"]["cpendidx"]] = cpendsidx
            self.outputDf[loader.lang["modules"]["changepoints"]["means"]] = means
            self.outputDf[loader.lang["modules"]["changepoints"]["sigmas"]] = sigmas
        else:
            messagebox.showerror(loader.lang["messagebox"]["error"], loader.lang["modules"]["changepoints"]["toomanycp"]+str(math.floor(np.size(signal)/10)))

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
        labelCost = Label(section, text=loader.lang["modules"]["changepoints"]["costfcs"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labelCost.grid(row=1)
        if not self.__outvarCost:
            self.__outvarCost = StringVar()
            self.__outvarCost.set(loader.lang["modules"]["changepoints"]["costs"]["l1"])
        comboboxCost = ttk.Combobox(section, state="readonly", textvariable=self.__outvarCost, width=int((section.winfo_width()-13)/7)+1)
        comboboxCost.grid(row=2)
        comboboxCost['values'] = list(self.__dictCost.keys())
        

        labelPenalty = Label(section, text=loader.lang["modules"]["changepoints"]["penalty"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labelPenalty.grid(row=3)
        if not self.__outvarPenalty:
            self.__outvarPenalty = DoubleVar()
            self.__outvarPenalty.set(5.0)
        vcmd = (section.register(entryvalidators.validate_float_pos),'%P')
        entryPenalty = Entry(section, textvariable=self.__outvarPenalty, validate='all', validatecommand=vcmd, width=int((section.winfo_width()-13)/7)+1)
        entryPenalty.grid(row=4)

        labelCPointsConsider = Label(section, text=loader.lang["modules"]["changepoints"]["cpointsconsider"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labelCPointsConsider.grid(row=5)
        if not self.__outvarCPointsConsider:
            self.__outvarCPointsConsider = BooleanVar()
        checkCPointsConsider = Checkbutton(section ,variable=self.__outvarCPointsConsider, onvalue=1, offvalue=0)
        checkCPointsConsider.grid(row=6)

        labelCPoints = Label(section, text=loader.lang["modules"]["changepoints"]["cpoints"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labelCPoints.grid(row=7)
        if not self.__outvarCPoints:
            self.__outvarCPoints = IntVar()
            self.__outvarCPoints.set(1)
        vcmd = (section.register(entryvalidators.validate_int_pos),'%P')
        entryCPoints = Entry(section, textvariable=self.__outvarCPoints, validate='all', validatecommand=vcmd, width=int((section.winfo_width()-13)/7)+1)
        entryCPoints.grid(row=8)

        frameAlgoExtraParams = Frame(section, width=section.winfo_width())
        frameAlgoExtraParams.grid(row=9)

        frameAlgoExtraParams.update()
        self.buildConfigAlgoParams(frameAlgoExtraParams)

    def buildConfigAlgoParams(self, section: ttk.Frame):
        """Method meant to be overwritten.
        Provides GUI elements for specific change point detection algorithms' parameters.

        :param section: GUI component where specific parameters should be displayed.
        """

    def __init__(self, name) -> None:
        super().__init__(name)
        self.__dictCost = {
            loader.lang["modules"]["changepoints"]["costs"]["l1"]: "l1",
            loader.lang["modules"]["changepoints"]["costs"]["l2"]: "l2",
            loader.lang["modules"]["changepoints"]["costs"]["normal"]: "normal"
        }


class RupturesPeltModule(RupturesModule):
    """Class implementing Pelt algorithm that detects change points.
    """

    def calculateChangePoints(self, signal) -> list:
        """Calculates change point indexes.

        :param signal: Time series data.
        :returns: Indexes of change points.
        """
        algo = rpt.Pelt(model=self.getCostFunction()).fit(signal)
        if self.shouldConsiderCPoints():
            messagebox.showerror(loader.lang["messagebox"]["error"], loader.lang["modules"]["changepoints"]["pelt"]["unsupported"])
            return []
        else:
            result = algo.predict(pen=self.getLinearPenalty())
        return result
 
class RupturesBinsegModule(RupturesModule):
    """Class implementing Binary segmentaton algorithm that detects change points.
    """
    def calculateChangePoints(self, signal) -> list:
        """Calculates change point indexes.

        :param signal: Time series data.
        :returns: Indexes of change points.
        """
        algo = rpt.Binseg(model=self.getCostFunction()).fit(signal)
        if self.shouldConsiderCPoints():
            result = algo.predict(n_bkps=self.getCPointsCount())
        else:
            result = algo.predict(pen=self.getLinearPenalty())
        return result

class RupturesWindowModule(RupturesModule):
    """Class implementing Window algorithm that detects change points.
    """

    _outvarWidth = None
    """Length of the window."""

    def calculateChangePoints(self, signal) -> list:
        """Calculates change point indexes.

        :param signal: Time series data.
        :returns: Indexes of change points.
        """
        algo = rpt.Window(width=self._outvarWidth.get(), model=self.getCostFunction()).fit(signal)
        if self.shouldConsiderCPoints():
            result = algo.predict(n_bkps=self.getCPointsCount())
        else:
            result = algo.predict(pen=self.getLinearPenalty())
        return result

    def buildConfigAlgoParams(self, section: ttk.Frame):
        """Provides GUI elements for specific change point detection algorithms' parameters.

        :param section: GUI component where specific parameters should be displayed.
        """
        labelWidth = Label(section, text=loader.lang["modules"]["changepoints"]["window"]["width"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labelWidth.grid(row=1)
        if not self._outvarWidth:
            self._outvarWidth = IntVar()
            self._outvarWidth.set(7)
        vcmd = (section.register(entryvalidators.validate_int_pos),'%P')
        entryWidth = Entry(section, textvariable=self._outvarWidth, validate='all', validatecommand=vcmd, width=int((section.winfo_width()-13)/7)+1)
        entryWidth.grid(row=2)

class RupturesBottomUpModule(RupturesModule):
    """Class implementing Bottom-Up algorithm that detects change points.
    """

    def calculateChangePoints(self, signal) -> list:
        """Calculates change point indexes.

        :param signal: Time series data.
        :returns: Indexes of change points.
        """
        algo = rpt.BottomUp(model=self.getCostFunction()).fit(signal)
        if self.shouldConsiderCPoints():
            result = algo.predict(n_bkps=self.getCPointsCount())
        else:
            result = algo.predict(pen=self.getLinearPenalty())
        return result
