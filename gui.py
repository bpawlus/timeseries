from tkinter import *
from tkinter import ttk, filedialog, messagebox
import os
import random
from pandas.core.frame import DataFrame
import loader
from hubCharts import HubCharts
from hubImporters import HubImporters
from hubTSModules import HubTSModules
from importers import baseimport
import numpy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import matplotlib.patches as patches
import logger
import entryvalidators


class Gui():
    """Base class responsible for constructing window application.
    """

    root = None
    """Reference to root window."""

    def buildSections(self):
        """Method meant to be overwritten.
        Constructs all sections of an application.
        """
        pass

    def buildGui(self):
        """Constructs and runs root window for an application.
        """
        self.root = Tk()
        self.root.title(loader.lang["title"])
        self.root.iconbitmap(loader.dirs["icon"])
        self.root.geometry(f'{loader.conf["width"]}x{loader.conf["height"]}')
        self.root.minsize(loader.conf["width"], loader.conf["height"])
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.buildSections()
        self.root.mainloop()

class AnalyzerGui(Gui):
    """Class contains window application of time series analyzer.
    """

    sectionChart: Frame = None
    """Section with chart that displays current data."""

    sectionSettings: Frame = None
    """Section with settings that set properties of data."""
    subsectionLoadData: Frame = None
    """Subsection of settings section that loads of data from memory."""
    subsectionDataSelection: Frame = None
    """Subsection of settings section that allows user to choose displayed data, which was previously loaded."""
    subsectionTSModules: Frame = None
    """Subsection of settings section that allows user to choose displayed time series analyzing modules."""

    sectionOutput: Frame = None
    """Section with output functions that display and export data."""
    subsectionStatisctics: Frame = None
    """Subsection of output section that displays data of modules in tabular form."""
    subsectionLogger: Frame = None
    """Subsection of output section that logs user's actions."""
    subsectionExportData: Frame = None
    """Subsection of output section that allows exporting logs, chart and statistics."""

    hubimporters: HubImporters = HubImporters()
    """Functional component with methods concerning data importers."""
    hubcharts: HubCharts = HubCharts()
    """Functional component with methods concerning loaded data in form of charts."""
    hubtsmodules: HubTSModules = HubTSModules()
    """Functional component with methods concerning time series analyzing modules."""

    importer: baseimport.ImportMethod = None
    """Chosen by user importer function (ex. .xls import when loading microsoft excel spreadsheet)."""
    chartId: int = -1
    """ID of currently displayed chart"""

    def clearsectionChart(self):
        """Method clears the view of section with chart.
        """
        for widget in self.sectionChart.winfo_children():
            widget.destroy()

    def statisticstabRefresh(self):
        """Removes the content of combobox and table view with all active time series modules.
        """
        self.outputModulescb.set('')
        for i in self.statisticstab.get_children():
            self.statisticstab.delete(i)

    def updateChartsCb(self):
        """Refreshes the content of combobox with all loaded time series modules.
        """
        self.chartscb['values'] = self.hubcharts.getAllChartDisplayNames()

    def updateChart(self):
        """Updates the view of section with chart.
        """
        self.clearsectionChart()

        if(self.chartId != -1):
            self.hubcharts.displayChart(self.chartId, self.sectionChart, self.hubtsmodules.displayModules)
            self.statisticstabRefresh()

            self.outputModulescb['values'] = self.hubtsmodules.getAllActiveModuleNames()
            self.statisticstab['columns'] = []

    def deleteChart(self):
        """Deletes the current viewed chart.
        """
        self.hubcharts.removeChart(self.chartId)
        self.chartId = -1
        self.statisticstabRefresh()

        self.outputModulescb['values'] = []
        self.statisticstab['columns'] = []

        self.clearsectionChart()


    def subsectionLoadData_btnimport_action(self):
        """Method called when activating import button in
        subsection of settings section that loads of data from memory.
        Configures chosen importer function.
        """
        directory = filedialog.askopenfilename(initialdir="", title=loader.lang["settings"]["loaddata"]["import"], filetypes=(self.hubimporters.allMethods))
        filename, fileextension = os.path.splitext(directory)
        for widget in self.importsettings.winfo_children():
            widget.destroy()

        self.importer = self.hubimporters.getImporterByFileextension(fileextension)
        if self.importer != None:
            self.importer.directory = directory
            self.importer.importSettingsGui(self.importsettings)
            self.btnexport['state'] = "normal"

    def subsectionLoadData_btnexport_action(self):
        """Method called when activating export button in
        subsection of settings section that loads of data from memory.
        Exports data from importer to application's memory.
        """
        df = self.importer.extractData()
        if(not df.empty):
            self.hubcharts.addChart(df, title=self.importer.defaultTitle)
            self.updateChartsCb()

    def subsectionDataSelection_btnupdate_action(self):
        """Method called when activating update button in
        subsection of settings section that allows user to choose displayed data, which was previously loaded.
        Updates chart displays with chosen data.
        """
        chart = self.hubcharts.getChartById(self.chartId)
        chart.title = self.titleentry.get()
        self.updateChartsCb()
        self.chartscb.set(f'{chart.title} ({chart.id})')
        self.updateChart()

    def subsectionDataSelection_btndelete_action(self):
        """Method called when activating delete button in
        subsection of settings section that allows user to choose displayed data, which was previously loaded.
        Deletes selected data.
        """
        self.deleteChart()
        self.updateChartsCb()
        self.chartscb.set("")             

        self.textoutput['state'] = "disabled"
        self.titleentry.set("")
        self.btndelete['state'] = "disabled"
        self.btnupdate['state'] = "disabled"

    def subsectionDataSelection_chartscb_action(self, event):
        """Method called when updating charts combobox in
        subsection of settings section that allows user to choose displayed data, which was previously loaded.
        Updates the preview of selected data.
        """
        name = self.chartscbvar.get()
        self.chartId = self.hubcharts.getChartIdByDisplayName(name)
            
        self.textoutput['state'] = "normal"
        chart = self.hubcharts.getChartById(self.chartId)
        self.titleentry.set(chart.title)
            
        self.btndelete['state'] = "normal"
        self.btnupdate['state'] = "normal"

    def subsectionTSModules_tsmodulesentrycb_action(self, event):
        """Method called when updating modules combobox in
        subsection of settings section that allows user to choose displayed time series analyzing modules.
        Rebuilds a menu with module parameters.
        """
        mod = self.hubtsmodules.getModuleByName(self.tsmodulesentry.get())
        mod.buildMenu(self.tsmodulesFrame)

    def subsectionStatisctics_outputModulescb_action(self, event):
        """Method called when updating modules combobox in
        subsection of output section that displays data of modules in tabular form.
        Rebuilds a table view of analyzing module data.
        """
        
        for i in self.statisticstab.get_children():
            self.statisticstab.delete(i)
        self.statisticstab.column("#0", width=0, stretch=NO)
        self.statisticstab.heading("#0",text="",anchor=CENTER)

        df = self.hubtsmodules.getModuleByName(self.outputModules.get()).outputDataframe
        columns = df.columns.values.tolist()
        self.statisticstab['columns'] = columns

        for column in columns:
            self.statisticstab.column(column, anchor=CENTER, width=int(self.subsectionStatisctics.winfo_width()/len(columns)))
            self.statisticstab.heading(column,text=column,anchor=CENTER)

        data = df.values.tolist()
        for v in data:
            self.statisticstab.insert('', END, values=v)

    def subsectionExportData_btnexportchart_action(self):
        """Method called when activating export button in
        subsection of output section that allows exporting logs, chart and statistics
        Exports displayed chart to image format.
        """
        if(self.chartId != -1):
            chart = self.hubcharts.getChartById(self.chartId)
            chart.exportChart(loader.dirs["exportchart"])
            messagebox.showinfo(loader.lang["messagebox"]["info"], f'{loader.lang["output"]["exportdata"]["successexportchart"]}{loader.dirs["exportchart"]}')
        else:
            messagebox.showerror(loader.lang["messagebox"]["error"], loader.lang["output"]["exportdata"]["failedexport"])

    def subsectionExportData_btnexportlogs_action(self):
        """Method called when activating export button in
        subsection of output section that allows exporting logs, chart and statistics
        Exports logs to text format.
        """
        f = open(loader.dirs["exportlogname"], "w")
        f.write(self.loggertextoutput.get("1.0",END))
        f.close()
        messagebox.showinfo(loader.lang["messagebox"]["info"], f'{loader.lang["output"]["exportdata"]["successexportlogs"]}{loader.dirs["exportlogname"]}')

    def subsectionExportData_btnexportstats_action(self):
        """Method called when activating export button in
        subsection of output section that allows exporting logs, chart and statistics
        Exports output modules data to text format.
        """
        if(self.chartId != -1):
            f = open(loader.dirs["exportstats"], "w")
            mods = self.hubtsmodules.getAllActiveModules()
            for mod in mods:
                f.write(mod.name)
                f.write("\n")
                f.write(mod.outputDataframe.to_string())
                f.write("\n\n")
            f.close()
            messagebox.showinfo(loader.lang["messagebox"]["info"], f'{loader.lang["output"]["exportdata"]["successexportstats"]}{loader.dirs["exportstats"]}')
        else:
            messagebox.showerror(loader.lang["messagebox"]["error"], loader.lang["output"]["exportdata"]["failedexport"])


    def buildSubsectionLoadData(self):
        """Builds subsection of settings section that loads of data from memory.
        """
        self.subsectionLoadData.grid_columnconfigure(0, weight=1)

        #Width formula: 13, 20, 27, 34... 13 + 7n
        self.importsettings = Frame(self.subsectionLoadData, width=self.subsectionLoadData.winfo_width())
        self.importsettings.grid(row=2)
        
        self.btnexport = Button(self.subsectionLoadData, state="disabled", text=loader.lang["settings"]["loaddata"]["select"], command=self.subsectionLoadData_btnexport_action, pady=5, width=int((self.subsectionLoadData.winfo_width()-13)/7)+1)
        self.btnexport.grid(row=3)

        btnimport = Button(self.subsectionLoadData, text=loader.lang["settings"]["loaddata"]["import"], command=self.subsectionLoadData_btnimport_action, pady=5, width=int((self.subsectionLoadData.winfo_width()-13)/7)+1)
        btnimport.grid(row=1)

    def buildSubsectionDataSelection(self):
        """Builds subsection of settings section that allows user to choose displayed data, which was previously loaded.
        """
        self.subsectionDataSelection.grid_columnconfigure(0, weight=1)
        
        labcharts = Label(self.subsectionDataSelection, text=loader.lang["settings"]["charts"]["select"], pady=5, width=int((self.subsectionDataSelection.winfo_width()-13)/7)+1)
        labcharts.grid(row=1)
        self.chartscbvar = StringVar()
        self.chartscb = ttk.Combobox(self.subsectionDataSelection, state="readonly", textvariable=self.chartscbvar, width=int((self.subsectionDataSelection.winfo_width()-13)/7)+1)
        self.chartscb.grid(row=2)

        labcharts = Label(self.subsectionDataSelection, text=loader.lang["settings"]["charts"]["titlechanger"], pady=5, width=int((self.subsectionDataSelection.winfo_width()-13)/7)+1)
        labcharts.grid(row=3)
        self.titleentry = StringVar()
        self.textoutput = Entry(self.subsectionDataSelection, textvariable=self.titleentry, state="disabled", width=int((self.subsectionDataSelection.winfo_width()-13)/7)+1)
        self.textoutput.grid(row=4)

        self.btnupdate = Button(self.subsectionDataSelection, state="disabled", text=loader.lang["settings"]["charts"]["update"], command=self.subsectionDataSelection_btnupdate_action, pady=5, width=int((self.subsectionDataSelection.winfo_width()-13)/7)+1)
        self.btnupdate.grid(row=5)

        self.btndelete = Button(self.subsectionDataSelection, state="disabled", text=loader.lang["settings"]["charts"]["delete"], command=self.subsectionDataSelection_btndelete_action, pady=5, width=int((self.subsectionDataSelection.winfo_width()-13)/7)+1)
        self.btndelete.grid(row=6)

        self.chartscb.bind('<<ComboboxSelected>>', self.subsectionDataSelection_chartscb_action)   

    def buildSubsectionTSModules(self):
        """Builds subsection of settings section that allows user to choose displayed time series analyzing modules.
        """
        self.subsectionTSModules.grid_columnconfigure(0, weight=1)

        labtsmodules = Label(self.subsectionTSModules, text=loader.lang["settings"]["modules"]["modules"], pady=5, width=int((self.subsectionTSModules.winfo_width()-13)/7)+1)
        labtsmodules.grid(row=1)
        self.tsmodulesentry = StringVar()
        tsmodulesentrycb = ttk.Combobox(self.subsectionTSModules, state="readonly", textvariable=self.tsmodulesentry, width=int((self.subsectionTSModules.winfo_width()-13)/7)+1)
        tsmodulesentrycb.grid(row=2)
        tsmodulesentrycb['values'] = [mod.name for mod in self.hubtsmodules.allModules]

        self.tsmodulesFrame = Frame(self.subsectionTSModules, width=self.subsectionTSModules.winfo_width())
        self.tsmodulesFrame.grid(row=3)
        
        btnexport = Button(self.subsectionTSModules, text=loader.lang["settings"]["modules"]["update"], command=self.updateChart, pady=5, width=int((self.subsectionTSModules.winfo_width()-13)/7)+1)
        btnexport.grid(row=4)

        tsmodulesentrycb.bind('<<ComboboxSelected>>', self.subsectionTSModules_tsmodulesentrycb_action)   

    def buildSubsectionStatisctics(self):
        """Builds subsection of output section that displays data of modules in tabular form.
        """
        self.subsectionStatisctics.grid_columnconfigure(0, weight=1)

        labcharts = Label(self.subsectionStatisctics, text=loader.lang["output"]["statistics"]["modules"], pady=5, width=int((self.subsectionStatisctics.winfo_width()-13)/7)+1)
        labcharts.grid(row=1)
        self.outputModules = StringVar()
        self.outputModulescb = ttk.Combobox(self.subsectionStatisctics, state="readonly", textvariable=self.outputModules, width=int((self.subsectionStatisctics.winfo_width()-13)/7)+1)
        self.outputModulescb.grid(row=2)

        self.statisticstab = ttk.Treeview(self.subsectionStatisctics)
        self.statisticstab.grid(row=3, sticky=NSEW)
        self.statisticstab.column("#0", width=self.subsectionStatisctics.winfo_width(), stretch=YES)
        self.statisticstab.heading("#0",text="",anchor=CENTER)
       
        self.outputModulescb.bind('<<ComboboxSelected>>', self.subsectionStatisctics_outputModulescb_action)   

    def buildSubsectionLogger(self):
        """Builds subsection of output section that logs user's actions.
        """
        self.subsectionLogger.grid_columnconfigure(0, weight=1)

        #Height formula: 4 + 16n
        self.loggertextoutput = Text(self.subsectionLogger, width=self.subsectionLogger.winfo_width(), height=int(((self.subsectionLogger.winfo_height()-4)/16+1)))
        self.loggertextoutput.grid(row=1, sticky=NSEW)

        logger.win = self.loggertextoutput
        logger.log("Initiated")

    def buildSubsectionExportData(self):
        """Builds subsection of output section that allows exporting logs, chart and statistics.
        """
        self.subsectionExportData.grid_columnconfigure(0, weight=1)

        btnexportchart = Button(self.subsectionExportData, text=loader.lang["output"]["exportdata"]["exportchart"], command=self.subsectionExportData_btnexportchart_action, pady=5, width=int((self.subsectionExportData.winfo_width()-13)/7)+1)
        btnexportchart.grid(row=1)

        btnexportlogs = Button(self.subsectionExportData, text=loader.lang["output"]["exportdata"]["exportlogs"], command=self.subsectionExportData_btnexportlogs_action, pady=5, width=int((self.subsectionExportData.winfo_width()-13)/7)+1)
        btnexportlogs.grid(row=2)

        btnexportstats = Button(self.subsectionExportData, text=loader.lang["output"]["exportdata"]["exportstats"], command=self.subsectionExportData_btnexportstats_action, pady=5, width=int((self.subsectionExportData.winfo_width()-13)/7)+1)
        btnexportstats.grid(row=3)


    def buildSectionChart(self):
        """Builds section with chart that displays current data.
        """
        self.sectionChart.grid_columnconfigure(0, weight=1)
        self.sectionChart.grid_rowconfigure(0, weight=1)
        
    def buildSectionSettings(self):
        """Builds section with settings that set properties of data.
        """
        self.sectionSettings.grid_columnconfigure(0, weight=1)
        self.sectionSettings.grid_rowconfigure(0, weight=1)

        settingsnotebook = ttk.Notebook(self.sectionSettings)

        self.subsectionLoadData = Frame(settingsnotebook,width=self.sectionSettings.winfo_width(),height=self.sectionSettings.winfo_height())
        self.subsectionDataSelection = Frame(settingsnotebook,width=self.sectionSettings.winfo_width(),height=self.sectionSettings.winfo_height())
        self.subsectionTSModules = Frame(settingsnotebook,width=self.sectionSettings.winfo_width(),height=self.sectionSettings.winfo_height())

        settingsnotebook.add(self.subsectionLoadData, text=loader.lang["settings"]["loaddata"]["header"])
        settingsnotebook.add(self.subsectionDataSelection, text=loader.lang["settings"]["charts"]["header"])
        settingsnotebook.add(self.subsectionTSModules, text=loader.lang["settings"]["modules"]["header"])

        settingsnotebook.pack(expand=1, fill='both')

        self.subsectionLoadData.update()
        self.subsectionDataSelection.update()
        self.subsectionTSModules.update()
        settingsnotebook.select(0)
        self.buildSubsectionLoadData()

        self.subsectionLoadData.update()
        self.subsectionDataSelection.update()
        self.subsectionTSModules.update()
        settingsnotebook.select(1)
        self.buildSubsectionDataSelection()

        self.subsectionLoadData.update()
        self.subsectionDataSelection.update()
        self.subsectionTSModules.update()
        settingsnotebook.select(2)
        self.buildSubsectionTSModules()

        self.subsectionLoadData.update()
        self.subsectionDataSelection.update()
        self.subsectionTSModules.update()
        settingsnotebook.select(0)

    def buildSectionOutput(self):
        """Builds section with output functions that display and export data.
        """
        self.sectionOutput.grid_columnconfigure(0, weight=1)
        self.sectionOutput.grid_rowconfigure(0, weight=1)

        outputnotebook = ttk.Notebook(self.sectionOutput)

        self.subsectionStatisctics = Frame(outputnotebook,width=self.sectionOutput.winfo_width(),height=self.sectionOutput.winfo_height())
        self.subsectionLogger = Frame(outputnotebook,width=self.sectionOutput.winfo_width(),height=self.sectionOutput.winfo_height())
        self.subsectionExportData = Frame(outputnotebook,width=self.sectionOutput.winfo_width(),height=self.sectionOutput.winfo_height())

        outputnotebook.add(self.subsectionStatisctics, text=loader.lang["output"]["statistics"]["header"])
        outputnotebook.add(self.subsectionLogger, text=loader.lang["output"]["logger"]["header"])
        outputnotebook.add(self.subsectionExportData, text=loader.lang["output"]["exportdata"]["header"])

        outputnotebook.pack(expand=1, fill='both')

        self.subsectionStatisctics.update()
        self.subsectionLogger.update()
        self.subsectionExportData.update()
        outputnotebook.select(0)
        self.buildSubsectionStatisctics()

        self.subsectionStatisctics.update()
        self.subsectionLogger.update()
        self.subsectionExportData.update()
        outputnotebook.select(1)
        self.buildSubsectionLogger()

        self.subsectionStatisctics.update()
        self.subsectionLogger.update()
        self.subsectionExportData.update()
        outputnotebook.select(2)
        self.buildSubsectionExportData()

        self.subsectionStatisctics.update()
        self.subsectionLogger.update()
        self.subsectionExportData.update()
        outputnotebook.select(0)

    def buildSections(self):
        """Constructs all sections of an application.
        """
        self.hubimporters.loadImporters()
        self.hubtsmodules.loadModules()

        self.sectionChart = Frame(self.root,bg='white',width=loader.conf["width"]*0.75, height=loader.conf["height"]*0.5)
        self.sectionSettings = Frame(self.root,bg='white',width=loader.conf["width"]*0.25, height=loader.conf["height"])
        self.sectionOutput = Frame(self.root,bg='white',width=loader.conf["width"]*0.75, height=loader.conf["height"]*0.5)

        self.sectionChart.grid(column=0,row=0,columnspan=3,rowspan=2,sticky=NSEW)
        self.sectionSettings.grid(column=3,row=0,columnspan=1,rowspan=4,sticky=NSEW)
        self.sectionOutput.grid(column=0,row=2,columnspan=3,rowspan=2,sticky=NSEW)

        self.sectionChart.update()
        self.sectionSettings.update()
        self.sectionOutput.update()

        self.buildSectionChart()
        self.buildSectionSettings()
        self.buildSectionOutput()

