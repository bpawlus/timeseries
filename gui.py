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

    _root = None
    """Reference to root window."""

    def buildSections(self):
        """Method meant to be overwritten.
        Constructs all sections of an application.
        """
        pass

    def buildGui(self):
        """Constructs and runs root window for an application.
        """
        self._root = Tk()
        self._root.title(loader.lang["title"])
        self._root.iconbitmap(loader.dirs["icon"])
        self._root.geometry(f'{loader.conf["width"]}x{loader.conf["height"]}')
        self._root.minsize(loader.conf["width"], loader.conf["height"])
        self._root.grid_rowconfigure(0, weight=1)
        self._root.grid_columnconfigure(0, weight=1)

        self.buildSections()
        self._root.mainloop()

class AnalyzerGui(Gui):
    """Class contains window application of time series analyzer.
    """

    _sectionChart: Frame = None
    """Section with chart that displays current data."""

    _sectionSettings: Frame = None
    """Section with settings that set properties of data."""
    _subsectionLoadData: Frame = None
    """Subsection of settings section that loads of data from memory."""
    _subsectionDataSelection: Frame = None
    """Subsection of settings section that allows user to choose displayed data, which was previously loaded."""
    _subsectionTSModules: Frame = None
    """Subsection of settings section that allows user to choose displayed time series analyzing modules."""

    _sectionOutput: Frame = None
    """Section with output functions that display and export data."""
    _subsectionStatisctics: Frame = None
    """Subsection of output section that displays data of modules in tabular form."""
    _subsectionLogger: Frame = None
    """Subsection of output section that logs user's actions."""
    _subsectionExportData: Frame = None
    """Subsection of output section that allows exporting logs, chart and statistics."""

    _hubimporters: HubImporters = HubImporters()
    """Functional component with methods concerning data importers."""
    _hubcharts: HubCharts = HubCharts()
    """Functional component with methods concerning loaded data in form of charts."""
    _hubtsmodules: HubTSModules = HubTSModules()
    """Functional component with methods concerning time series analyzing modules."""

    _importer: baseimport.ImportMethod = None
    """Chosen by user importer function (ex. .xls import when loading microsoft excel spreadsheet)."""
    _chartId: int = -1
    """ID of currently displayed chart"""

    def clear_sectionChart(self):
        """Method clears the view of section with chart.
        """
        for widget in self._sectionChart.winfo_children():
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
        self.chartscb['values'] = self._hubcharts.getAllChartDisplayNames()

    def updateChart(self):
        """Updates the view of section with chart.
        """
        self.clear_sectionChart()

        if(self._chartId != -1):
            self._hubcharts.displayChart(self._chartId, self._sectionChart, self._hubtsmodules.displayModules)
            self.statisticstabRefresh()

            self.outputModulescb['values'] = self._hubtsmodules.getAllActiveModuleNames()
            self.statisticstab['columns'] = []

    def deleteChart(self):
        """Deletes the current viewed chart.
        """
        self._hubcharts.removeChart(self._chartId)
        self._chartId = -1
        self.statisticstabRefresh()

        self.outputModulescb['values'] = []
        self.statisticstab['columns'] = []

        self.clear_sectionChart()


    def _subsectionLoadData_btnimport_action(self):
        """Method called when activating import button in
        subsection of settings section that loads of data from memory.
        Configures chosen importer function.
        """
        directory = filedialog.askopenfilename(initialdir="", title=loader.lang["settings"]["loaddata"]["import"], filetypes=(self._hubimporters.getAllMethods()))
        filename, fileextension = os.path.splitext(directory)
        for widget in self.importsettings.winfo_children():
            widget.destroy()

        self._importer = self._hubimporters.getImporterByFileextension(fileextension)
        if self._importer != None:
            self._importer.directory = directory
            self._importer.importSettingsGui(self.importsettings)
            self.btnexport['state'] = "normal"

    def _subsectionLoadData_btnexport_action(self):
        """Method called when activating export button in
        subsection of settings section that loads of data from memory.
        Exports data from importer to application's memory.
        """
        df = self._importer.extractData()
        if(not df.empty):
            self._hubcharts.addChart(df, title=self._importer.defaultTitle)
            self.updateChartsCb()

    def _subsectionDataSelection_btnupdate_action(self):
        """Method called when activating update button in
        subsection of settings section that allows user to choose displayed data, which was previously loaded.
        Updates chart displays with chosen data.
        """
        chart = self._hubcharts.getChartById(self._chartId)
        chart.title = self.titleentry.get()
        self.updateChartsCb()
        self.chartscb.set(f'{chart.title} ({chart.id})')
        self.updateChart()

    def _subsectionDataSelection_btndelete_action(self):
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

    def _subsectionDataSelection_chartscb_action(self, event):
        """Method called when updating charts combobox in
        subsection of settings section that allows user to choose displayed data, which was previously loaded.
        Updates the preview of selected data.
        """
        name = self.chartscbvar.get()
        self._chartId = self._hubcharts.getChartIdByDisplayName(name)
            
        self.textoutput['state'] = "normal"
        chart = self._hubcharts.getChartById(self._chartId)
        self.titleentry.set(chart.title)
            
        self.btndelete['state'] = "normal"
        self.btnupdate['state'] = "normal"

    def _subsectionTSModules_tsmodulesentrycb_action(self, event):
        """Method called when updating modules combobox in
        subsection of settings section that allows user to choose displayed time series analyzing modules.
        Rebuilds a menu with module parameters.
        """
        mod = self._hubtsmodules.getModuleByName(self.tsmodulesentry.get())
        mod.buildMenu(self.tsmodulesFrame)

    def _subsectionStatisctics_outputModulescb_action(self, event):
        """Method called when updating modules combobox in
        subsection of output section that displays data of modules in tabular form.
        Rebuilds a table view of analyzing module data.
        """
        
        for i in self.statisticstab.get_children():
            self.statisticstab.delete(i)
        self.statisticstab.column("#0", width=0, stretch=NO)
        self.statisticstab.heading("#0",text="",anchor=CENTER)

        df = self._hubtsmodules.getModuleByName(self.outputModules.get()).outputDataframe
        columns = df.columns.values.tolist()
        self.statisticstab['columns'] = columns

        for column in columns:
            self.statisticstab.column(column, anchor=CENTER, width=int(self._subsectionStatisctics.winfo_width()/len(columns)))
            self.statisticstab.heading(column,text=column,anchor=CENTER)

        data = df.values.tolist()
        for v in data:
            self.statisticstab.insert('', END, values=v)

    def _subsectionExportData_btnexportchart_action(self):
        """Method called when activating export button in
        subsection of output section that allows exporting logs, chart and statistics
        Exports displayed chart to image format.
        """
        if(self._chartId != -1):
            chart = self._hubcharts.getChartById(self._chartId)
            chart.exportChart(loader.dirs["exportchart"])
            messagebox.showinfo(loader.lang["messagebox"]["info"], f'{loader.lang["output"]["exportdata"]["successexportchart"]}{loader.dirs["exportchart"]}')
        else:
            messagebox.showerror(loader.lang["messagebox"]["error"], loader.lang["output"]["exportdata"]["failedexport"])

    def _subsectionExportData_btnexportlogs_action(self):
        """Method called when activating export button in
        subsection of output section that allows exporting logs, chart and statistics
        Exports logs to text format.
        """
        f = open(loader.dirs["exportlogname"], "w")
        f.write(self.loggertextoutput.get("1.0",END))
        f.close()
        messagebox.showinfo(loader.lang["messagebox"]["info"], f'{loader.lang["output"]["exportdata"]["successexportlogs"]}{loader.dirs["exportlogname"]}')

    def _subsectionExportData_btnexportstats_action(self):
        """Method called when activating export button in
        subsection of output section that allows exporting logs, chart and statistics
        Exports output modules data to text format.
        """
        if(self._chartId != -1):
            f = open(loader.dirs["exportstats"], "w")
            mods = self._hubtsmodules.getAllActiveModules()
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
        self._subsectionLoadData.grid_columnconfigure(0, weight=1)

        #Width formula: 13, 20, 27, 34... 13 + 7n
        self.importsettings = Frame(self._subsectionLoadData, width=self._subsectionLoadData.winfo_width())
        self.importsettings.grid(row=2)
        
        self.btnexport = Button(self._subsectionLoadData, state="disabled", text=loader.lang["settings"]["loaddata"]["select"], command=self._subsectionLoadData_btnexport_action, pady=5, width=int((self._subsectionLoadData.winfo_width()-13)/7)+1)
        self.btnexport.grid(row=3)

        btnimport = Button(self._subsectionLoadData, text=loader.lang["settings"]["loaddata"]["import"], command=self._subsectionLoadData_btnimport_action, pady=5, width=int((self._subsectionLoadData.winfo_width()-13)/7)+1)
        btnimport.grid(row=1)

    def buildSubsectionDataSelection(self):
        """Builds subsection of settings section that allows user to choose displayed data, which was previously loaded.
        """
        self._subsectionDataSelection.grid_columnconfigure(0, weight=1)
        
        labcharts = Label(self._subsectionDataSelection, text=loader.lang["settings"]["charts"]["select"], pady=5, width=int((self._subsectionDataSelection.winfo_width()-13)/7)+1)
        labcharts.grid(row=1)
        self.chartscbvar = StringVar()
        self.chartscb = ttk.Combobox(self._subsectionDataSelection, state="readonly", textvariable=self.chartscbvar, width=int((self._subsectionDataSelection.winfo_width()-13)/7)+1)
        self.chartscb.grid(row=2)

        labcharts = Label(self._subsectionDataSelection, text=loader.lang["settings"]["charts"]["titlechanger"], pady=5, width=int((self._subsectionDataSelection.winfo_width()-13)/7)+1)
        labcharts.grid(row=3)
        self.titleentry = StringVar()
        self.textoutput = Entry(self._subsectionDataSelection, textvariable=self.titleentry, state="disabled", width=int((self._subsectionDataSelection.winfo_width()-13)/7)+1)
        self.textoutput.grid(row=4)

        self.btnupdate = Button(self._subsectionDataSelection, state="disabled", text=loader.lang["settings"]["charts"]["update"], command=self._subsectionDataSelection_btnupdate_action, pady=5, width=int((self._subsectionDataSelection.winfo_width()-13)/7)+1)
        self.btnupdate.grid(row=5)

        self.btndelete = Button(self._subsectionDataSelection, state="disabled", text=loader.lang["settings"]["charts"]["delete"], command=self._subsectionDataSelection_btndelete_action, pady=5, width=int((self._subsectionDataSelection.winfo_width()-13)/7)+1)
        self.btndelete.grid(row=6)

        self.chartscb.bind('<<ComboboxSelected>>', self._subsectionDataSelection_chartscb_action)   

    def buildSubsectionTSModules(self):
        """Builds subsection of settings section that allows user to choose displayed time series analyzing modules.
        """
        self._subsectionTSModules.grid_columnconfigure(0, weight=1)

        labtsmodules = Label(self._subsectionTSModules, text=loader.lang["settings"]["modules"]["modules"], pady=5, width=int((self._subsectionTSModules.winfo_width()-13)/7)+1)
        labtsmodules.grid(row=1)
        self.tsmodulesentry = StringVar()
        tsmodulesentrycb = ttk.Combobox(self._subsectionTSModules, state="readonly", textvariable=self.tsmodulesentry, width=int((self._subsectionTSModules.winfo_width()-13)/7)+1)
        tsmodulesentrycb.grid(row=2)
        tsmodulesentrycb['values'] = self._hubtsmodules.getAllModuleNames()

        self.tsmodulesFrame = Frame(self._subsectionTSModules, width=self._subsectionTSModules.winfo_width())
        self.tsmodulesFrame.grid(row=3)
        
        btnexport = Button(self._subsectionTSModules, text=loader.lang["settings"]["modules"]["update"], command=self.updateChart, pady=5, width=int((self._subsectionTSModules.winfo_width()-13)/7)+1)
        btnexport.grid(row=4)

        tsmodulesentrycb.bind('<<ComboboxSelected>>', self._subsectionTSModules_tsmodulesentrycb_action)   

    def buildSubsectionStatisctics(self):
        """Builds subsection of output section that displays data of modules in tabular form.
        """
        self._subsectionStatisctics.grid_columnconfigure(0, weight=1)

        labcharts = Label(self._subsectionStatisctics, text=loader.lang["output"]["statistics"]["modules"], pady=5, width=int((self._subsectionStatisctics.winfo_width()-13)/7)+1)
        labcharts.grid(row=1)
        self.outputModules = StringVar()
        self.outputModulescb = ttk.Combobox(self._subsectionStatisctics, state="readonly", textvariable=self.outputModules, width=int((self._subsectionStatisctics.winfo_width()-13)/7)+1)
        self.outputModulescb.grid(row=2)

        self.statisticstab = ttk.Treeview(self._subsectionStatisctics)
        self.statisticstab.grid(row=3, sticky=NSEW)
        self.statisticstab.column("#0", width=self._subsectionStatisctics.winfo_width(), stretch=YES)
        self.statisticstab.heading("#0",text="",anchor=CENTER)
       
        self.outputModulescb.bind('<<ComboboxSelected>>', self._subsectionStatisctics_outputModulescb_action)   

    def buildSubsectionLogger(self):
        """Builds subsection of output section that logs user's actions.
        """
        self._subsectionLogger.grid_columnconfigure(0, weight=1)

        #Height formula: 4 + 16n
        self.loggertextoutput = Text(self._subsectionLogger, width=self._subsectionLogger.winfo_width(), height=int(((self._subsectionLogger.winfo_height()-4)/16+1)))
        self.loggertextoutput.grid(row=1, sticky=NSEW)

        logger.win = self.loggertextoutput
        logger.log("Initiated")

    def buildSubsectionExportData(self):
        """Builds subsection of output section that allows exporting logs, chart and statistics.
        """
        self._subsectionExportData.grid_columnconfigure(0, weight=1)

        btnexportchart = Button(self._subsectionExportData, text=loader.lang["output"]["exportdata"]["exportchart"], command=self._subsectionExportData_btnexportchart_action, pady=5, width=int((self._subsectionExportData.winfo_width()-13)/7)+1)
        btnexportchart.grid(row=1)

        btnexportlogs = Button(self._subsectionExportData, text=loader.lang["output"]["exportdata"]["exportlogs"], command=self._subsectionExportData_btnexportlogs_action, pady=5, width=int((self._subsectionExportData.winfo_width()-13)/7)+1)
        btnexportlogs.grid(row=2)

        btnexportstats = Button(self._subsectionExportData, text=loader.lang["output"]["exportdata"]["exportstats"], command=self._subsectionExportData_btnexportstats_action, pady=5, width=int((self._subsectionExportData.winfo_width()-13)/7)+1)
        btnexportstats.grid(row=3)


    def buildSectionChart(self):
        """Builds section with chart that displays current data.
        """
        self._sectionChart.grid_columnconfigure(0, weight=1)
        self._sectionChart.grid_rowconfigure(0, weight=1)
        
    def buildSectionSettings(self):
        """Builds section with settings that set properties of data.
        """
        self._sectionSettings.grid_columnconfigure(0, weight=1)
        self._sectionSettings.grid_rowconfigure(0, weight=1)

        settingsnotebook = ttk.Notebook(self._sectionSettings)

        self._subsectionLoadData = Frame(settingsnotebook,width=self._sectionSettings.winfo_width(),height=self._sectionSettings.winfo_height())
        self._subsectionDataSelection = Frame(settingsnotebook,width=self._sectionSettings.winfo_width(),height=self._sectionSettings.winfo_height())
        self._subsectionTSModules = Frame(settingsnotebook,width=self._sectionSettings.winfo_width(),height=self._sectionSettings.winfo_height())

        settingsnotebook.add(self._subsectionLoadData, text=loader.lang["settings"]["loaddata"]["header"])
        settingsnotebook.add(self._subsectionDataSelection, text=loader.lang["settings"]["charts"]["header"])
        settingsnotebook.add(self._subsectionTSModules, text=loader.lang["settings"]["modules"]["header"])

        settingsnotebook.pack(expand=1, fill='both')

        self._subsectionLoadData.update()
        self._subsectionDataSelection.update()
        self._subsectionTSModules.update()
        settingsnotebook.select(0)
        self.buildSubsectionLoadData()

        self._subsectionLoadData.update()
        self._subsectionDataSelection.update()
        self._subsectionTSModules.update()
        settingsnotebook.select(1)
        self.buildSubsectionDataSelection()

        self._subsectionLoadData.update()
        self._subsectionDataSelection.update()
        self._subsectionTSModules.update()
        settingsnotebook.select(2)
        self.buildSubsectionTSModules()

        self._subsectionLoadData.update()
        self._subsectionDataSelection.update()
        self._subsectionTSModules.update()
        settingsnotebook.select(0)

    def buildSectionOutput(self):
        """Builds section with output functions that display and export data.
        """
        self._sectionOutput.grid_columnconfigure(0, weight=1)
        self._sectionOutput.grid_rowconfigure(0, weight=1)

        outputnotebook = ttk.Notebook(self._sectionOutput)

        self._subsectionStatisctics = Frame(outputnotebook,width=self._sectionOutput.winfo_width(),height=self._sectionOutput.winfo_height())
        self._subsectionLogger = Frame(outputnotebook,width=self._sectionOutput.winfo_width(),height=self._sectionOutput.winfo_height())
        self._subsectionExportData = Frame(outputnotebook,width=self._sectionOutput.winfo_width(),height=self._sectionOutput.winfo_height())

        outputnotebook.add(self._subsectionStatisctics, text=loader.lang["output"]["statistics"]["header"])
        outputnotebook.add(self._subsectionLogger, text=loader.lang["output"]["logger"]["header"])
        outputnotebook.add(self._subsectionExportData, text=loader.lang["output"]["exportdata"]["header"])

        outputnotebook.pack(expand=1, fill='both')

        self._subsectionStatisctics.update()
        self._subsectionLogger.update()
        self._subsectionExportData.update()
        outputnotebook.select(0)
        self.buildSubsectionStatisctics()

        self._subsectionStatisctics.update()
        self._subsectionLogger.update()
        self._subsectionExportData.update()
        outputnotebook.select(1)
        self.buildSubsectionLogger()

        self._subsectionStatisctics.update()
        self._subsectionLogger.update()
        self._subsectionExportData.update()
        outputnotebook.select(2)
        self.buildSubsectionExportData()

        self._subsectionStatisctics.update()
        self._subsectionLogger.update()
        self._subsectionExportData.update()
        outputnotebook.select(0)

    def buildSections(self):
        """Constructs all sections of an application.
        """
        self._hubimporters.loadImporters()
        self._hubtsmodules.loadModules()

        self._sectionChart = Frame(self._root,bg='white',width=loader.conf["width"]*0.75, height=loader.conf["height"]*0.5)
        self._sectionSettings = Frame(self._root,bg='white',width=loader.conf["width"]*0.25, height=loader.conf["height"])
        self._sectionOutput = Frame(self._root,bg='white',width=loader.conf["width"]*0.75, height=loader.conf["height"]*0.5)

        self._sectionChart.grid(column=0,row=0,columnspan=3,rowspan=2,sticky=NSEW)
        self._sectionSettings.grid(column=3,row=0,columnspan=1,rowspan=4,sticky=NSEW)
        self._sectionOutput.grid(column=0,row=2,columnspan=3,rowspan=2,sticky=NSEW)

        self._sectionChart.update()
        self._sectionSettings.update()
        self._sectionOutput.update()

        self.buildSectionChart()
        self.buildSectionSettings()
        self.buildSectionOutput()

