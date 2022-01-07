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
import logger
import loader
from tsmodules import basemod
from tsmodules import originaldata
from tsmodules import rollingmean
from tsmodules import rollingstd
from tsmodules import differentation
from tsmodules import autocorrelation
from tsmodules import seasonaldecompose
from tsmodules import rupturesmods

"""
class ChangePointAreas(ChartModule):
    cpCount = 10
    useOwnCpCount = bool(0)
    outputDataframe = DataFrame()

    def getOutputDataframe(self) -> DataFrame:
        return self.outputDataframe

    def clearOutputDataframe(self):
        self.outputDataframe = DataFrame()

    def scoring(self, data, i: int, j: int) -> float:
        sum = 0
        for s in range(i, j):
            sum += abs(data[s]-np.mean([data[s] for s in range(i, j)]))
        return sum
    
    def calculateCPcount(self, data, count, opt_part):
        bic = np.zeros(count)
        mse = np.zeros(count)
        n = len(data)

        for i in range(count):
            opt_part_i = opt_part[i][0:i+1]

            if opt_part_i[i] == n-1:
                break
            else:
                change_points = [0]
                change_points.extend(opt_part_i)
                change_points.append(n-1)

            means = np.zeros(n)
            j = 0
            for j in range(i+1):
                beg = change_points[j]
                end = change_points[j+1]+1
                first = data[beg:end+1]
                u = np.ones(len(first))
                means[beg:end+1] = u*np.mean(first)

            first = data[change_points[j+1]:change_points[j+2]+1]
            u = np.ones(len(first))
            means[change_points[j+1]:change_points[j+2]+1] = u*np.mean(first)

            for ii in range(n):
                mse[i] += abs(data[ii]/means[ii]-1)
            bic[i] = math.log(mse[i])*n+(i+1)*math.log(n)

        bic = bic.tolist()
        mse = mse.tolist()

        bic.insert(0,bic[0])
        mse[0] = 0
        for ii in range(n):
            mse[0] += abs(data[ii]-1)
        bic[0] = math.log(mse[0])*n

        minbic = min(bic)
        return bic.index(minbic)

    def calculateCPpositions(self, data, count):
        Q = np.zeros(count)
        N = len(data)

        p_opt_idx = np.zeros(N)
        p_aux = np.zeros(N)
        opt_pals=np.zeros((count,N), dtype=int)

        for k in range(N):
            p_opt_idx[k] = self.scoring(data, k, N)

        for kster in range(1, count+1):
            for kk in range(1,N-kster+1):
                for jj in range(kk+1,N-kster+1+1):
                    p_aux[jj-1] = self.scoring(data, kk-1, jj-2+1) + p_opt_idx[jj-1]

                reshaped = [p_aux[i-1] for i in range(kk+1,N-kster+1+1)]
                mm = min(reshaped)
                ix = reshaped.index(mm)
                p_opt_idx[kk-1]=mm
                opt_pals[kster-1][kk-1]=kk+ix
            Q[kster-1] = p_opt_idx[0]

        opt_part=np.zeros((count,count), dtype=int)
        for i in range(1,count+1):
            opt_part[i-1][0]=opt_pals[i-1][0]
            for kster in range(i-1,0,-1):
                opt_part[i-1][i-kster]=opt_pals[kster-1][opt_part[i-1][i-kster-1]]

        return Q, opt_part

    def displayModule(self, ax, plotdf):
        plotdf = plotdf[[col for col in plotdf.columns]].groupby(plotdf.columns[0]).sum()
        data = [value[0] for value in plotdf.values]
        indexes = [value for value in plotdf.index]
        count = 10
        
        if(self.useOwnCpCount.get()):
            count=self.cpCount-1
            #count=4
        else:
            #print("Tu dodatkowe obliczenia")
            #return
            Q, opt_part = self.calculateCPpositions(data, count)
            count = self.calculateCPcount(data, count, opt_part)
        
        #Q = np.array([89.80459545, 85.48421212, 79.19482971, 74.85958911, 67.84495274, 63.52456941, 61.93539294, 59.71509466, 57.68162371, 55.99978486])
        #opt_part = [[40,0,0,0,0,0,0,0,0,0],[12,40,0,0,0,0,0,0,0,0],[40,74,87,0,0,0,0,0,0,0],[40,74,87,99,0,0,0,0,0,0],[40,74,87,98,99,0,0,0,0,0],[12,40,74,87,98,99,0,0,0,0],[12,40,62,74,87,98,99,0,0,0],[12,40,74,87,96,97,98,99,0,0],[12,40,53,54,62,74,87,98,99,0],[12,40,52,62,74,87,96,97,98,99]]
        Q, opt_part = self.calculateCPpositions(data, count)
        #opt_part = [[40,0,0,0],[12,40,0,0],[40,74,87,0],[40,74,87,99]]
        change_points = [0]
        change_points.extend(opt_part[count-1])
        change_points.append(len(data)-1)

        cps = []
        cpe = []
        means = []
        sigmas = []
        for c in range(len(change_points)-1):
            mean = np.mean([data[s] for s in range(change_points[c], change_points[c+1])])
            sum = 0
            for i in range(change_points[c], change_points[c+1]):
                sum += math.pow((data[i] - mean),2)
            sum = sum/(change_points[c+1]-change_points[c]+1)
            sum = math.sqrt(sum)
            
            rect = patches.Rectangle((change_points[c], mean-sum), change_points[c+1]-change_points[c], sum*2, linewidth=2, edgecolor='#FFFF00', facecolor='none')
            ax.add_patch(rect)

            cps.append(indexes[change_points[c]])
            cpe.append(indexes[change_points[c+1]-1])
            means.append(mean)
            sigmas.append(sum)

        self.outputDataframe[lang["modules"]["changepoints"]["cpstart"]] = cps
        self.outputDataframe[lang["modules"]["changepoints"]["cpend"]] = cpe
        self.outputDataframe[lang["modules"]["changepoints"]["means"]] = means
        self.outputDataframe[lang["modules"]["changepoints"]["sigmas"]] = sigmas

    def buildConfig(self, subsection: ttk.Frame):
        global lang
        labuseown = Label(subsection, text=lang["modules"]["changepoints"]["useowncpcount"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
        labuseown.grid(row=1)
        if not self.useOwnCpCount:
            self.useOwnCpCount = BooleanVar()
        useOwnCpCountBut = Checkbutton(subsection ,variable=self.useOwnCpCount, onvalue=1, offvalue=0)
        useOwnCpCountBut.grid(row=2)

        labpoints = Label(subsection, text=lang["modules"]["changepoints"]["cpcount"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
        labpoints.grid(row=3)
        changePointCount = Scale(subsection, from_=2, to=20, tickinterval=9, orient=HORIZONTAL, length=int(subsection.winfo_width()))
        changePointCount.set(self.cpCount)
        changePointCount.grid(row=4)

        def updateChangePointCount(event):
            self.cpCount = int(changePointCount.get())

        changePointCount.bind("<ButtonRelease-1>", updateChangePointCount)
"""

