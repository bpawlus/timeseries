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

    xseries = None
    """Chosen X-axis name from chosen sheet"""
    yseries = None
    """Chosen Y-axis name from chosen sheet."""
    sheet = None
    """Chosen sheet name from spreadsheet."""
    datax = []
    """Loaded X-axis data. Should contain indexes with constant intervals."""
    datay = []
    """Loaded Y-axis data. Should data of observed phenomenon."""
    xseriesprovided = False
    """Auxiliary variable, determines if user provided X-axis data."""
    yseriesprovided = False
    """Auxiliary variable, determines if user provided Y-axis data."""

    def onXYprovided(self):
        """Determines behaviour of import method's GUI behaviour when X and Y axis data are provided.
        """
        if(self.xseries.get() != self.yseries.get()):
            data = pd.read_excel(self.directory, sheet_name=self.sheet.get(), usecols=(self.xseries.get(), self.yseries.get())).values.tolist()
            self.datax = [item[0] for item in data]
            self.datay = [item[1] for item in data]

            for i in self.preview.get_children():
                self.preview.delete(i)
            for v in data:
                self.preview.insert('', END, values=v)
        else:
            for i in self.preview.get_children():
                self.preview.delete(i)
            self.datax.clear()
            self.datay.clear()

    def onXchange(self, event):
        """Determines behaviour of import method's GUI behaviour when X axis data is provided.
        """
        self.preview.column("x", anchor=CENTER)
        self.preview.heading("x",text=self.xseries.get(),anchor=CENTER)
        self.xseriesprovided = True
        if self.xseriesprovided and self.yseriesprovided:
            self.onXYprovided()

    def onYchange(self, event):
        """Determines behaviour of import method's GUI behaviour when Y axis data is provided.
        """
        self.preview.column("y", anchor=CENTER)
        self.preview.heading("y",text=self.yseries.get(),anchor=CENTER)
        self.yseriesprovided = True
        if self.xseriesprovided and self.yseriesprovided:
            self.onXYprovided()

    def onSheetChange(self, event):
        """Determines behaviour of import method's GUI behaviour when sheet is chosen.
        """
        df = pd.read_excel(self.directory, sheet_name=self.sheet.get())

        self.xseriesprovided = False
        self.yseriesprovided = False

        self.xseriescb.set("")
        self.yseriescb.set("")
        self.xseriescb['state'] = "readonly"
        self.yseriescb['state'] = "readonly"
        self.xseriescb['values'] = df.columns.values.tolist()
        self.yseriescb['values'] = df.columns.values.tolist()

        self.preview.column("x", anchor=CENTER)
        self.preview.column("y", anchor=CENTER)
        self.preview.heading("x",text="",anchor=CENTER)
        self.preview.heading("y",text="",anchor=CENTER)

        for i in self.preview.get_children():
            self.preview.delete(i)
        self.datax.clear()
        self.datay.clear()

    def importSettingsGui(self, section: ttk.Frame):
        """Provides GUI elements for selection of specific signal from provided data.
        """
        logger.log("Started importing XLS file from: " + self.directory)
        
        pre = pd.ExcelFile(self.directory)

        labsheet = Label(section, text=loader.lang["importer-xls"]["sheets"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labsheet.grid(row=1)
        self.sheet = StringVar()
        sheetcb = ttk.Combobox(section, state="readonly", textvariable=self.sheet, width=int((section.winfo_width()-13)/7)+1)
        sheetcb['values'] = pre.sheet_names
        sheetcb.grid(row=2)

        labxseries = Label(section, text=loader.lang["importer-xls"]["xseries"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labxseries.grid(row=3)
        self.xseries = StringVar()
        self.xseriescb = ttk.Combobox(section, state="disabled", textvariable=self.xseries, width=int((section.winfo_width()-13)/7)+1)
        self.xseriescb.grid(row=4)

        labyseries = Label(section, text=loader.lang["importer-xls"]["yseries"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labyseries.grid(row=5)
        self.yseries = StringVar()
        self.yseriescb = ttk.Combobox(section, state="disabled", textvariable=self.yseries, width=int((section.winfo_width()-13)/7)+1)
        self.yseriescb.grid(row=6)

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

        self.xseriescb.bind('<<ComboboxSelected>>', self.onXchange)            
        self.yseriescb.bind('<<ComboboxSelected>>', self.onYchange)    
        sheetcb.bind('<<ComboboxSelected>>', self.onSheetChange)    

    def extractData(self) -> DataFrame:
        """Extracts signal from provided data.
        
        :returns: Data frame of single, selected time series.
        """
        if(len(self.datax) and len(self.datay)):
            logger.log("Importing XLS columns (X/Y): " + self.xseries.get() + "/" + self.yseries.get() + " from sheet " + self.sheet.get())
            data = {
                f'{self.xseries.get()}': self.datax,
                f'{self.yseries.get()}': self.datay
            }

            messagebox.showinfo(loader.lang["messagebox"]["info"], loader.lang["importer-xls"]["successimport"])
            return DataFrame(data,columns=[self.xseries.get(),self.yseries.get()])
        else:
            messagebox.showerror(loader.lang["messagebox"]["error"], loader.lang["importer-xls"]["wrongimport"])
            return DataFrame()
