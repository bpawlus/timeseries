from tsmodules import basemod
from pandas.core.frame import DataFrame
from tkinter import *
from tkinter import ttk
import statsmodels.api as sm
import pandas as pd
import loader

class SeasonalDecomposeModule(basemod.TSModule):
    outputDataframe = DataFrame()
    lagentryvar = None
    componentsvarlist = []
    componentslist = ["lag", "trend", "resid"]

    def getOutputDataframe(self) -> DataFrame:
        return self.outputDataframe

    def clearOutputDataframe(self):
        self.outputDataframe = DataFrame()

    def displayModule(self, ax, plotdf):
        if self.lagentryvar.get() > 0:

            self.outputDataframe[plotdf.columns[0]]= plotdf[plotdf.columns[0]]

            series = pd.Series(x for x in plotdf[plotdf.columns[1]])
            res = sm.tsa.seasonal_decompose(series.values, period=self.lagentryvar.get())
            reslist = [res.seasonal, res.trend, res.resid, res.observed]
            i=0
            for comp in self.componentslist:
                if self.componentsvarlist[i].get():
                    self.outputDataframe[plotdf.columns[0] + " " + loader.lang["modules"]["seasonaldecompose"][comp]] = reslist[i]
                i+=1
        
        if len(self.outputDataframe.columns) > 1:
            origdf = self.outputDataframe.dropna()
            print("origdf", origdf)
            origdf = self.outputDataframe[[col for col in self.outputDataframe.columns]].groupby(self.outputDataframe.columns[0]).sum()
            origdf.plot(kind='line', legend=True, ax=ax, color='y',marker='o', fontsize=4, markersize=2)

    def buildConfig(self, subsection: ttk.Frame):
        lablag = Label(subsection, text=loader.lang["modules"]["seasonaldecompose"]["lag"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
        lablag.grid(row=1)

        if not self.lagentryvar:
            self.lagentryvar = IntVar()
            self.lagentryvar.set(1)

        vcmd = (subsection.register(self.validate_lagentry),'%P')
        lagentry = Entry(subsection, textvariable=self.lagentryvar, validate='all', validatecommand=vcmd, width=int((subsection.winfo_width()-13)/7)+1)
        cpyval = self.lagentryvar.get()
        lagentry.delete(0,END)
        lagentry.insert(0,cpyval)
        lagentry.grid(row=2)

        i = 0
        for comp in self.componentslist:
            labcomp = Label(subsection, text=loader.lang["modules"]["seasonaldecompose"]["show"]+" "+loader.lang["modules"]["seasonaldecompose"][comp], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
            labcomp.grid(row=(i*2)+3)
            if len(self.componentsvarlist) != 3:
                self.componentsvarlist.append(BooleanVar())
            compbtn = Checkbutton(subsection ,variable=self.componentsvarlist[i], onvalue=1, offvalue=0)
            compbtn.grid(row=(i*2)+4)
            i+=1


    def validate_lagentry(self, val):
        if str.isdigit(val) or val == "":
            return True
        else:
            return False
