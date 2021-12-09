from loader import lang, appconfig, directories
from allmodules import basemod
from pandas.core.frame import DataFrame
import numpy as np
import ruptures as rpt
import math
import matplotlib.patches as patches
import matplotlib.dates as mdates

class RupturesModule(basemod.ChartModule):
    outputDataframe = DataFrame()

    def getOutputDataframe(self) -> DataFrame:
        return self.outputDataframe

    def clearOutputDataframe(self):
        self.outputDataframe = DataFrame()

    def displayModule(self, ax, plotdf):
        points = np.array(plotdf[plotdf.columns[1]])
        cps = self.calculateChangePoints(points)
        cps.insert(0,0)
        cps[len(cps)-1]
        cpstarts = []
        cpends = []
        means = []
        sigmas = []
        print("cps", cps)
        for c in range(len(cps)-1):
            mean = np.mean([points[i] for i in range(cps[c], cps[c+1])])
            sum = 0
            for i in range(cps[c], cps[c+1]):
                sum += math.pow((points[i] - mean),2)
            sum = sum/(cps[c+1]-cps[c]+1)
            sum = math.sqrt(sum)
            
            means.append(mean)
            sigmas.append(sum)
            cpstarts.append(plotdf[plotdf.columns[0]][cps[c]])
            cpends.append(plotdf[plotdf.columns[0]][cps[c+1]-1])

            start = plotdf[plotdf.columns[0]][cps[c]]
            width = plotdf[plotdf.columns[0]][cps[c+1]-1]-plotdf[plotdf.columns[0]][cps[c]]

            rect = patches.Rectangle((start, mean-sum), width, sum*2, linewidth=1, edgecolor='#0000FF', facecolor='none')
            ax.add_patch(rect)


        self.outputDataframe[lang["modules"]["changepoints"]["cpstart"]] = cpstarts
        self.outputDataframe[lang["modules"]["changepoints"]["cpend"]] = cpends
        self.outputDataframe[lang["modules"]["changepoints"]["means"]] = means
        self.outputDataframe[lang["modules"]["changepoints"]["sigmas"]] = sigmas
        pass

    def calculateChangePoints(self, points) -> list:
        return []

class RupturesPeltModule(RupturesModule):
    def calculateChangePoints(self, points) -> list:
        model="rbf"
        algo = rpt.Pelt(model=model).fit(points)
        result = algo.predict(pen=10)
        return result
 
class RupturesBinsegModule(RupturesModule):
    def calculateChangePoints(self, points) -> list:
        model = "l2"  
        algo = rpt.Binseg(model=model).fit(points)
        result = algo.predict(n_bkps=10)
        return result

class RupturesWindowModule(RupturesModule):
    def calculateChangePoints(self, points) -> list:
        model = "l2" 
        algo = rpt.Window(width=40, model=model).fit(points)
        result = algo.predict(n_bkps=10)
        return result

class RupturesDynpModule(RupturesModule):
    def calculateChangePoints(self, points) -> list:
        model = "l1"  
        algo = rpt.Dynp(model=model, min_size=3, jump=5).fit(points)
        result = algo.predict(n_bkps=10)
        return result