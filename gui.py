from tkinter import *
from tkinter import ttk, filedialog, messagebox
import os
from pandas.core.frame import DataFrame
from dataGenerator import SignalGenerator
import loader
from hubCharts import HubCharts
from hubImporters import HubImporters
from hubTSModules import HubTSModules
from importers import baseimport
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logger
import entryvalidators


class Gui():
    """Base class responsible for constructing window application.
    """

    __root = None
    """Reference to root window."""

    def _buildSections(self):
        """Method meant to be overwritten.
        Constructs all sections of an application.
        """
        print("dsassa")
        pass

    def getRoot(self):
        return self.__root

    def buildGui(self):
        """Constructs and runs root window for an application.
        """
        self.__root = Tk()
        self.__root.title(loader.lang["title"])
        self.__root.iconbitmap(loader.dirs["icon"])
        self.__root.geometry(f'{loader.conf["width"]}x{loader.conf["height"]}')
        self.__root.minsize(loader.conf["width"], loader.conf["height"])
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        self._buildSections()
        self.__root.mainloop()

class AnalyzerGui(Gui):
    """Class contains window application of time series analyzer.
    """

    __sectionChart: Frame = None
    """Section with chart that displays current data."""

    __sectionSettings: Frame = None
    """Section with settings that set properties of data."""
    __subsectionLoadData: Frame = None
    """Subsection of settings section that loads of data from memory."""
    __subsectionDataSelection: Frame = None
    """Subsection of settings section that allows user to choose displayed data, which was previously loaded."""
    __subsectionTSModules: Frame = None
    """Subsection of settings section that allows user to choose displayed time series analyzing modules."""

    __sectionOutput: Frame = None
    """Section with output functions that display and export data."""
    __subsectionStatisctics: Frame = None
    """Subsection of output section that displays data of modules in tabular form."""
    __subsectionLogger: Frame = None
    """Subsection of output section that logs user's actions."""
    __subsectionExportData: Frame = None
    """Subsection of output section that allows exporting logs, chart and statistics."""

    __hubImporters: HubImporters = HubImporters()
    """Functional component with methods concerning data importers."""
    __hubCharts: HubCharts = HubCharts()
    """Functional component with methods concerning loaded data in form of charts."""
    __hubTSModules: HubTSModules = HubTSModules()
    """Functional component with methods concerning time series analyzing modules."""

    __importer: baseimport.ImportMethod = None
    """Chosen by user importer function (ex. .xls import when loading microsoft excel spreadsheet)."""
    __chartId: int = -1
    """ID of currently displayed chart"""

    def __clearSectionChart(self):
        """Method clears the view of section with chart.
        """
        for widget in self.__sectionChart.winfo_children():
            widget.destroy()

    def __refreshTreeviewStatistics(self):
        """Removes the content of combobox and table view with all active time series modules.
        """
        self.__comboboxOutputModules.set('')
        for i in self.__treeviewStatistics.get_children():
            self.__treeviewStatistics.delete(i)

    def __updateComboboxCharts(self):
        """Refreshes the content of combobox with all loaded time series modules.
        """
        self.__comboboxCharts['values'] = self.__hubCharts.getAllChartDisplayNames()

    def __updateChart(self):
        """Updates the view of section with chart.
        """
        self.__clearSectionChart()

        if(self.__chartId != -1):
            self.__hubCharts.displayChart(self.__chartId, self.__sectionChart, self.__hubTSModules.displayModules)
            self.__refreshTreeviewStatistics()

            self.__comboboxOutputModules['values'] = self.__hubTSModules.getAllActiveModuleNames()
            self.__treeviewStatistics['columns'] = []

    def __deleteChart(self):
        """Deletes the current viewed chart.
        """
        self.__hubCharts.removeChart(self.__chartId)
        self.__chartId = -1
        self.__refreshTreeviewStatistics()

        self.__comboboxOutputModules['values'] = []
        self.__treeviewStatistics['columns'] = []

        self.__clearSectionChart()


    def __subsectionLoadData_buttonImportData_action(self):
        """Method called when activating import button in
        subsection of settings section that loads of data from memory.
        Configures chosen importer function.
        """
        directory = filedialog.askopenfilename(initialdir="", title=loader.lang["settings"]["loaddata"]["import"], filetypes=(self.__hubImporters.getAllMethods()))
        filename, fileextension = os.path.splitext(directory)
        for widget in self.__frameImportSettings.winfo_children():
            widget.destroy()

        self.__importer = self.__hubImporters.getImporterByFileextension(fileextension)
        if self.__importer != None:
            self.__importer.setDirectory(directory)
            self.__importer.importSettingsGui(self.__frameImportSettings)
            self.__buttonImportDataFromFile['state'] = "normal"

    def __subsectionLoadData_buttonImportDataFromFile_action(self):
        """Method called when activating export button in
        subsection of settings section that loads of data from memory.
        Exports data from importer to application's memory.
        """
        df = self.__importer.extractData()
        if(not df.empty):
            self.__hubCharts.addChart(df, title=self.__importer.getDefaultTitle())
            self.__updateComboboxCharts()

    def __subsectionDataSelection_buttonUpdateData_action(self):
        """Method called when activating update button in
        subsection of settings section that allows user to choose displayed data, which was previously loaded.
        Updates chart displays with chosen data.
        """
        chart = self.__hubCharts.getChartById(self.__chartId)
        chart.setTitle(self.__outvarRenameData.get())
        self.__updateComboboxCharts()
        self.__comboboxCharts.set(f'{chart.getTitle()} ({chart.getId()})')
        self.__updateChart()

    def __subsectionDataSelection_buttonDeleteData_action(self):
        """Method called when activating delete button in
        subsection of settings section that allows user to choose displayed data, which was previously loaded.
        Deletes selected data.
        """
        self.__deleteChart()
        self.__updateComboboxCharts()
        self.__comboboxCharts.set("")             

        self.__entryRenameData['state'] = "disabled"
        self.__outvarRenameData.set("")
        self.__buttonDeleteData['state'] = "disabled"
        self.__buttonUpdateData['state'] = "disabled"

    def __subsectionDataSelection_chartscb_action(self, event):
        """Method called when updating charts combobox in
        subsection of settings section that allows user to choose displayed data, which was previously loaded.
        Updates the preview of selected data.
        """
        name = self.__outvarCharts.get()
        self.__chartId = self.__hubCharts.getChartIdByDisplayName(name)
            
        self.__entryRenameData['state'] = "normal"
        chart = self.__hubCharts.getChartById(self.__chartId)
        self.__outvarRenameData.set(chart.getTitle())
            
        self.__buttonDeleteData['state'] = "normal"
        self.__buttonUpdateData['state'] = "normal"

    def __subsectionTSModules_comboboxTSModule_action(self, event):
        """Method called when updating modules combobox in
        subsection of settings section that allows user to choose displayed time series analyzing modules.
        Rebuilds a menu with module parameters.
        """
        mod = self.__hubTSModules.getModuleByName(self.__outvarTSModule.get())
        mod.buildMenu(self.__frameTSModules)

    def __subsectionStatisctics_comboboxOutputModules_action(self, event):
        """Method called when updating modules combobox in
        subsection of output section that displays data of modules in tabular form.
        Rebuilds a table view of analyzing module data.
        """
        
        for i in self.__treeviewStatistics.get_children():
            self.__treeviewStatistics.delete(i)
        self.__treeviewStatistics.column("#0", width=0, stretch=NO)
        self.__treeviewStatistics.heading("#0",text="",anchor=CENTER)

        df = self.__hubTSModules.getModuleByName(self.__outvarOutputModules.get()).outputDf
        columns = df.columns.values.tolist()
        self.__treeviewStatistics['columns'] = columns

        for column in columns:
            self.__treeviewStatistics.column(column, anchor=CENTER, width=int(self.__subsectionStatisctics.winfo_width()/len(columns)))
            self.__treeviewStatistics.heading(column,text=column,anchor=CENTER)

        data = df.values.tolist()
        for v in data:
            self.__treeviewStatistics.insert('', END, values=v)

    def __subsectionExportData_buttonExportChart_action(self):
        """Method called when activating export button in
        subsection of output section that allows exporting logs, chart and statistics
        Exports displayed chart to image format.
        """
        if(self.__chartId != -1):
            chart = self.__hubCharts.getChartById(self.__chartId)
            chart.exportChart(loader.dirs["exportchart"])
            messagebox.showinfo(loader.lang["messagebox"]["info"], f'{loader.lang["output"]["exportdata"]["successexportchart"]}{loader.dirs["exportchart"]}')
        else:
            messagebox.showerror(loader.lang["messagebox"]["error"], loader.lang["output"]["exportdata"]["failedexport"])

    def __subsectionExportData_buttonExportLogs_action(self):
        """Method called when activating export button in
        subsection of output section that allows exporting logs, chart and statistics
        Exports logs to text format.
        """
        f = open(loader.dirs["exportlogname"], "w")
        f.write(self.__outtextfieldLogger.get("1.0",END))
        f.close()
        messagebox.showinfo(loader.lang["messagebox"]["info"], f'{loader.lang["output"]["exportdata"]["successexportlogs"]}{loader.dirs["exportlogname"]}')

    def __subsectionExportData_buttonExportStats_action(self):
        """Method called when activating export button in
        subsection of output section that allows exporting logs, chart and statistics
        Exports output modules data to text format.
        """
        if(self.__chartId != -1):
            f = open(loader.dirs["exportstats"], "w")
            mods = self.__hubTSModules.getAllActiveModules()
            for mod in mods:
                f.write(mod.getModuleName())
                f.write("\n")
                f.write(mod.outputDf.to_string())
                f.write("\n\n")
            f.close()
            messagebox.showinfo(loader.lang["messagebox"]["info"], f'{loader.lang["output"]["exportdata"]["successexportstats"]}{loader.dirs["exportstats"]}')
        else:
            messagebox.showerror(loader.lang["messagebox"]["error"], loader.lang["output"]["exportdata"]["failedexport"])


    def __buildSubsectionLoadData(self):
        """Builds subsection of settings section that loads of data from memory.
        """
        self.__subsectionLoadData.grid_columnconfigure(0, weight=1)

        #Width formula: 13, 20, 27, 34... 13 + 7n
        self.__frameImportSettings = Frame(self.__subsectionLoadData, width=self.__subsectionLoadData.winfo_width())
        self.__frameImportSettings.grid(row=2)
        
        self.__buttonImportDataFromFile = Button(self.__subsectionLoadData, state="disabled", text=loader.lang["settings"]["loaddata"]["select"], command=self.__subsectionLoadData_buttonImportDataFromFile_action, pady=5, width=int((self.__subsectionLoadData.winfo_width()-13)/7)+1)
        self.__buttonImportDataFromFile.grid(row=3)

        buttonImportData = Button(self.__subsectionLoadData, text=loader.lang["settings"]["loaddata"]["import"], command=self.__subsectionLoadData_buttonImportData_action, pady=5, width=int((self.__subsectionLoadData.winfo_width()-13)/7)+1)
        buttonImportData.grid(row=1)

    def __buildSubsectionDataSelection(self):
        """Builds subsection of settings section that allows user to choose displayed data, which was previously loaded.
        """
        self.__subsectionDataSelection.grid_columnconfigure(0, weight=1)
        
        labelCharts = Label(self.__subsectionDataSelection, text=loader.lang["settings"]["charts"]["select"], pady=5, width=int((self.__subsectionDataSelection.winfo_width()-13)/7)+1)
        labelCharts.grid(row=1)
        self.__outvarCharts = StringVar()
        self.__comboboxCharts = ttk.Combobox(self.__subsectionDataSelection, state="readonly", textvariable=self.__outvarCharts, width=int((self.__subsectionDataSelection.winfo_width()-13)/7)+1)
        self.__comboboxCharts.grid(row=2)

        labelTitleChange = Label(self.__subsectionDataSelection, text=loader.lang["settings"]["charts"]["titlechanger"], pady=5, width=int((self.__subsectionDataSelection.winfo_width()-13)/7)+1)
        labelTitleChange.grid(row=3)
        self.__outvarRenameData = StringVar()
        self.__entryRenameData = Entry(self.__subsectionDataSelection, textvariable=self.__outvarRenameData, state="disabled", width=int((self.__subsectionDataSelection.winfo_width()-13)/7)+1)
        self.__entryRenameData.grid(row=4)

        self.__buttonUpdateData = Button(self.__subsectionDataSelection, state="disabled", text=loader.lang["settings"]["charts"]["update"], command=self.__subsectionDataSelection_buttonUpdateData_action, pady=5, width=int((self.__subsectionDataSelection.winfo_width()-13)/7)+1)
        self.__buttonUpdateData.grid(row=5)

        self.__buttonDeleteData = Button(self.__subsectionDataSelection, state="disabled", text=loader.lang["settings"]["charts"]["delete"], command=self.__subsectionDataSelection_buttonDeleteData_action, pady=5, width=int((self.__subsectionDataSelection.winfo_width()-13)/7)+1)
        self.__buttonDeleteData.grid(row=6)

        self.__comboboxCharts.bind('<<ComboboxSelected>>', self.__subsectionDataSelection_chartscb_action)   

    def __buildSubsectionTSModules(self):
        """Builds subsection of settings section that allows user to choose displayed time series analyzing modules.
        """
        self.__subsectionTSModules.grid_columnconfigure(0, weight=1)

        labelTSModules = Label(self.__subsectionTSModules, text=loader.lang["settings"]["modules"]["modules"], pady=5, width=int((self.__subsectionTSModules.winfo_width()-13)/7)+1)
        labelTSModules.grid(row=1)
        self.__outvarTSModule = StringVar()
        comboboxTSModule = ttk.Combobox(self.__subsectionTSModules, state="readonly", textvariable=self.__outvarTSModule, width=int((self.__subsectionTSModules.winfo_width()-13)/7)+1)
        comboboxTSModule.grid(row=2)
        comboboxTSModule['values'] = self.__hubTSModules.getAllModuleNames()

        self.__frameTSModules = Frame(self.__subsectionTSModules, width=self.__subsectionTSModules.winfo_width())
        self.__frameTSModules.grid(row=3)
        
        buttonUpdateData = Button(self.__subsectionTSModules, text=loader.lang["settings"]["modules"]["update"], command=self.__updateChart, pady=5, width=int((self.__subsectionTSModules.winfo_width()-13)/7)+1)
        buttonUpdateData.grid(row=4)

        comboboxTSModule.bind('<<ComboboxSelected>>', self.__subsectionTSModules_comboboxTSModule_action)   

    def __buildSubsectionStatisctics(self):
        """Builds subsection of output section that displays data of modules in tabular form.
        """
        self.__subsectionStatisctics.grid_columnconfigure(0, weight=1)

        labelCharts = Label(self.__subsectionStatisctics, text=loader.lang["output"]["statistics"]["modules"], pady=5, width=int((self.__subsectionStatisctics.winfo_width()-13)/7)+1)
        labelCharts.grid(row=1)
        self.__outvarOutputModules = StringVar()
        self.__comboboxOutputModules = ttk.Combobox(self.__subsectionStatisctics, state="readonly", textvariable=self.__outvarOutputModules, width=int((self.__subsectionStatisctics.winfo_width()-13)/7)+1)
        self.__comboboxOutputModules.grid(row=2)

        self.__treeviewStatistics = ttk.Treeview(self.__subsectionStatisctics)
        self.__treeviewStatistics.grid(row=3, sticky=NSEW)
        self.__treeviewStatistics.column("#0", width=self.__subsectionStatisctics.winfo_width(), stretch=YES)
        self.__treeviewStatistics.heading("#0",text="",anchor=CENTER)
       
        self.__comboboxOutputModules.bind('<<ComboboxSelected>>', self.__subsectionStatisctics_comboboxOutputModules_action)   

    def __buildSubsectionLogger(self):
        """Builds subsection of output section that logs user's actions.
        """
        self.__subsectionLogger.grid_columnconfigure(0, weight=1)

        #Height formula: 4 + 16n
        self.__outtextfieldLogger = Text(self.__subsectionLogger, width=self.__subsectionLogger.winfo_width(), height=int(((self.__subsectionLogger.winfo_height()-4)/16+1)))
        self.__outtextfieldLogger.grid(row=1, sticky=NSEW)

        logger.win = self.__outtextfieldLogger
        logger.log("Initiated")

    def __buildSubsectionExportData(self):
        """Builds subsection of output section that allows exporting logs, chart and statistics.
        """
        self.__subsectionExportData.grid_columnconfigure(0, weight=1)

        __buttonImportDataChart = Button(self.__subsectionExportData, text=loader.lang["output"]["exportdata"]["exportchart"], command=self.__subsectionExportData_buttonExportChart_action, pady=5, width=int((self.__subsectionExportData.winfo_width()-13)/7)+1)
        __buttonImportDataChart.grid(row=1)

        __buttonImportDataLogs = Button(self.__subsectionExportData, text=loader.lang["output"]["exportdata"]["exportlogs"], command=self.__subsectionExportData_buttonExportLogs_action, pady=5, width=int((self.__subsectionExportData.winfo_width()-13)/7)+1)
        __buttonImportDataLogs.grid(row=2)

        __buttonImportDataStats = Button(self.__subsectionExportData, text=loader.lang["output"]["exportdata"]["exportstats"], command=self.__subsectionExportData_buttonExportStats_action, pady=5, width=int((self.__subsectionExportData.winfo_width()-13)/7)+1)
        __buttonImportDataStats.grid(row=3)


    def __buildSectionChart(self):
        """Builds section with chart that displays current data.
        """
        self.__sectionChart.grid_columnconfigure(0, weight=1)
        self.__sectionChart.grid_rowconfigure(0, weight=1)
        
    def __buildSectionSettings(self):
        """Builds section with settings that set properties of data.
        """
        self.__sectionSettings.grid_columnconfigure(0, weight=1)
        self.__sectionSettings.grid_rowconfigure(0, weight=1)

        notebookSettings = ttk.Notebook(self.__sectionSettings)

        self.__subsectionLoadData = Frame(notebookSettings,width=self.__sectionSettings.winfo_width(),height=self.__sectionSettings.winfo_height())
        self.__subsectionDataSelection = Frame(notebookSettings,width=self.__sectionSettings.winfo_width(),height=self.__sectionSettings.winfo_height())
        self.__subsectionTSModules = Frame(notebookSettings,width=self.__sectionSettings.winfo_width(),height=self.__sectionSettings.winfo_height())

        notebookSettings.add(self.__subsectionLoadData, text=loader.lang["settings"]["loaddata"]["header"])
        notebookSettings.add(self.__subsectionDataSelection, text=loader.lang["settings"]["charts"]["header"])
        notebookSettings.add(self.__subsectionTSModules, text=loader.lang["settings"]["modules"]["header"])

        notebookSettings.pack(expand=1, fill='both')

        self.__subsectionLoadData.update()
        self.__subsectionDataSelection.update()
        self.__subsectionTSModules.update()
        notebookSettings.select(0)
        self.__buildSubsectionLoadData()

        self.__subsectionLoadData.update()
        self.__subsectionDataSelection.update()
        self.__subsectionTSModules.update()
        notebookSettings.select(1)
        self.__buildSubsectionDataSelection()

        self.__subsectionLoadData.update()
        self.__subsectionDataSelection.update()
        self.__subsectionTSModules.update()
        notebookSettings.select(2)
        self.__buildSubsectionTSModules()

        self.__subsectionLoadData.update()
        self.__subsectionDataSelection.update()
        self.__subsectionTSModules.update()
        notebookSettings.select(0)

    def __buildSectionOutput(self):
        """Builds section with output functions that display and export data.
        """
        self.__sectionOutput.grid_columnconfigure(0, weight=1)
        self.__sectionOutput.grid_rowconfigure(0, weight=1)

        notebookOutput = ttk.Notebook(self.__sectionOutput)

        self.__subsectionStatisctics = Frame(notebookOutput,width=self.__sectionOutput.winfo_width(),height=self.__sectionOutput.winfo_height())
        self.__subsectionLogger = Frame(notebookOutput,width=self.__sectionOutput.winfo_width(),height=self.__sectionOutput.winfo_height())
        self.__subsectionExportData = Frame(notebookOutput,width=self.__sectionOutput.winfo_width(),height=self.__sectionOutput.winfo_height())

        notebookOutput.add(self.__subsectionStatisctics, text=loader.lang["output"]["statistics"]["header"])
        notebookOutput.add(self.__subsectionLogger, text=loader.lang["output"]["logger"]["header"])
        notebookOutput.add(self.__subsectionExportData, text=loader.lang["output"]["exportdata"]["header"])

        notebookOutput.pack(expand=1, fill='both')

        self.__subsectionStatisctics.update()
        self.__subsectionLogger.update()
        self.__subsectionExportData.update()
        notebookOutput.select(0)
        self.__buildSubsectionStatisctics()

        self.__subsectionStatisctics.update()
        self.__subsectionLogger.update()
        self.__subsectionExportData.update()
        notebookOutput.select(1)
        self.__buildSubsectionLogger()

        self.__subsectionStatisctics.update()
        self.__subsectionLogger.update()
        self.__subsectionExportData.update()
        notebookOutput.select(2)
        self.__buildSubsectionExportData()

        self.__subsectionStatisctics.update()
        self.__subsectionLogger.update()
        self.__subsectionExportData.update()
        notebookOutput.select(0)

    def _buildSections(self):
        """Constructs all sections of an application.
        """
        self.__hubImporters.loadImporters()
        self.__hubTSModules.loadModules()

        self.__sectionChart = Frame(self.getRoot(),bg='white',width=loader.conf["width"]*0.75, height=loader.conf["height"]*0.5)
        self.__sectionSettings = Frame(self.getRoot(),bg='white',width=loader.conf["width"]*0.25, height=loader.conf["height"])
        self.__sectionOutput = Frame(self.getRoot(),bg='white',width=loader.conf["width"]*0.75, height=loader.conf["height"]*0.5)

        self.__sectionChart.grid(column=0,row=0,columnspan=3,rowspan=2,sticky=NSEW)
        self.__sectionSettings.grid(column=3,row=0,columnspan=1,rowspan=4,sticky=NSEW)
        self.__sectionOutput.grid(column=0,row=2,columnspan=3,rowspan=2,sticky=NSEW)

        self.__sectionChart.update()
        self.__sectionSettings.update()
        self.__sectionOutput.update()

        self.__buildSectionChart()
        self.__buildSectionSettings()
        self.__buildSectionOutput()

