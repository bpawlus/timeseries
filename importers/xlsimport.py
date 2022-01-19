import logger
from tkinter import *
from tkinter import ttk, messagebox
import pandas as pd
from pandas import DataFrame

from importers import baseimport
import loader

class XlsImportMethod(baseimport.ImportMethod):
    """Class responsible for loading time series data from .xls files.
    """

    __xSeries = None
    """Chosen X-axis name from chosen sheet"""
    __ySeries = None
    """Chosen Y-axis name from chosen sheet."""
    __sheet = None
    """Chosen sheet name from spreadsheet."""
    __datax = []
    """Loaded X-axis data. Should contain indexes with constant intervals."""
    __datay = []
    """Loaded Y-axis data. Should data of observed phenomenon."""
    __xSeriesProvided = False
    """Auxiliary variable, determines if user provided X-axis data."""
    __ySeriesProvided = False
    """Auxiliary variable, determines if user provided Y-axis data."""

    def onXYprovided(self):
        """Determines behaviour of import method's GUI behaviour when X and Y axis data are provided.
        """
        if(self.__xSeries.get() != self.__ySeries.get()):
            data = pd.read_excel(self.getDirectory(), sheet_name=self.__sheet.get(), usecols=(self.__xSeries.get(), self.__ySeries.get())).values.tolist()
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
        self.preview.heading("x",text=self.__xSeries.get(),anchor=CENTER)
        self.__xSeriesProvided = True
        if self.__xSeriesProvided and self.__ySeriesProvided:
            self.onXYprovided()

    def onYchange(self, event):
        """Determines behaviour of import method's GUI behaviour when Y axis data is provided.
        """
        self.preview.column("y", anchor=CENTER)
        self.preview.heading("y",text=self.__ySeries.get(),anchor=CENTER)
        self.__ySeriesProvided = True
        if self.__xSeriesProvided and self.__ySeriesProvided:
            self.onXYprovided()

    def onSheetChange(self, event):
        """Determines behaviour of import method's GUI behaviour when sheet is chosen.
        """
        df = pd.read_excel(self.getDirectory(), sheet_name=self.__sheet.get())

        self.__xSeriesProvided = False
        self.__ySeriesProvided = False

        self.__xSeriescb.set("")
        self.__ySeriescb.set("")
        self.__xSeriescb['state'] = "readonly"
        self.__ySeriescb['state'] = "readonly"
        self.__xSeriescb['values'] = df.columns.values.tolist()
        self.__ySeriescb['values'] = df.columns.values.tolist()

        self.preview.column("x", anchor=CENTER)
        self.preview.column("y", anchor=CENTER)
        self.preview.heading("x",text="",anchor=CENTER)
        self.preview.heading("y",text="",anchor=CENTER)

        for i in self.preview.get_children():
            self.preview.delete(i)
        self.__datax.clear()
        self.__datay.clear()

    def importSettingsGui(self, section: ttk.Frame):
        """Provides GUI elements for selection of specific signal from provided data.
        """
        logger.log("Started importing XLS file from: " + self.getDirectory())
        
        pre = pd.ExcelFile(self.getDirectory())

        labsheet = Label(section, text=loader.lang["importer-xls"]["sheets"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labsheet.grid(row=1)
        self.__sheet = StringVar()
        sheetcb = ttk.Combobox(section, state="readonly", textvariable=self.__sheet, width=int((section.winfo_width()-13)/7)+1)
        sheetcb['values'] = pre.sheet_names
        sheetcb.grid(row=2)

        labxseries = Label(section, text=loader.lang["importer-xls"]["xseries"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labxseries.grid(row=3)
        self.__xSeries = StringVar()
        self.__xSeriescb = ttk.Combobox(section, state="disabled", textvariable=self.__xSeries, width=int((section.winfo_width()-13)/7)+1)
        self.__xSeriescb.grid(row=4)

        labyseries = Label(section, text=loader.lang["importer-xls"]["yseries"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labyseries.grid(row=5)
        self.__ySeries = StringVar()
        self.__ySeriescb = ttk.Combobox(section, state="disabled", textvariable=self.__ySeries, width=int((section.winfo_width()-13)/7)+1)
        self.__ySeriescb.grid(row=6)

        labpreview = Label(section, text=loader.lang["importer-xls"]["preview"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labpreview.grid(row=7)

        self.preview = ttk.Treeview(section)
        self.preview['columns'] = ("x", "y")
        self.preview.column("#0", width=0, stretch=NO)
        self.preview.column("x", anchor=CENTER, width=int(section.winfo_width()/2))
        self.preview.column("y", anchor=CENTER, width=int(section.winfo_width()/2))
        self.preview.heading("#0",text="",anchor=CENTER)
        self.preview.heading("x",text="",anchor=CENTER)
        self.preview.heading("y",text="",anchor=CENTER)
        self.preview.grid(row=8)

        self.__xSeriescb.bind('<<ComboboxSelected>>', self.onXchange)            
        self.__ySeriescb.bind('<<ComboboxSelected>>', self.onYchange)    
        sheetcb.bind('<<ComboboxSelected>>', self.onSheetChange)    

    def extractData(self) -> DataFrame:
        """Extracts signal from provided data.
        
        :returns: Data frame of single, selected time series.
        """
        if(len(self.__datax) and len(self.__datay)):
            logger.log("Importing XLS columns (X/Y): " + self.__xSeries.get() + "/" + self.__ySeries.get() + " from sheet " + self.__sheet.get())
            data = {
                f'{self.__xSeries.get()}': self.__datax,
                f'{self.__ySeries.get()}': self.__datay
            }

            messagebox.showinfo(loader.lang["messagebox"]["info"], loader.lang["importer-xls"]["successimport"])
            return DataFrame(data,columns=[self.__xSeries.get(),self.__ySeries.get()])
        else:
            messagebox.showerror(loader.lang["messagebox"]["error"], loader.lang["importer-xls"]["wrongimport"])
            return DataFrame()
