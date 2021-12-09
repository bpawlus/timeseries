from loader import lang, appconfig, directories
from allmodules import basemod
from pandas.core.frame import DataFrame

class DifferentiationModule(basemod.ChartModule):
    outputDataframe = DataFrame()

    def getOutputDataframe(self) -> DataFrame:
        return self.outputDataframe

    def clearOutputDataframe(self):
        self.outputDataframe = DataFrame()

    def displayModule(self, ax, plotdf):
        df = plotdf.rename(columns={f'{plotdf.columns[1]}': f'{plotdf.columns[1]} {lang["modules"]["differentiation"]["diffdisplay"]}'})
        self.outputDataframe[plotdf.columns[0]] = [v[0] for v in plotdf.values]
        df = df[[col for col in df.columns]].groupby(df.columns[0]).sum()
        self.outputDataframe[plotdf.columns[1]] = [v[0] for v in df.values]
        df.diff().plot(kind='line', legend=True, ax=ax, color='g',marker='o', fontsize=5, markersize=2)
