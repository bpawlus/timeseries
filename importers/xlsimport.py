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

    __xseries = None
    """Chosen X-axis name from chosen sheet"""
    __yseries = None
    """Chosen Y-axis name from chosen sheet."""
    __sheet = None
    """Chosen sheet name from spreadsheet."""
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
            data = pd.read_excel(self.directory, sheet_name=self.__sheet.get(), usecols=(self.__xseries.get(), self.__yseries.get())).values.tolist()
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

    def onSheetChange(self, event):
        """Determines behaviour of import method's GUI behaviour when sheet is chosen.
        """
        df = pd.read_excel(self.directory, sheet_name=self.__sheet.get())

        self.__xseriesprovided = False
        self.__yseriesprovided = False

        self.__xseriescb.set("")
        self.__yseriescb.set("")
        self.__xseriescb['state'] = "readonly"
        self.__yseriescb['state'] = "readonly"
        self.__xseriescb['values'] = df.columns.values.tolist()
        self.__yseriescb['values'] = df.columns.values.tolist()

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
        logger.log("Started importing XLS file from: " + self.directory)
        
        pre = pd.ExcelFile(self.directory)

        labsheet = Label(section, text=loader.lang["importer-xls"]["sheets"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labsheet.grid(row=1)
        self.__sheet = StringVar()
        sheetcb = ttk.Combobox(section, state="readonly", textvariable=self.__sheet, width=int((section.winfo_width()-13)/7)+1)
        sheetcb['values'] = pre.sheet_names
        sheetcb.grid(row=2)

        labxseries = Label(section, text=loader.lang["importer-xls"]["xseries"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labxseries.grid(row=3)
        self.__xseries = StringVar()
        self.__xseriescb = ttk.Combobox(section, state="disabled", textvariable=self.__xseries, width=int((section.winfo_width()-13)/7)+1)
        self.__xseriescb.grid(row=4)

        labyseries = Label(section, text=loader.lang["importer-xls"]["yseries"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labyseries.grid(row=5)
        self.__yseries = StringVar()
        self.__yseriescb = ttk.Combobox(section, state="disabled", textvariable=self.__yseries, width=int((section.winfo_width()-13)/7)+1)
        self.__yseriescb.grid(row=6)

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

        self.__xseriescb.bind('<<ComboboxSelected>>', self.onXchange)            
        self.__yseriescb.bind('<<ComboboxSelected>>', self.onYchange)    
        sheetcb.bind('<<ComboboxSelected>>', self.onSheetChange)    

    def extractData(self) -> DataFrame:
        """Extracts signal from provided data.
        
        :returns: Data frame of single, selected time series.
        """
        if(len(self.__datax) and len(self.__datay)):
            logger.log("Importing XLS columns (X/Y): " + self.__xseries.get() + "/" + self.__yseries.get() + " from sheet " + self.__sheet.get())
            data = {
                f'{self.__xseries.get()}': self.__datax,
                f'{self.__yseries.get()}': self.__datay
            }

            messagebox.showinfo(loader.lang["messagebox"]["info"], loader.lang["importer-xls"]["successimport"])
            return DataFrame(data,columns=[self.__xseries.get(),self.__yseries.get()])
        else:
            messagebox.showerror(loader.lang["messagebox"]["error"], loader.lang["importer-xls"]["wrongimport"])
            return DataFrame()