class GeneratorGui(Gui):
    __sectionChart: Frame = None
    """Section with chart that displays current generated data."""

    __sectionSettings: Frame = None
    """Section with settings that set properties of generated data."""
    __sectionsubChartGenerator: Frame = None
    """Subsection of settings section that configures parameters of generated chart."""
    __subsectionExportData: Frame = None
    """Subsection of settings section that allows exporting generated chart and statistics."""

    __genDf = DataFrame()
    """Data frame of generated signal."""

    __cpCount = 2
    """Number of change points in generated signal."""
    __samples = 100
    """Number of samples (data length) in generated signal."""
    __outvarMean = None
    """Mean of all data in generated signal."""
    __outvarSpread = None
    """Spread of mean of all data in generated signal."""
    __outvarCPSpread = None
    """Gaussian noise scale in areas between change points in generated signal."""
    __outvarSpreadCPSpread = None
    """Spread of gaussian noise scale in areas between change points in generated signal."""

    __signalGenerator: SignalGenerator = SignalGenerator()

    def __subsectionExportData_buttonUpdateData_action(self):
        """Method called when activating export button in
        subsection of settings section that allows exporting generated chart and statistics.
        Generates a new, randomized signal.
        """
        for widget in self.__sectionChart.winfo_children():
            widget.destroy()

        self.__signalGenerator.generateSignal(self.__samples, self.__cpCount, self.__outvarMean.get(), self.__outvarSpread.get(), self.__outvarCPSpread.get(), self.__outvarSpreadCPSpread.get())

        self.dfdata = {
            "X": [x for x in range(self.__samples)],
            "Y": self.__signalGenerator.getSignal()
        }

        self.__genDf = DataFrame(self.dfdata,columns=["X","Y"])
        figure = plt.Figure(dpi=100)
        ax = figure.add_subplot(111)

        figure = FigureCanvasTkAgg(figure, self.__sectionChart)
        figure.get_tk_widget().grid(row=0)

        self.__genDf = self.__genDf[["X", "Y"]].groupby("X").sum()
        self.__genDf.plot(kind='line', legend=FALSE, ax=ax, color='r',marker='o', fontsize=4, markersize=2)

        self.__signalGenerator.applyPatchesToChart(ax)
        ax.set_title(loader.lang["settings-gen"]["chartname"])
        self.__buttonExportData['state'] = "normal"

    def __subsectionExportData_buttonExport_action(self):
        """Method called when activating export button in
        subsection of settings section that allows exporting generated chart and statistics.
        Exports generated data to text format and csv spreadsheet.
        """
        
        if not self.__genDf.empty:
            (genCps, genMeans, genSpreads) = self.__signalGenerator.getGeneratedSignalProperties()
            f = open(loader.dirs["geninfo"], "w")
            f.write(loader.lang["settings-gen"]["results"]["cps"] + "\n")
            f.write(' '.join([str(e) for e in genCps]))
            f.write("\n\n")
            f.write(loader.lang["settings-gen"]["results"]["means"] + "\n")
            f.write(' '.join([str(e) for e in genMeans]))
            f.write("\n\n")
            f.write(loader.lang["settings-gen"]["results"]["spreads"] + "\n")
            f.write(' '.join([str(e) for e in genSpreads]))
            f.close()
            self.__genDf.to_csv(loader.dirs["gen"])
            messagebox.showinfo(loader.lang["messagebox"]["info"], loader.lang["settings-gen"]["results"]["exportinfo"] + "\n" + loader.dirs["geninfo"] + "\n" + loader.dirs["gen"])


    def __buildSubSectionChartGenerator(self):
        """Builds subsection of settings section that configures parameters of generated chart.
        """
        self.__sectionsubChartGenerator.grid_columnconfigure(0, weight=1)

        labelPoints = Label(self.__sectionsubChartGenerator, text=loader.lang["settings-gen"]["generator"]["cpcount"], pady=5, width=int((self.__sectionsubChartGenerator.winfo_width()-13)/7)+1)
        labelPoints.grid(row=1)
        sliderChangePointCount = Scale(self.__sectionsubChartGenerator, from_=0, to=10, tickinterval=2, orient=HORIZONTAL, length=int(self.__sectionsubChartGenerator.winfo_width()))
        sliderChangePointCount.set(self.__cpCount)
        sliderChangePointCount.grid(row=2)

        def updateChangePointCount(event):
            self.__cpCount = int(sliderChangePointCount.get())

        sliderChangePointCount.bind("<ButtonRelease-1>", updateChangePointCount)

        labelSamples = Label(self.__sectionsubChartGenerator, text=loader.lang["settings-gen"]["generator"]["samples"], pady=5, width=int((self.__sectionsubChartGenerator.winfo_width()-13)/7)+1)
        labelSamples.grid(row=3)
        self.sliderSamples = Scale(self.__sectionsubChartGenerator, from_=100, to=500, tickinterval=50, orient=HORIZONTAL, length=int(self.__sectionsubChartGenerator.winfo_width()))
        self.sliderSamples.set(self.__samples)
        self.sliderSamples.grid(row=4)

        def updateSamplesCount(event):
            self.__samples = int(self.sliderSamples.get())

        self.sliderSamples.bind("<ButtonRelease-1>", updateSamplesCount)

        labelMean = Label(self.__sectionsubChartGenerator, text=loader.lang["settings-gen"]["generator"]["mean"], pady=5, width=int((self.__sectionsubChartGenerator.winfo_width()-13)/7)+1)
        labelMean.grid(row=5)
        if not self.__outvarMean:
            self.__outvarMean = DoubleVar()
            self.__outvarMean.set(0.0)
        vcmd = (self.__sectionsubChartGenerator.register(entryvalidators.validate_float),'%P')
        entryMean = Entry(self.__sectionsubChartGenerator, textvariable=self.__outvarMean, validate='all', validatecommand=vcmd, width=int((self.__sectionsubChartGenerator.winfo_width()-13)/7)+1)
        entryMean.grid(row=6)

        labelSpread = Label(self.__sectionsubChartGenerator, text=loader.lang["settings-gen"]["generator"]["spread"], pady=5, width=int((self.__sectionsubChartGenerator.winfo_width()-13)/7)+1)
        labelSpread.grid(row=7)
        if not self.__outvarSpread:
            self.__outvarSpread = DoubleVar()
            self.__outvarSpread.set(2.5)
        vcmd = (self.__sectionsubChartGenerator.register(entryvalidators.validate_float_pos_zero),'%P')
        entrySpread = Entry(self.__sectionsubChartGenerator, textvariable=self.__outvarSpread, validate='all', validatecommand=vcmd, width=int((self.__sectionsubChartGenerator.winfo_width()-13)/7)+1)
        entrySpread.grid(row=8)

        labelCPSpread = Label(self.__sectionsubChartGenerator, text=loader.lang["settings-gen"]["generator"]["cpspread"], pady=5, width=int((self.__sectionsubChartGenerator.winfo_width()-13)/7)+1)
        labelCPSpread.grid(row=9)
        if not self.__outvarCPSpread:
            self.__outvarCPSpread = DoubleVar()
            self.__outvarCPSpread.set(0.75)
        vcmd = (self.__sectionsubChartGenerator.register(entryvalidators.validate_float_pos_zero),'%P')
        entryCPSpread = Entry(self.__sectionsubChartGenerator, textvariable=self.__outvarCPSpread, validate='all', validatecommand=vcmd, width=int((self.__sectionsubChartGenerator.winfo_width()-13)/7)+1)
        entryCPSpread.grid(row=10)

        labelSpreadCPSpread = Label(self.__sectionsubChartGenerator, text=loader.lang["settings-gen"]["generator"]["spreadcpspread"], pady=5, width=int((self.__sectionsubChartGenerator.winfo_width()-13)/7)+1)
        labelSpreadCPSpread.grid(row=11)
        if not self.__outvarSpreadCPSpread:
            self.__outvarSpreadCPSpread = DoubleVar()
            self.__outvarSpreadCPSpread.set(0.0)
        vcmd = (self.__sectionsubChartGenerator.register(entryvalidators.validate_float_pos_zero),'%P')
        entrySpreadCPSpread = Entry(self.__sectionsubChartGenerator, textvariable=self.__outvarSpreadCPSpread, validate='all', validatecommand=vcmd, width=int((self.__sectionsubChartGenerator.winfo_width()-13)/7)+1)
        entrySpreadCPSpread.grid(row=12)

    def __buildSubSectionExportData(self):
        """Builds subsection of settings section that allows exporting generated chart and statistics.
        """
        self.__subsectionExportData.grid_columnconfigure(0, weight=1)

        __buttonUpdateData = Button(self.__subsectionExportData, text=loader.lang["settings-gen"]["output"]["update"], pady=5, width=int((self.__subsectionExportData.winfo_width()-13)/7)+1)
        __buttonUpdateData.grid(row=1)

        self.__buttonExportData = Button(self.__subsectionExportData, state="disabled", text=loader.lang["settings-gen"]["output"]["export"], pady=5, width=int((self.__subsectionExportData.winfo_width()-13)/7)+1)
        self.__buttonExportData.grid(row=2)

        __buttonUpdateData.configure(command=self.__subsectionExportData_buttonUpdateData_action)
        self.__buttonExportData.configure(command=self.__subsectionExportData_buttonExport_action)
        

    def __buildSectionChart(self):
        """Builds section with chart that displays current generated data.
        """
        self.__sectionChart.grid_columnconfigure(0, weight=1)
        self.__sectionChart.grid_rowconfigure(0, weight=1)

    def __buildSectionSettings(self):
        """Builds section with settings that set properties of generated data.
        """
        self.__sectionSettings.grid_columnconfigure(0, weight=1)
        self.__sectionSettings.grid_rowconfigure(0, weight=1)

        notebookSettings = ttk.Notebook(self.__sectionSettings)

        self.__sectionsubChartGenerator = Frame(notebookSettings,width=self.__sectionSettings.winfo_width(),height=self.__sectionSettings.winfo_height())
        self.__subsectionExportData = Frame(notebookSettings,width=self.__sectionSettings.winfo_width(),height=self.__sectionSettings.winfo_height())

        notebookSettings.add(self.__sectionsubChartGenerator, text=loader.lang["settings-gen"]["generator"]["header"])
        notebookSettings.add(self.__subsectionExportData, text=loader.lang["settings-gen"]["output"]["header"])

        notebookSettings.pack(expand=1, fill='both')

        self.__sectionsubChartGenerator.update()
        self.__subsectionExportData.update()
        notebookSettings.select(0)
        self.__buildSubSectionChartGenerator()

        self.__sectionsubChartGenerator.update()
        self.__subsectionExportData.update()
        notebookSettings.select(1)
        self.__buildSubSectionExportData()

        self.__sectionsubChartGenerator.update()
        self.__subsectionExportData.update()
        notebookSettings.select(0)

    def _buildSections(self):
        """Constructs all sections of an application.
        """
        self.__sectionChart = Frame(self.getRoot(),bg='white',width=loader.conf["width"])
        self.__sectionSettings = Frame(self.getRoot(),width=loader.conf["width"])

        self.__sectionChart.grid(column=0,row=0,columnspan=1,rowspan=1,sticky=NSEW)
        self.__sectionSettings.grid(column=0,row=1,columnspan=1,rowspan=1,sticky=NSEW)

        self.__sectionChart.update()
        self.__sectionSettings.update()

        self.__buildSectionChart()
        self.__buildSectionSettings()