from tsmodules import basemod
from pandas.core.frame import DataFrame
from tkinter import *
from tkinter import ttk
import loader

class RollingMeanModule(basemod.TSModule):
    rollCount = 5
    outputDataframe = DataFrame()

    def getOutputDataframe(self) -> DataFrame:
        return self.outputDataframe

    def clearOutputDataframe(self):
        self.outputDataframe = DataFrame()

    def displayModule(self, ax, plotdf):
        dfrolling = plotdf.rename(columns={f'{plotdf.columns[1]}': f'{plotdf.columns[1]} {loader.lang["modules"]["rollingmean"]["rollingdisplay"]} {self.rollCount}'})
        self.outputDataframe[plotdf.columns[0]] = [v[0] for v in plotdf.values]
        dfrolling = dfrolling[[col for col in dfrolling.columns]].groupby(dfrolling.columns[0]).sum()
        dfrolling = dfrolling.rolling(self.rollCount).mean()
        self.outputDataframe[plotdf.columns[1]] = [v[0] for v in dfrolling.values]
        dfrolling.plot(kind='line', legend=True, ax=ax, color='b',marker='o', fontsize=5, markersize=2)

    def buildConfig(self, subsection: ttk.Frame):
        labroll = Label(subsection, text=loader.lang["modules"]["rollingmean"]["count"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
        labroll.grid(row=1)
        rollCountScale = Scale(subsection, from_=2, to=16, tickinterval=7, orient=HORIZONTAL, length=int(subsection.winfo_width()))
        rollCountScale.set(self.rollCount)
        rollCountScale.grid(row=2)

        def updateChangePointCount(event):
            self.rollCount = int(rollCountScale.get())

        rollCountScale.bind("<ButtonRelease-1>", updateChangePointCount)
    