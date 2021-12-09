from tkinter import *
from tkinter import ttk, filedialog, messagebox
from typing import Tuple

import pandas as pd
from pandas import DataFrame

import logger
from loader import lang, appconfig, directories

allmethods = ()
alldrivers = ()

class ImportMethod:
    directory = ""
    defaultTitle = ""
    
    @staticmethod
    def addMethod(self):
        global allmethods, alldrivers
        allmethods = ((self.extension, self.displayname),) + allmethods
        alldrivers = ((self.extension, self),)+alldrivers

    def __init__(self, extension, displayname):
        self.extension = extension
        self.displayname = displayname
        self.addMethod(self)

    def importSettingsGui(self, subsection: ttk.Frame, lang):
        return

    def extractData(self) -> DataFrame:
        return DataFrame()

class XlsImportMethod(ImportMethod):
    xseries = None
    yseries = None
    sheet = None
    datax = []
    datay = []
    xseriesprovided = False
    yseriesprovided = False

    def importSettingsGui(self, subsection: ttk.Frame):
        logger.log("Started importing XLS file from: " + self.directory)
        
        global lang
        self.defaultTitle = lang["importer-xls"]["defaultTitle"]
        pre = pd.ExcelFile(self.directory)

        labsheet = Label(subsection, text=lang["importer-xls"]["sheets"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
        labsheet.grid(row=1)
        self.sheet = StringVar()
        sheetcb = ttk.Combobox(subsection, state="readonly", textvariable=self.sheet, width=int((subsection.winfo_width()-13)/7)+1)
        sheetcb['values'] = pre.sheet_names
        sheetcb.grid(row=2)

        labxseries = Label(subsection, text=lang["importer-xls"]["xseries"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
        labxseries.grid(row=3)
        self.xseries = StringVar()
        xseriescb = ttk.Combobox(subsection, state="disabled", textvariable=self.xseries, width=int((subsection.winfo_width()-13)/7)+1)
        xseriescb.grid(row=4)

        labyseries = Label(subsection, text=lang["importer-xls"]["yseries"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
        labyseries.grid(row=5)
        self.yseries = StringVar()
        yseriescb = ttk.Combobox(subsection, state="disabled", textvariable=self.yseries, width=int((subsection.winfo_width()-13)/7)+1)
        yseriescb.grid(row=6)

        labpreview = Label(subsection, text=lang["importer-xls"]["preview"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
        labpreview.grid(row=7)

        preview = ttk.Treeview(subsection)
        preview['columns'] = ("x", "y")
        preview.column("#0", width=0, stretch=NO)
        preview.column("x", anchor=CENTER, width=int(subsection.winfo_width()/2))
        preview.column("y", anchor=CENTER, width=int(subsection.winfo_width()/2))
        preview.heading("#0",text="",anchor=CENTER)
        preview.heading("x",text="",anchor=CENTER)
        preview.heading("y",text="",anchor=CENTER)
        preview.grid(row=8)



        def onXYprovided():
            if(self.xseries.get() != self.yseries.get()):
                data = pd.read_excel(self.directory, sheet_name=self.sheet.get(), usecols=(self.xseries.get(), self.yseries.get())).values.tolist()
                self.datax = [item[0] for item in data]
                self.datay = [item[1] for item in data]

                for i in preview.get_children():
                    preview.delete(i)
                for v in data:
                    preview.insert('', END, values=v)
            else:
                for i in preview.get_children():
                    preview.delete(i)
                self.datax.clear()
                self.datay.clear()

        def onXchange(event):
            preview.column("x", anchor=CENTER)
            preview.heading("x",text=self.xseries.get(),anchor=CENTER)
            self.xseriesprovided = True
            if self.xseriesprovided and self.yseriesprovided:
                onXYprovided()
        xseriescb.bind('<<ComboboxSelected>>', onXchange)            

        def onYchange(event):
            preview.column("y", anchor=CENTER)
            preview.heading("y",text=self.yseries.get(),anchor=CENTER)
            self.yseriesprovided = True
            if self.xseriesprovided and self.yseriesprovided:
                onXYprovided()

        yseriescb.bind('<<ComboboxSelected>>', onYchange)    

        def onSheetChange(event):
            df = pd.read_excel(self.directory, sheet_name=self.sheet.get())

            self.xseriesprovided = False
            self.yseriesprovided = False

            xseriescb.set("")
            yseriescb.set("")
            xseriescb['state'] = "readonly"
            yseriescb['state'] = "readonly"
            xseriescb['values'] = df.columns.values.tolist()
            yseriescb['values'] = df.columns.values.tolist()

            preview.column("x", anchor=CENTER)
            preview.column("y", anchor=CENTER)
            preview.heading("x",text="",anchor=CENTER)
            preview.heading("y",text="",anchor=CENTER)

            for i in preview.get_children():
                preview.delete(i)
            self.datax.clear()
            self.datay.clear()

        sheetcb.bind('<<ComboboxSelected>>', onSheetChange)    

    def extractData(self) -> DataFrame:
        if(len(self.datax) and len(self.datay)):
            logger.log("Importing XLS columns (X/Y): " + self.xseries.get() + "/" + self.yseries.get() + " from sheet " + self.sheet.get())
            data = {
                f'{self.xseries.get()}': self.datax,
                f'{self.yseries.get()}': self.datay
            }

            messagebox.showinfo(lang["messagebox"]["info"], lang["importer-xls"]["successimport"])
            return DataFrame(data,columns=[self.xseries.get(),self.yseries.get()])
        else:
            messagebox.showerror(lang["messagebox"]["error"], lang["importer-xls"]["wrongimport"])
            return DataFrame()

class CsvImportMethod(ImportMethod):
    xseries = None
    yseries = None
    datax = []
    datay = []
    xseriesprovided = False
    yseriesprovided = False

    def importSettingsGui(self, subsection: ttk.Frame):
        logger.log("Started importing CSV file from: " + self.directory)
        
        global lang
        self.defaultTitle = lang["importer-xls"]["defaultTitle"]
        pre = pd.read_csv(self.directory)

        labxseries = Label(subsection, text=lang["importer-csv"]["xseries"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
        labxseries.grid(row=1)
        self.xseries = StringVar()
        xseriescb = ttk.Combobox(subsection, state="readonly", textvariable=self.xseries, width=int((subsection.winfo_width()-13)/7)+1)
        xseriescb.set("")
        xseriescb['values'] = pre.columns.values.tolist()
        xseriescb.grid(row=2)

        labyseries = Label(subsection, text=lang["importer-csv"]["yseries"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
        labyseries.grid(row=3)
        self.yseries = StringVar()
        yseriescb = ttk.Combobox(subsection, state="readonly", textvariable=self.yseries, width=int((subsection.winfo_width()-13)/7)+1)
        yseriescb.set("")
        yseriescb['values'] = pre.columns.values.tolist()
        yseriescb.grid(row=4)

        labpreview = Label(subsection, text=lang["importer-csv"]["preview"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
        labpreview.grid(row=5)

        preview = ttk.Treeview(subsection)
        preview['columns'] = ("x", "y")
        preview.column("#0", width=0, stretch=NO)
        preview.column("x", anchor=CENTER, width=int(subsection.winfo_width()/2))
        preview.column("y", anchor=CENTER, width=int(subsection.winfo_width()/2))
        preview.heading("#0",text="",anchor=CENTER)
        preview.heading("x",text="",anchor=CENTER)
        preview.heading("y",text="",anchor=CENTER)
        preview.grid(row=6)

        def onXYprovided():
            if(self.xseries.get() != self.yseries.get()):
                data = pd.read_csv(self.directory, usecols=(self.xseries.get(), self.yseries.get())).values.tolist()
                self.datax = [item[0] for item in data]
                self.datay = [item[1] for item in data]

                for i in preview.get_children():
                    preview.delete(i)
                for v in data:
                    preview.insert('', END, values=v)
            else:
                for i in preview.get_children():
                    preview.delete(i)
                self.datax.clear()
                self.datay.clear()

        def onXchange(event):
            preview.column("x", anchor=CENTER)
            preview.heading("x",text=self.xseries.get(),anchor=CENTER)
            self.xseriesprovided = True
            if self.xseriesprovided and self.yseriesprovided:
                onXYprovided()
        xseriescb.bind('<<ComboboxSelected>>', onXchange)            

        def onYchange(event):
            preview.column("y", anchor=CENTER)
            preview.heading("y",text=self.yseries.get(),anchor=CENTER)
            self.yseriesprovided = True
            if self.xseriesprovided and self.yseriesprovided:
                onXYprovided()

        yseriescb.bind('<<ComboboxSelected>>', onYchange)    

        self.xseriesprovided = False
        self.yseriesprovided = False

    def extractData(self) -> DataFrame:
        if(len(self.datax) and len(self.datay)):
            logger.log("Importing XLS columns (X/Y): " + self.xseries.get() + "/" + self.yseries.get())
            data = {
                f'{self.xseries.get()}': self.datax,
                f'{self.yseries.get()}': self.datay
            }
            messagebox.showinfo(lang["messagebox"]["info"], lang["importer-csv"]["successimport"])
            return DataFrame(data,columns=[self.xseries.get(),self.yseries.get()])
        else:
            messagebox.showerror(lang["messagebox"]["error"], lang["importer-csv"]["wrongimport"])
            return DataFrame()

methodxls = XlsImportMethod(".xls", "xls")
methodcsv = CsvImportMethod(".csv", "csv")