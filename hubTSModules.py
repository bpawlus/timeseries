"""
from tkinter import *
from tkinter import ttk
import numpy as np
import matplotlib.patches as patches
import math
import colorsys
import statsmodels.api as sm
from pandas.core.frame import DataFrame
import pandas as pd
"""
from pandas.core.frame import DataFrame
import logger
import loader
from tsmodules import basemod
from tsmodules import originaldata
from tsmodules import rollingmean
from tsmodules import rollingstd
from tsmodules import differentation
from tsmodules import autocorrelation
from tsmodules import decompose
from tsmodules import rupturesmods
from tsmodules import ruptureeval

class HubTSModules:
    """Class with methods concerning loaded data in form of charts.
    """

    __allModules = None
    """List containing all loaded time series modules."""

    def getAllModules(self):
        return self.__allModules

    def displayModules(self, ax, plotdf):
        """Displays all selected modules' patches on selected plot.

        :param ax: Reference to plot's axes.
        :param plotdf: Data frame with original signal.
        """
        for module in self.__allModules:
            module.outputDf = DataFrame()
            if module.isModelActive():
                logger.log("Displaying module: " + module.getModuleName())
                module.displayModule(ax, plotdf)

    def getAllActiveModules(self):
        """Returns all active time series modules.

        :returns: Requested list.
        """
        return [mod for mod in self.__allModules if mod.isModelActive() and not mod.outputDf.empty]

    def getAllActiveModuleNames(self):
        """Returns all active time series module names.

        :returns: Requested list.
        """
        return [mod.getModuleName() for mod in self.__allModules if mod.isModelActive() and not mod.outputDf.empty]

    def getModuleByName(self, name: str) -> basemod.TSModule:
        """Returns module of argument's name.
        
        :param name: Name of the module.
        :returns: Requested module.
        """
        return next(mod for mod in self.__allModules if name == mod.getModuleName())

    def getAllModuleNames(self):
        """Returns all module names.
        
        :returns: All module names.
        """
        return [mod.getModuleName() for mod in self.__allModules]

    def addModule(self, module: basemod.TSModule):
        """Adds time series module to list.

        :param module: Time series module to add.
        """
        self.__allModules.append(module)

    def loadModules(self):
        """Loads the list with all provided modules.
        """
        self.addModule(originaldata.OriginalDataDisplayModule(loader.lang["modules"]["display"]["header"]))
        self.addModule(rollingmean.RollingMeanModule(loader.lang["modules"]["rollingmean"]["header"]))
        self.addModule(rollingstd.RollingStdModule(loader.lang["modules"]["rollingstd"]["header"]))
        self.addModule(differentation.DifferentiationModule(loader.lang["modules"]["differentiation"]["header"]))
        self.addModule(autocorrelation.AutocorrelationsModule(loader.lang["modules"]["autocorrelations"]["header"]))
        self.addModule(decompose.DecomposeModule(loader.lang["modules"]["decompose"]["header"]))
        self.addModule(rupturesmods.RupturesBinsegModule(loader.lang["modules"]["changepoints"]["binseg"]["header"]))
        self.addModule(rupturesmods.RupturesBottomUpModule(loader.lang["modules"]["changepoints"]["botup"]["header"]))
        self.addModule(rupturesmods.RupturesPeltModule(loader.lang["modules"]["changepoints"]["pelt"]["header"]))
        self.addModule(rupturesmods.RupturesWindowModule(loader.lang["modules"]["changepoints"]["window"]["header"]))
        self.addModule(ruptureeval.RupturesEvaluation(loader.lang["modules"]["evaluation"]["header"]))

    def __init__(self) -> None:
        self.__allModules = []
