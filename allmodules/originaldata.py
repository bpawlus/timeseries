from loader import lang, appconfig, directories
from allmodules import basemod
from pandas.core.frame import DataFrame

class OriginalDataDisplayModule(basemod.ChartModule):
    outputDataframe = DataFrame()

    def getOutputDataframe(self) -> DataFrame:
        return self.outputDataframe

    def clearOutputDataframe(self):
        self.outputDataframe = DataFrame()

    def displayModule(self, ax, plotdf):
        origdf = plotdf[[col for col in plotdf.columns]].groupby(plotdf.columns[0]).sum()
        origdf.plot(kind='line', legend=True, ax=ax, color='r',marker='o', fontsize=4, markersize=2)
        self.outputDataframe = plotdf
