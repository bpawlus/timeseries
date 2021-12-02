from tkinter import *
from tkinter import ttk, filedialog, messagebox
import os
import re

import importer
import charts
import logger
import modules
import loader

root = None

textoutput = None
chartscb = None

def updateChartsCb():
    chartscb['values'] = [f'{ch.title} ({ch.id})' for ch in charts.allcharts]

chartid = -1
sectionchart = None
outputModulescb = None
statisticstab = None

def updateChart():
    for widget in sectionchart.winfo_children():
        widget.destroy()

    if(chartid != -1):
        chart = next((ch for ch in charts.allcharts if ch.id == chartid), None)
        chart.displayChart(sectionchart)
        outputModulescb.set('')
        for i in statisticstab.get_children():
            statisticstab.delete(i)
        outputModulescb['values'] = [mod.name for mod in modules.allmodules if mod.isactive and mod.isactive.get() and not mod.getOutputDataframe().empty]
        statisticstab['columns'] = []

def deleteChart():
    global chartid
    charts.allcharts.remove(next((ch for ch in charts.allcharts if ch.id == chartid),None))
    chartid = -1
    outputModulescb.set('')
    for i in statisticstab.get_children():
        statisticstab.delete(i)
    outputModulescb['values'] = []
    statisticstab['columns'] = []

    for widget in sectionchart.winfo_children():
        widget.destroy()

importdriver = None

appconfig = None
directories = None
lang = None


def buildSubSectionLoadData(subsection: Frame):
    subsection.grid_columnconfigure(0, weight=1)

    #Width formula: 13, 20, 27, 34... 13 + 7n
    importsettings = Frame(subsection, width=subsection.winfo_width())
    importsettings.grid(row=2)
    
    def callbackexport():
        global importdriver, lang, chartscb
        df = importdriver.extractData()
        if(not df.empty):
            charts.Chart(df, title=importdriver.defaultTitle)
            updateChartsCb()
        else:
            pass

    btnexport = Button(subsection, state="disabled", text=lang["settings"]["loaddata"]["select"], command=callbackexport, pady=5, width=int((subsection.winfo_width()-13)/7)+1)
    btnexport.grid(row=3)

    def callbackimport():
        global importdriver
        directory = filedialog.askopenfilename(initialdir="", title=lang["settings"]["loaddata"]["import"], filetypes=(importer.allmethods))
        filename, fileextension = os.path.splitext(directory)
        for widget in importsettings.winfo_children():
            widget.destroy()

        driverlist = [driv for ext, driv in importer.alldrivers if ext == fileextension ]
        if len(driverlist):
            importdriver = driverlist[0]
            importdriver.directory = directory
            importdriver.importSettingsGui(importsettings)
            btnexport['state'] = "normal"

    btnimport = Button(subsection, text=lang["settings"]["loaddata"]["import"], command=callbackimport, pady=5, width=int((subsection.winfo_width()-13)/7)+1)
    btnimport.grid(row=1)

