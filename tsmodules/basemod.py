from pandas.core.frame import DataFrame
from tkinter import *
from tkinter import ttk
import loader

class TSModule:
    name = "Unnamed Module"
    isactive = None

    def buildMenu(self, subsection: ttk.Frame):
        for widget in subsection.winfo_children():
            widget.destroy()
        subsection.update()

        moduleFrameHeader = Frame(subsection, width=subsection.winfo_width())
        moduleFrameHeader.grid(row=1)

        moduleFrameConfig = Frame(subsection, width=subsection.winfo_width())
        moduleFrameConfig.grid(row=2)

        moduleFrameHeader.update()
        moduleFrameConfig.update()

        self.buildCheckbox(subsection=moduleFrameHeader)
        self.buildConfig(subsection=moduleFrameConfig)

    def __init__(self, name):
        self.name = name

    def buildCheckbox(self, subsection: ttk.Frame):
        lab = Label(subsection, text=loader.lang["modules"]["isactive"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
        lab.grid(row=1)
        if not self.isactive:
            self.isactive = BooleanVar()
        moduleCheck = Checkbutton(subsection ,variable=self.isactive, onvalue=1, offvalue=0)
        moduleCheck.grid(row=2)

    def buildConfig(self, subsection: ttk.Frame):
        pass

    def displayModule(self, ax, plotdf):
        pass

    def getOutputDataframe(self) -> DataFrame:
        return DataFrame()

    def clearOutputDataframe(self):
        pass
