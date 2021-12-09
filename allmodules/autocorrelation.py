from loader import lang, appconfig, directories
from allmodules import basemod
from pandas.core.frame import DataFrame
from tkinter import *
from tkinter import ttk

class AutocorrelationModule(basemod.ChartModule):
    outputDataframe = DataFrame()
    lagentryvar = None

    def getOutputDataframe(self) -> DataFrame:
        return self.outputDataframe

    def clearOutputDataframe(self):
        self.outputDataframe = DataFrame()

    def displayModule(self, ax, plotdf):
        if self.lagentryvar.get() > 0: 
            self.outputDataframe[lang["modules"]["autocorrelation"]["lag"]] = [i+1 for i in range(0, int(self.lagentryvar.get()))]

            autocorrs = []
            for i in range(0,self.lagentryvar.get()):
                autocorrs.append(plotdf[plotdf.columns[1]].autocorr(lag=i+1))
            self.outputDataframe[lang["modules"]["autocorrelation"]["corr"]] = autocorrs

    def buildConfig(self, subsection: ttk.Frame):
        lablag = Label(subsection, text=lang["modules"]["autocorrelation"]["lag"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
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

    def validate_lagentry(self, val):
        if str.isdigit(val) or val == "":
            return True
        else:
            return False