def buildSubSectionCharts(subsection: Frame):
    global chartscb

    subsection.grid_columnconfigure(0, weight=1)
    
    labcharts = Label(subsection, text=lang["settings"]["charts"]["select"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
    labcharts.grid(row=1)
    chartlist = StringVar()
    chartscb = ttk.Combobox(subsection, state="readonly", textvariable=chartlist, width=int((subsection.winfo_width()-13)/7)+1)
    chartscb.grid(row=2)

    labcharts = Label(subsection, text=lang["settings"]["charts"]["titlechanger"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
    labcharts.grid(row=3)
    titleentry = StringVar()
    textoutput = Entry(subsection, textvariable=titleentry, state="disabled", width=int((subsection.winfo_width()-13)/7)+1)
    textoutput.grid(row=4)

    def updateChartSequence():
        global chartid, sectionchart
        chart = next((ch for ch in charts.allcharts if ch.id == chartid), None)
        chart.title = titleentry.get()
        updateChartsCb()
        chartscb.set(f'{chart.title} ({chart.id})')
        updateChart()

    btnupdate = Button(subsection, state="disabled", text=lang["settings"]["charts"]["update"], command=updateChartSequence, pady=5, width=int((subsection.winfo_width()-13)/7)+1)
    btnupdate.grid(row=5)

    def deleteChartSequence():
        global sectionchart
        
        deleteChart()
        updateChartsCb()
        chartscb.set("")             

        textoutput['state'] = "disabled"
        titleentry.set("")
        btndelete['state'] = "disabled"
        btnupdate['state'] = "disabled"

    btndelete = Button(subsection, state="disabled", text=lang["settings"]["charts"]["delete"], command=deleteChartSequence, pady=5, width=int((subsection.winfo_width()-13)/7)+1)
    btndelete.grid(row=6)

    def selectChart(event):
        global chartid
        name = chartlist.get()
        chartid = int(re.findall("[0-9]+\\)$", name)[0][:-1])
        
        textoutput['state'] = "normal"
        chart = next((ch for ch in charts.allcharts if ch.id == chartid), None)
        titleentry.set(chart.title)
        
        btndelete['state'] = "normal"
        btnupdate['state'] = "normal"

    chartscb.bind('<<ComboboxSelected>>', selectChart)   

def buildSubSectionModules(subsection: Frame):
    subsection.grid_columnconfigure(0, weight=1)

    labmodules = Label(subsection, text=lang["settings"]["modules"]["modules"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
    labmodules.grid(row=1)
    modulesentry = StringVar()
    modulesentrycb = ttk.Combobox(subsection, state="readonly", textvariable=modulesentry, width=int((subsection.winfo_width()-13)/7)+1)
    modulesentrycb.grid(row=2)
    modulesentrycb['values'] = [mod.name for mod in modules.allmodules]

    modulesFrame = Frame(subsection, width=subsection.winfo_width())
    modulesFrame.grid(row=3)
    
    btnexport = Button(subsection, text=lang["settings"]["modules"]["update"], command=updateChart, pady=5, width=int((subsection.winfo_width()-13)/7)+1)
    btnexport.grid(row=4)

    def selectModule(event):
        mod = next(mod for mod in modules.allmodules if modulesentry.get() == mod.name)
        mod.buildMenu(modulesFrame)

    modulesentrycb.bind('<<ComboboxSelected>>', selectModule)   

def buildSubSectionStatisctics(subsection: Frame):
    global outputModulescb, statisticstab
    subsection.grid_columnconfigure(0, weight=1)

    labcharts = Label(subsection, text=lang["output"]["statistics"]["modules"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
    labcharts.grid(row=1)
    outputModules = StringVar()
    outputModulescb = ttk.Combobox(subsection, state="readonly", textvariable=outputModules, width=int((subsection.winfo_width()-13)/7)+1)
    outputModulescb.grid(row=2)

    statisticstab = ttk.Treeview(subsection)
    statisticstab.grid(row=3, sticky=NSEW)
    statisticstab.column("#0", width=subsection.winfo_width(), stretch=YES)
    statisticstab.heading("#0",text="",anchor=CENTER)

    def selectModuleOutput(event):
        for i in statisticstab.get_children():
            statisticstab.delete(i)
        statisticstab.column("#0", width=0, stretch=NO)
        statisticstab.heading("#0",text="",anchor=CENTER)

        df = next((mod.getOutputDataframe() for mod in modules.allmodules if mod.name == outputModules.get()), None)
        columns = df.columns.values.tolist()
        statisticstab['columns'] = columns

        for column in columns:
            statisticstab.column(column, anchor=CENTER, width=int(subsection.winfo_width()/len(columns)))
            statisticstab.heading(column,text=column,anchor=CENTER)

        data = df.values.tolist()
        for v in data:
            statisticstab.insert('', END, values=v)
        
        

    outputModulescb.bind('<<ComboboxSelected>>', selectModuleOutput)   

def buildSubSectionLogger(subsection: Frame):
    global textoutput
    subsection.grid_columnconfigure(0, weight=1)

    #Height formula: 4 + 16n
    textoutput = Text(subsection, width=subsection.winfo_width(), height=int(((subsection.winfo_height()-4)/16+1)))
    textoutput.grid(row=1, sticky=NSEW)

    logger.win = textoutput
    logger.log("Initiated")

def buildSubSectionExportData(subsection: Frame):
    subsection.grid_columnconfigure(0, weight=1)

    def exportChart():
        if(chartid != -1):
            chart = next((ch for ch in charts.allcharts if ch.id == chartid), None)
            chart.exportChart(directories["exportchart"])
            messagebox.showinfo(lang["messagebox"]["info"], f'{lang["output"]["exportdata"]["successexportchart"]}{directories["exportchart"]}')
        else:
            messagebox.showerror(lang["messagebox"]["error"], lang["output"]["exportdata"]["failedexport"])

    def exportLogs():
        global textoutput
        f = open(directories["exportlogname"], "w")
        f.write(textoutput.get("1.0",END))
        f.close()
        messagebox.showinfo(lang["messagebox"]["info"], f'{lang["output"]["exportdata"]["successexportlogs"]}{directories["exportlogname"]}')

    def exportStats():
        if(chartid != -1):
            f = open(directories["exportstats"], "w")
            mods = [mod for mod in modules.allmodules if mod.isactive and mod.isactive.get() and not mod.getOutputDataframe().empty]
            for mod in mods:
                f.write(mod.name)
                f.write("\n")
                f.write(mod.getOutputDataframe().to_string())
                f.write("\n\n")
            f.close()
            messagebox.showinfo(lang["messagebox"]["info"], f'{lang["output"]["exportdata"]["successexportstats"]}{directories["exportstats"]}')
        else:
            messagebox.showerror(lang["messagebox"]["error"], lang["output"]["exportdata"]["failedexport"])


    btnexportchart = Button(subsection, text=lang["output"]["exportdata"]["exportchart"], command=exportChart, pady=5, width=int((subsection.winfo_width()-13)/7)+1)
    btnexportchart.grid(row=1)

    btnexportlogs = Button(subsection, text=lang["output"]["exportdata"]["exportlogs"], command=exportLogs, pady=5, width=int((subsection.winfo_width()-13)/7)+1)
    btnexportlogs.grid(row=2)

    btnexportstats = Button(subsection, text=lang["output"]["exportdata"]["exportstats"], command=exportStats, pady=5, width=int((subsection.winfo_width()-13)/7)+1)
    btnexportstats.grid(row=3)



def buildSectionChart(section: Frame):
    section.grid_columnconfigure(0, weight=1)
    section.grid_rowconfigure(0, weight=1)
    
def buildSectionSettings(section: Frame):
    section.grid_columnconfigure(0, weight=1)
    section.grid_rowconfigure(0, weight=1)

    settingsnotebook = ttk.Notebook(section)

    loaddatasubsection = Frame(settingsnotebook,width=section.winfo_width(),height=section.winfo_height())
    chartssubsection = Frame(settingsnotebook,width=section.winfo_width(),height=section.winfo_height())
    modulessubsection = Frame(settingsnotebook,width=section.winfo_width(),height=section.winfo_height())

    settingsnotebook.add(loaddatasubsection, text=lang["settings"]["loaddata"]["header"])
    settingsnotebook.add(chartssubsection, text=lang["settings"]["charts"]["header"])
    settingsnotebook.add(modulessubsection, text=lang["settings"]["modules"]["header"])

    settingsnotebook.pack(expand=1, fill='both')

    loaddatasubsection.update()
    chartssubsection.update()
    modulessubsection.update()
    settingsnotebook.select(0)
    buildSubSectionLoadData(loaddatasubsection)

    loaddatasubsection.update()
    chartssubsection.update()
    modulessubsection.update()
    settingsnotebook.select(1)
    buildSubSectionCharts(chartssubsection)

    loaddatasubsection.update()
    chartssubsection.update()
    modulessubsection.update()
    settingsnotebook.select(2)
    buildSubSectionModules(modulessubsection)

    loaddatasubsection.update()
    chartssubsection.update()
    modulessubsection.update()
    settingsnotebook.select(0)

def buildSectionOutput(section: Frame):
    section.grid_columnconfigure(0, weight=1)
    section.grid_rowconfigure(0, weight=1)

    outputnotebook = ttk.Notebook(section)

    statisticssubsection = Frame(outputnotebook,width=section.winfo_width(),height=section.winfo_height())
    loggersubsection = Frame(outputnotebook,width=section.winfo_width(),height=section.winfo_height())
    exportdatasubsection = Frame(outputnotebook,width=section.winfo_width(),height=section.winfo_height())

    outputnotebook.add(statisticssubsection, text=lang["output"]["statistics"]["header"])
    outputnotebook.add(loggersubsection, text=lang["output"]["logger"]["header"])
    outputnotebook.add(exportdatasubsection, text=lang["output"]["exportdata"]["header"])

    outputnotebook.pack(expand=1, fill='both')

    statisticssubsection.update()
    loggersubsection.update()
    exportdatasubsection.update()
    outputnotebook.select(0)
    buildSubSectionStatisctics(statisticssubsection)

    statisticssubsection.update()
    loggersubsection.update()
    exportdatasubsection.update()
    outputnotebook.select(1)
    buildSubSectionLogger(loggersubsection)

    statisticssubsection.update()
    loggersubsection.update()
    exportdatasubsection.update()
    outputnotebook.select(2)
    buildSubSectionExportData(exportdatasubsection)

    statisticssubsection.update()
    loggersubsection.update()
    exportdatasubsection.update()
    outputnotebook.select(0)



def buildRoot():
    global root, sectionchart
    root = Tk()
    root.title(lang["title"])
    root.iconbitmap(directories["icon"])
    root.geometry(f'{appconfig["width"]}x{appconfig["height"]}')
    root.minsize(appconfig["width"], appconfig["height"])
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    sectionchart = Frame(root,bg='white',width=appconfig["width"]*0.75, height=appconfig["height"]*0.5)
    sectionsettings = Frame(root,bg='white',width=appconfig["width"]*0.25, height=appconfig["height"])
    sectionoutput = Frame(root,bg='white',width=appconfig["width"]*0.75, height=appconfig["height"]*0.5)

    sectionchart.grid(column=0,row=0,columnspan=3,rowspan=2,sticky=NSEW)
    sectionsettings.grid(column=3,row=0,columnspan=1,rowspan=4,sticky=NSEW)
    sectionoutput.grid(column=0,row=2,columnspan=3,rowspan=2,sticky=NSEW)

    sectionchart.update()
    sectionsettings.update()
    sectionoutput.update()

    buildSectionChart(sectionchart)
    buildSectionSettings(sectionsettings)
    buildSectionOutput(sectionoutput)

    root.mainloop()
    
appconfig, directories, lang = loader.loadConfig()
charts.postConfigInit(appconfig, directories, lang)
importer.postConfigInit(appconfig, directories, lang)
logger.postConfigInit(appconfig, directories, lang)
modules.postConfigInit(appconfig, directories, lang)
buildRoot()