class GeneratorGui(Gui):
    _sectionChart: Frame = None
    """Section with chart that displays current generated data."""

    _sectionSettings: Frame = None
    """Section with settings that set properties of generated data."""
    _sectionsubChartgenerator: Frame = None
    """Subsection of settings section that configures parameters of generated chart."""
    _subsectionExportData: Frame = None
    """Subsection of settings section that allows exporting generated chart and statistics."""

    _df = DataFrame()
    """Data frame of generated signal."""
    _cps = None
    """Generated change point indexes."""
    _means = None
    """Means in area between change points, before applying noise."""
    _spreads = None
    """Variances in area between change points, before applying noise."""

    _cpCount = 2
    """Number of change points in generated signal."""
    _samples = 100
    """Number of samples (data length) in generated signal."""
    _meanVar = None
    """Mean of all data in generated signal."""
    _spreadVar = None
    """Spread of mean of all data in generated signal."""
    _cpspreadVar = None
    """Variance in areas between change points in generated signal."""
    _spreadcpspreadVar = None
    """Spread of variance in areas between change points in generated signal."""

    def _subsectionExportData_btnupdate_action(self):
        """Method called when activating export button in
        subsection of settings section that allows exporting generated chart and statistics.
        Generates a new, randomized signal.
        """
        for widget in self._sectionChart.winfo_children():
            widget.destroy()

        step = self._samples/(self._cpCount+1)

        x = 0
        self._cps = [0]
        self._means = [random.uniform(self._meanVar.get()-self._spreadVar.get(), self._meanVar.get()+self._spreadVar.get())]
        self._spreads = [abs(random.uniform(self._cpspreadVar.get()-self._spreadcpspreadVar.get(), self._cpspreadVar.get()+self._spreadcpspreadVar.get()))]

        for i in range(self._cpCount):
            x += step
            self._cps.append(random.randint(int(x-step/2+1), int(x+step/2-1)))
            self._means.append(random.uniform(self._meanVar.get()-self._spreadVar.get(), self._meanVar.get()+self._spreadVar.get()))
            self._spreads.append(abs(random.uniform(self._cpspreadVar.get()-self._spreadcpspreadVar.get(), self._cpspreadVar.get()+self._spreadcpspreadVar.get())))
            
        self.dfdatay = []
        rects = []
        self._cps.append(self._samples)

        for i in range(len(self._cps)-1):
            cplen = self._cps[i+1]-self._cps[i]
            data = numpy.random.normal(self._means[i], self._spreads[i], cplen)
            self.dfdatay.extend(data)
            rects.append(patches.Rectangle((self._cps[i], self._means[i]-self._spreads[i]), cplen, 2*self._spreads[i], linewidth=2, edgecolor='#FFFF00', facecolor='none'))

        self._cps[len(self._cps)-1] -= 1
        self.dfdata = {
            "X": [x for x in range(self._samples)],
            "Y": self.dfdatay
        }

        self._df = DataFrame(self.dfdata,columns=["X","Y"])
        figure = plt.Figure(dpi=100)
        ax = figure.add_subplot(111)

        figure = FigureCanvasTkAgg(figure, self._sectionChart)
        figure.get_tk_widget().grid(row=0)

        self._df = self._df[["X", "Y"]].groupby("X").sum()
        self._df.plot(kind='line', legend=FALSE, ax=ax, color='r',marker='o', fontsize=4, markersize=2)

        for patch in rects:
            ax.add_patch(patch)

        ax.set_title(loader.lang["settings-gen"]["chartname"])
        self.btnexport['state'] = "normal"

    def _subsectionExportData_btnexport_action(self):
        """Method called when activating export button in
        subsection of settings section that allows exporting generated chart and statistics.
        Exports generated data to text format and csv spreadsheet.
        """
        if not self._df.empty:
            f = open(loader.dirs["geninfo"], "w")
            f.write(loader.lang["settings-gen"]["results"]["cps"] + "\n")
            f.write(' '.join([str(e) for e in self._cps]))
            f.write("\n\n")
            f.write(loader.lang["settings-gen"]["results"]["means"] + "\n")
            f.write(' '.join([str(e) for e in self._means]))
            f.write("\n\n")
            f.write(loader.lang["settings-gen"]["results"]["spreads"] + "\n")
            f.write(' '.join([str(e) for e in self._spreads]))
            f.close()
            self._df.to_csv(loader.dirs["gen"])
            messagebox.showinfo(loader.lang["messagebox"]["info"], loader.lang["settings-gen"]["results"]["exportinfo"] + "\n" + loader.dirs["geninfo"] + "\n" + loader.dirs["gen"])


    def buildSubSectionChartGenerator(self):
        """Builds subsection of settings section that configures parameters of generated chart.
        """
        self._sectionsubChartgenerator.grid_columnconfigure(0, weight=1)

        labpoints = Label(self._sectionsubChartgenerator, text=loader.lang["settings-gen"]["generator"]["cpcount"], pady=5, width=int((self._sectionsubChartgenerator.winfo_width()-13)/7)+1)
        labpoints.grid(row=1)
        changePointCount = Scale(self._sectionsubChartgenerator, from_=0, to=10, tickinterval=2, orient=HORIZONTAL, length=int(self._sectionsubChartgenerator.winfo_width()))
        changePointCount.set(self._cpCount)
        changePointCount.grid(row=2)

        def updateChangePointCount(event):
            self._cpCount = int(changePointCount.get())

        changePointCount.bind("<ButtonRelease-1>", updateChangePointCount)

        labsamples = Label(self._sectionsubChartgenerator, text=loader.lang["settings-gen"]["generator"]["samples"], pady=5, width=int((self._sectionsubChartgenerator.winfo_width()-13)/7)+1)
        labsamples.grid(row=3)
        self.samplesCount = Scale(self._sectionsubChartgenerator, from_=100, to=500, tickinterval=50, orient=HORIZONTAL, length=int(self._sectionsubChartgenerator.winfo_width()))
        self.samplesCount.set(self._samples)
        self.samplesCount.grid(row=4)

        def updateSamplesCount(event):
            self._samples = int(self.samplesCount.get())

        self.samplesCount.bind("<ButtonRelease-1>", updateSamplesCount)

        labmean = Label(self._sectionsubChartgenerator, text=loader.lang["settings-gen"]["generator"]["mean"], pady=5, width=int((self._sectionsubChartgenerator.winfo_width()-13)/7)+1)
        labmean.grid(row=5)
        if not self._meanVar:
            self._meanVar = DoubleVar()
            self._meanVar.set(0.0)
        vcmd = (self._sectionsubChartgenerator.register(entryvalidators.validate_floatentries),'%P')
        meanentry = Entry(self._sectionsubChartgenerator, textvariable=self._meanVar, validate='all', validatecommand=vcmd, width=int((self._sectionsubChartgenerator.winfo_width()-13)/7)+1)
        meanentry.grid(row=6)

        labspread = Label(self._sectionsubChartgenerator, text=loader.lang["settings-gen"]["generator"]["spread"], pady=5, width=int((self._sectionsubChartgenerator.winfo_width()-13)/7)+1)
        labspread.grid(row=7)
        if not self._spreadVar:
            self._spreadVar = DoubleVar()
            self._spreadVar.set(2.5)
        vcmd = (self._sectionsubChartgenerator.register(entryvalidators.validate_floatentries),'%P')
        spreadentry = Entry(self._sectionsubChartgenerator, textvariable=self._spreadVar, validate='all', validatecommand=vcmd, width=int((self._sectionsubChartgenerator.winfo_width()-13)/7)+1)
        spreadentry.grid(row=8)

        cpspread = Label(self._sectionsubChartgenerator, text=loader.lang["settings-gen"]["generator"]["cpspread"], pady=5, width=int((self._sectionsubChartgenerator.winfo_width()-13)/7)+1)
        cpspread.grid(row=9)
        if not self._cpspreadVar:
            self._cpspreadVar = DoubleVar()
            self._cpspreadVar.set(0.75)
        vcmd = (self._sectionsubChartgenerator.register(entryvalidators.validate_floatentries),'%P')
        cpspreadentry = Entry(self._sectionsubChartgenerator, textvariable=self._cpspreadVar, validate='all', validatecommand=vcmd, width=int((self._sectionsubChartgenerator.winfo_width()-13)/7)+1)
        cpspreadentry.grid(row=10)

        labspreadcpspread = Label(self._sectionsubChartgenerator, text=loader.lang["settings-gen"]["generator"]["spreadcpspread"], pady=5, width=int((self._sectionsubChartgenerator.winfo_width()-13)/7)+1)
        labspreadcpspread.grid(row=11)
        if not self._spreadcpspreadVar:
            self._spreadcpspreadVar = DoubleVar()
            self._spreadcpspreadVar.set(0.0)
        vcmd = (self._sectionsubChartgenerator.register(entryvalidators.validate_floatentries),'%P')
        spreadcpspreadentry = Entry(self._sectionsubChartgenerator, textvariable=self._spreadcpspreadVar, validate='all', validatecommand=vcmd, width=int((self._sectionsubChartgenerator.winfo_width()-13)/7)+1)
        spreadcpspreadentry.grid(row=12)

    def buildSubSectionExportData(self):
        """Builds subsection of settings section that allows exporting generated chart and statistics.
        """
        self._subsectionExportData.grid_columnconfigure(0, weight=1)

        btnupdate = Button(self._subsectionExportData, text=loader.lang["settings-gen"]["output"]["update"], pady=5, width=int((self._subsectionExportData.winfo_width()-13)/7)+1)
        btnupdate.grid(row=1)

        self.btnexport = Button(self._subsectionExportData, state="disabled", text=loader.lang["settings-gen"]["output"]["export"], pady=5, width=int((self._subsectionExportData.winfo_width()-13)/7)+1)
        self.btnexport.grid(row=2)

        btnupdate.configure(command=self._subsectionExportData_btnupdate_action)
        self.btnexport.configure(command=self._subsectionExportData_btnexport_action)
        

    def buildSectionChart(self):
        """Builds section with chart that displays current generated data.
        """
        self._sectionChart.grid_columnconfigure(0, weight=1)
        self._sectionChart.grid_rowconfigure(0, weight=1)

    def buildSectionSettings(self):
        """Builds section with settings that set properties of generated data.
        """
        self._sectionSettings.grid_columnconfigure(0, weight=1)
        self._sectionSettings.grid_rowconfigure(0, weight=1)

        notebook = ttk.Notebook(self._sectionSettings)

        self._sectionsubChartgenerator = Frame(notebook,width=self._sectionSettings.winfo_width(),height=self._sectionSettings.winfo_height())
        self._subsectionExportData = Frame(notebook,width=self._sectionSettings.winfo_width(),height=self._sectionSettings.winfo_height())

        notebook.add(self._sectionsubChartgenerator, text=loader.lang["settings-gen"]["generator"]["header"])
        notebook.add(self._subsectionExportData, text=loader.lang["settings-gen"]["output"]["header"])

        notebook.pack(expand=1, fill='both')

        self._sectionsubChartgenerator.update()
        self._subsectionExportData.update()
        notebook.select(0)
        self.buildSubSectionChartGenerator()

        self._sectionsubChartgenerator.update()
        self._subsectionExportData.update()
        notebook.select(1)
        self.buildSubSectionExportData()

        self._sectionsubChartgenerator.update()
        self._subsectionExportData.update()
        notebook.select(0)

    def buildSections(self):
        """Constructs all sections of an application.
        """
        self._sectionChart = Frame(self._root,bg='white',width=loader.conf["width"])
        self._sectionSettings = Frame(self._root,width=loader.conf["width"])

        self._sectionChart.grid(column=0,row=0,columnspan=1,rowspan=1,sticky=NSEW)
        self._sectionSettings.grid(column=0,row=1,columnspan=1,rowspan=1,sticky=NSEW)

        self._sectionChart.update()
        self._sectionSettings.update()

        self.buildSectionChart()
        self.buildSectionSettings()