class GeneratorGui(Gui):
    sectionChart: Frame = None
    """Section with chart that displays current generated data."""

    sectionSettings: Frame = None
    """Section with settings that set properties of generated data."""
    subsectionChartgenerator: Frame = None
    """Subsection of settings section that configures parameters of generated chart."""
    subsectionExportdata: Frame = None
    """Subsection of settings section that allows exporting generated chart and statistics."""

    df = DataFrame()
    """Data frame of generated signal."""
    cps = None
    """Generated change point indexes."""
    means = None
    """Means in area between change points, before applying noise."""
    spreads = None
    """Variances in area between change points, before applying noise."""

    cpCount = 2
    """Number of change points in generated signal."""
    samples = 100
    """Number of samples (data length) in generated signal."""
    meanVar = None
    """Mean of all data in generated signal."""
    spreadVar = None
    """Spread of mean of all data in generated signal."""
    cpspreadVar = None
    """Variance in areas between change points in generated signal."""
    spreadcpspreadVar = None
    """Spread of variance in areas between change points in generated signal."""

    def subsectionExportdata_btnupdate_action(self):
        """Method called when activating export button in
        subsection of settings section that allows exporting generated chart and statistics.
        Generates a new, randomized signal.
        """
        for widget in self.sectionChart.winfo_children():
            widget.destroy()

        step = self.samples/(self.cpCount+1)

        x = 0
        self.cps = [0]
        self.means = [random.uniform(self.meanVar.get()-self.spreadVar.get(), self.meanVar.get()+self.spreadVar.get())]
        self.spreads = [abs(random.uniform(self.cpspreadVar.get()-self.spreadcpspreadVar.get(), self.cpspreadVar.get()+self.spreadcpspreadVar.get()))]

        for i in range(self.cpCount):
            x += step
            self.cps.append(random.randint(int(x-step/2+1), int(x+step/2-1)))
            self.means.append(random.uniform(self.meanVar.get()-self.spreadVar.get(), self.meanVar.get()+self.spreadVar.get()))
            self.spreads.append(abs(random.uniform(self.cpspreadVar.get()-self.spreadcpspreadVar.get(), self.cpspreadVar.get()+self.spreadcpspreadVar.get())))
            
        self.dfdatay = []
        rects = []
        self.cps.append(self.samples)

        for i in range(len(self.cps)-1):
            cplen = self.cps[i+1]-self.cps[i]
            data = numpy.random.normal(self.means[i], self.spreads[i], cplen)
            self.dfdatay.extend(data)
            rects.append(patches.Rectangle((self.cps[i], self.means[i]-self.spreads[i]), cplen, 2*self.spreads[i], linewidth=2, edgecolor='#FFFF00', facecolor='none'))

        self.cps[len(self.cps)-1] -= 1
        self.dfdata = {
            "X": [x for x in range(self.samples)],
            "Y": self.dfdatay
        }

        self.df = DataFrame(self.dfdata,columns=["X","Y"])
        figure = plt.Figure(dpi=100)
        ax = figure.add_subplot(111)

        figure = FigureCanvasTkAgg(figure, self.sectionChart)
        figure.get_tk_widget().grid(row=0)

        self.df = self.df[["X", "Y"]].groupby("X").sum()
        self.df.plot(kind='line', legend=FALSE, ax=ax, color='r',marker='o', fontsize=4, markersize=2)

        for patch in rects:
            ax.add_patch(patch)

        ax.set_title(loader.lang["settings-gen"]["chartname"])
        self.btnexport['state'] = "normal"

    def subsectionExportdata_btnexport_action(self):
        """Method called when activating export button in
        subsection of settings section that allows exporting generated chart and statistics.
        Exports generated data to text format and csv spreadsheet.
        """
        if not self.df.empty:
            f = open(loader.dirs["geninfo"], "w")
            f.write(loader.lang["settings-gen"]["results"]["cps"] + "\n")
            f.write(' '.join([str(e) for e in self.cps]))
            f.write("\n\n")
            f.write(loader.lang["settings-gen"]["results"]["means"] + "\n")
            f.write(' '.join([str(e) for e in self.means]))
            f.write("\n\n")
            f.write(loader.lang["settings-gen"]["results"]["spreads"] + "\n")
            f.write(' '.join([str(e) for e in self.spreads]))
            f.close()
            self.df.to_csv(loader.dirs["gen"])
            messagebox.showinfo(loader.lang["messagebox"]["info"], loader.lang["settings-gen"]["results"]["exportinfo"] + "\n" + loader.dirs["geninfo"] + "\n" + loader.dirs["gen"])


    def buildSubSectionChartGenerator(self):
        """Builds subsection of settings section that configures parameters of generated chart.
        """
        self.subsectionChartgenerator.grid_columnconfigure(0, weight=1)

        labpoints = Label(self.subsectionChartgenerator, text=loader.lang["settings-gen"]["generator"]["cpcount"], pady=5, width=int((self.subsectionChartgenerator.winfo_width()-13)/7)+1)
        labpoints.grid(row=1)
        changePointCount = Scale(self.subsectionChartgenerator, from_=0, to=10, tickinterval=2, orient=HORIZONTAL, length=int(self.subsectionChartgenerator.winfo_width()))
        changePointCount.set(self.cpCount)
        changePointCount.grid(row=2)

        def updateChangePointCount(event):
            self.cpCount = int(changePointCount.get())

        changePointCount.bind("<ButtonRelease-1>", updateChangePointCount)

        labsamples = Label(self.subsectionChartgenerator, text=loader.lang["settings-gen"]["generator"]["samples"], pady=5, width=int((self.subsectionChartgenerator.winfo_width()-13)/7)+1)
        labsamples.grid(row=3)
        self.samplesCount = Scale(self.subsectionChartgenerator, from_=100, to=500, tickinterval=50, orient=HORIZONTAL, length=int(self.subsectionChartgenerator.winfo_width()))
        self.samplesCount.set(self.samples)
        self.samplesCount.grid(row=4)

        def updateSamplesCount(event):
            self.samples = int(self.samplesCount.get())

        self.samplesCount.bind("<ButtonRelease-1>", updateSamplesCount)

        labmean = Label(self.subsectionChartgenerator, text=loader.lang["settings-gen"]["generator"]["mean"], pady=5, width=int((self.subsectionChartgenerator.winfo_width()-13)/7)+1)
        labmean.grid(row=5)
        if not self.meanVar:
            self.meanVar = DoubleVar()
            self.meanVar.set(0.0)
        vcmd = (self.subsectionChartgenerator.register(entryvalidators.validate_floatentries),'%P')
        meanentry = Entry(self.subsectionChartgenerator, textvariable=self.meanVar, validate='all', validatecommand=vcmd, width=int((self.subsectionChartgenerator.winfo_width()-13)/7)+1)
        meanentry.grid(row=6)

        labspread = Label(self.subsectionChartgenerator, text=loader.lang["settings-gen"]["generator"]["spread"], pady=5, width=int((self.subsectionChartgenerator.winfo_width()-13)/7)+1)
        labspread.grid(row=7)
        if not self.spreadVar:
            self.spreadVar = DoubleVar()
            self.spreadVar.set(2.5)
        vcmd = (self.subsectionChartgenerator.register(entryvalidators.validate_floatentries),'%P')
        spreadentry = Entry(self.subsectionChartgenerator, textvariable=self.spreadVar, validate='all', validatecommand=vcmd, width=int((self.subsectionChartgenerator.winfo_width()-13)/7)+1)
        spreadentry.grid(row=8)

        cpspread = Label(self.subsectionChartgenerator, text=loader.lang["settings-gen"]["generator"]["cpspread"], pady=5, width=int((self.subsectionChartgenerator.winfo_width()-13)/7)+1)
        cpspread.grid(row=9)
        if not self.cpspreadVar:
            self.cpspreadVar = DoubleVar()
            self.cpspreadVar.set(0.75)
        vcmd = (self.subsectionChartgenerator.register(entryvalidators.validate_floatentries),'%P')
        cpspreadentry = Entry(self.subsectionChartgenerator, textvariable=self.cpspreadVar, validate='all', validatecommand=vcmd, width=int((self.subsectionChartgenerator.winfo_width()-13)/7)+1)
        cpspreadentry.grid(row=10)

        labspreadcpspread = Label(self.subsectionChartgenerator, text=loader.lang["settings-gen"]["generator"]["spreadcpspread"], pady=5, width=int((self.subsectionChartgenerator.winfo_width()-13)/7)+1)
        labspreadcpspread.grid(row=11)
        if not self.spreadcpspreadVar:
            self.spreadcpspreadVar = DoubleVar()
            self.spreadcpspreadVar.set(0.0)
        vcmd = (self.subsectionChartgenerator.register(entryvalidators.validate_floatentries),'%P')
        spreadcpspreadentry = Entry(self.subsectionChartgenerator, textvariable=self.spreadcpspreadVar, validate='all', validatecommand=vcmd, width=int((self.subsectionChartgenerator.winfo_width()-13)/7)+1)
        spreadcpspreadentry.grid(row=12)

    def buildSubSectionExportData(self):
        """Builds subsection of settings section that allows exporting generated chart and statistics.
        """
        self.subsectionExportdata.grid_columnconfigure(0, weight=1)

        btnupdate = Button(self.subsectionExportdata, text=loader.lang["settings-gen"]["output"]["update"], pady=5, width=int((self.subsectionExportdata.winfo_width()-13)/7)+1)
        btnupdate.grid(row=1)

        self.btnexport = Button(self.subsectionExportdata, state="disabled", text=loader.lang["settings-gen"]["output"]["export"], pady=5, width=int((self.subsectionExportdata.winfo_width()-13)/7)+1)
        self.btnexport.grid(row=2)

        btnupdate.configure(command=self.subsectionExportdata_btnupdate_action)
        self.btnexport.configure(command=self.subsectionExportdata_btnexport_action)
        

    def buildSectionChart(self):
        """Builds section with chart that displays current generated data.
        """
        self.sectionChart.grid_columnconfigure(0, weight=1)
        self.sectionChart.grid_rowconfigure(0, weight=1)

    def buildSectionSettings(self):
        """Builds section with settings that set properties of generated data.
        """
        self.sectionSettings.grid_columnconfigure(0, weight=1)
        self.sectionSettings.grid_rowconfigure(0, weight=1)

        notebook = ttk.Notebook(self.sectionSettings)

        self.subsectionChartgenerator = Frame(notebook,width=self.sectionSettings.winfo_width(),height=self.sectionSettings.winfo_height())
        self.subsectionExportdata = Frame(notebook,width=self.sectionSettings.winfo_width(),height=self.sectionSettings.winfo_height())

        notebook.add(self.subsectionChartgenerator, text=loader.lang["settings-gen"]["generator"]["header"])
        notebook.add(self.subsectionExportdata, text=loader.lang["settings-gen"]["output"]["header"])

        notebook.pack(expand=1, fill='both')

        self.subsectionChartgenerator.update()
        self.subsectionExportdata.update()
        notebook.select(0)
        self.buildSubSectionChartGenerator()

        self.subsectionChartgenerator.update()
        self.subsectionExportdata.update()
        notebook.select(1)
        self.buildSubSectionExportData()

        self.subsectionChartgenerator.update()
        self.subsectionExportdata.update()
        notebook.select(0)

    def buildSections(self):
        """Constructs all sections of an application.
        """
        self.sectionChart = Frame(self.root,bg='white',width=loader.conf["width"])
        self.sectionSettings = Frame(self.root,width=loader.conf["width"])

        self.sectionChart.grid(column=0,row=0,columnspan=1,rowspan=1,sticky=NSEW)
        self.sectionSettings.grid(column=0,row=1,columnspan=1,rowspan=1,sticky=NSEW)

        self.sectionChart.update()
        self.sectionSettings.update()

        self.buildSectionChart()
        self.buildSectionSettings()