class HubTSModules:
    """Class with methods concerning loaded data in form of charts.
    """
    allModules = []
    """List containing all loaded time series modules."""

    def addModule(self, module: basemod.TSModule):
        """Adds time series module to list.

        :param module: Time series module to add.
        """
        self.allModules.append(module)

    def displayModules(self, ax, plotdf):
        """Displays all selected modules' patches on selected plot.

        :param ax: Reference to plot's axes.
        :param plotdf: Data frame with original signal.
        """
        for module in self.allModules:
            module.clearOutputDataframe()
            if module.isactive and module.isactive.get():
                logger.log("Displaying module: " + module.name)
                module.displayModule(ax, plotdf)

    def getAllActiveModules(self):
        """Returns all active time series modules.

        :returns: Requested list.
        """
        return [mod for mod in self.allModules if mod.isactive and mod.isactive.get() and not mod.getOutputDataframe().empty]

    def getAllActiveModuleNames(self):
        """Returns all active time series module names.

        :returns: Requested list.
        """
        return [mod.name for mod in self.allModules if mod.isactive and mod.isactive.get() and not mod.getOutputDataframe().empty]

    def getModuleByName(self, name: str) -> basemod.TSModule:
        """Returns module of argument's name.
        
        :param name: Name of the module.
        :returns: Requested module.
        """
        return next(mod for mod in self.allModules if name == mod.name)

    def loadModules(self):
        """Loads the list with all provided modules.
        """
        self.addModule(originaldata.OriginalDataDisplayModule(loader.lang["modules"]["display"]["header"]))
        self.addModule(rollingmean.RollingMeanModule(loader.lang["modules"]["rollingmean"]["header"]))
        self.addModule(rollingstd.RollingStdModule(loader.lang["modules"]["rollingstd"]["header"]))
        self.addModule(differentation.DifferentiationModule(loader.lang["modules"]["differentiation"]["header"]))
        self.addModule(autocorrelation.AutocorrelationModule(loader.lang["modules"]["autocorrelation"]["header"]))
        self.addModule(seasonaldecompose.SeasonalDecomposeModule(loader.lang["modules"]["seasonaldecompose"]["header"]))
        self.addModule(rupturesmods.RupturesBinsegModule(loader.lang["modules"]["rupturemods"]["binseg"]["header"]))
        self.addModule(rupturesmods.RupturesDynpModule(loader.lang["modules"]["rupturemods"]["dynp"]["header"]))
        self.addModule(rupturesmods.RupturesPeltModule(loader.lang["modules"]["rupturemods"]["pelt"]["header"]))
        self.addModule(rupturesmods.RupturesWindowModule(loader.lang["modules"]["rupturemods"]["window"]["header"]))
