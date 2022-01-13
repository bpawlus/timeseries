import logger
from tkinter import *
from tkinter import ttk, messagebox
import pandas as pd
from pandas import DataFrame

import loader
from importers import baseimport

class CsvImportMethod(baseimport.ImportMethod):
    """Class responsible for loading time series data from .csv files.
    """

    __xseries = None
    """Chosen X-axis name from chosen sheet"""
    __yseries = None
    """Chosen Y-axis name from chosen sheet."""
    __datax = []
    """Loaded X-axis data. Should contain indexes with constant intervals."""
    __datay = []
    """Loaded Y-axis data. Should data of observed phenomenon."""
    __xseriesprovided = False
    """Auxiliary variable, determines if user provided X-axis data."""
    __yseriesprovided = False
    """Auxiliary variable, determines if user provided Y-axis data."""

    def onXYprovided(self):
        """Determines behaviour of import method's GUI behaviour when X and Y axis data are provided.
        """
        if(self.__xseries.get() != self.__yseries.get()):
            data = pd.read_csv(self.directory, usecols=(self.__xseries.get(), self.__yseries.get())).values.tolist()
            self.__datax = [item[0] for item in data]
            self.__datay = [item[1] for item in data]

            for i in self.preview.get_children():
                self.preview.delete(i)
            for v in data:
                self.preview.insert('', END, values=v)
        else:
            for i in self.preview.get_children():
                self.preview.delete(i)
            self.__datax.clear()
            self.__datay.clear()

    def onXchange(self, event):
        """Determines behaviour of import method's GUI behaviour when X axis data is provided.
        """
        self.preview.column("x", anchor=CENTER)
        self.preview.heading("x",text=self.__xseries.get(),anchor=CENTER)
        self.__xseriesprovided = True
        if self.__xseriesprovided and self.__yseriesprovided:
            self.onXYprovided()          

    def onYchange(self, event):
        """Determines behaviour of import method's GUI behaviour when Y axis data is provided.
        """
        self.preview.column("y", anchor=CENTER)
        self.preview.heading("y",text=self.__yseries.get(),anchor=CENTER)
        self.__yseriesprovided = True
        if self.__xseriesprovided and self.__yseriesprovided:
            self.onXYprovided()

    def importSettingsGui(self, section: ttk.Frame):
        """Provides GUI elements for selection of specific signal from provided data.
        """
        logger.log("Started importing CSV file from: " + self.directory)
        
        pre = pd.read_csv(self.directory)

        labxseries = Label(section, text=loader.lang["importer-csv"]["xseries"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labxseries.grid(row=1)
        self.__xseries = StringVar()
        xseriescb = ttk.Combobox(section, state="readonly", textvariable=self.__xseries, width=int((section.winfo_width()-13)/7)+1)
        xseriescb.set("")
        xseriescb['values'] = pre.columns.values.tolist()
        xseriescb.grid(row=2)

        labyseries = Label(section, text=loader.lang["importer-csv"]["yseries"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labyseries.grid(row=3)
        self.__yseries = StringVar()
        yseriescb = ttk.Combobox(section, state="readonly", textvariable=self.__yseries, width=int((section.winfo_width()-13)/7)+1)
        yseriescb.set("")
        yseriescb['values'] = pre.columns.values.tolist()
        yseriescb.grid(row=4)

        labpreview = Label(section, text=loader.lang["importer-csv"]["preview"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labpreview.grid(row=5)

        self.preview = ttk.Treeview(section)
        self.preview['columns'] = ("x", "y")
        self.preview.column("#0", width=0, stretch=NO)
        self.preview.column("x", anchor=CENTER, width=int(section.winfo_width()/2))
        self.preview.column("y", anchor=CENTER, width=int(section.winfo_width()/2))
        self.preview.heading("#0",text="",anchor=CENTER)
        self.preview.heading("x",text="",anchor=CENTER)
        self.preview.heading("y",text="",anchor=CENTER)
        self.preview.grid(row=6)

        xseriescb.bind('<<ComboboxSelected>>', self.onXchange)  
        yseriescb.bind('<<ComboboxSelected>>', self.onYchange)    

        self.__xseriesprovided = False
        self.__yseriesprovided = False

    def extractData(self) -> DataFrame:
        """Extracts signal from provided data.
        
        :returns: Data frame of single, selected time series.
        """
        if(len(self.__datax) and len(self.__datay)):
            logger.log("Importing XLS columns (X/Y): " + self.__xseries.get() + "/" + self.__yseries.get())
            data = {
                f'{self.__xseries.get()}': self.__datax,
                f'{self.__yseries.get()}': self.__datay
            }
            messagebox.showinfo(loader.lang["messagebox"]["info"], loader.lang["importer-csv"]["successimport"])
            return DataFrame(data,columns=[self.__xseries.get(),self.__yseries.get()])
        else:
            messagebox.showerror(loader.lang["messagebox"]["error"], loader.lang["importer-csv"]["wrongimport"])
            return DataFrame()
