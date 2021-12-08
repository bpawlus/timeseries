from logging import disable
from tkinter import *
from tkinter import ttk, messagebox
import os
import re
import numpy
import pandas as pd
from pandas.core.frame import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import matplotlib.patches as patches

import loader

root = None
sectionchart = None

df = DataFrame()
cps = None
means = None
spreads = None

cpCount = 2
samples = 100
meanVar = None
spreadVar = None
cpspreadVar = None
spreadcpspreadVar = None

appconfig = None
directories = None
lang = None

def buildSubSectionChartGenerator(subsection: Frame):
    global cpCount, samples, meanVar, spreadVar, cpspreadVar, spreadcpspreadVar, df
    subsection.grid_columnconfigure(0, weight=1)

    labpoints = Label(subsection, text=lang["settings-gen"]["generator"]["cpcount"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
    labpoints.grid(row=1)
    changePointCount = Scale(subsection, from_=0, to=10, tickinterval=2, orient=HORIZONTAL, length=int(subsection.winfo_width()))
    changePointCount.set(cpCount)
    changePointCount.grid(row=2)

    def updateChangePointCount(event):
        global cpCount
        cpCount = int(changePointCount.get())

    changePointCount.bind("<ButtonRelease-1>", updateChangePointCount)

    def validate_floatentries(val):
        try:
            fval = float(val)
            if fval < 0:
                return False
        except:
            return False
        return True

    labsamples = Label(subsection, text=lang["settings-gen"]["generator"]["samples"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
    labsamples.grid(row=3)
    samplesCount = Scale(subsection, from_=100, to=500, tickinterval=50, orient=HORIZONTAL, length=int(subsection.winfo_width()))
    samplesCount.set(samples)
    samplesCount.grid(row=4)

    def updateSamplesCount(event):
        global samples
        samples = int(samplesCount.get())

    samplesCount.bind("<ButtonRelease-1>", updateSamplesCount)

    labmean = Label(subsection, text=lang["settings-gen"]["generator"]["mean"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
    labmean.grid(row=5)
    if not meanVar:
        meanVar = DoubleVar()
        meanVar.set(0.0)
    vcmd = (subsection.register(validate_floatentries),'%P')
    meanentry = Entry(subsection, textvariable=meanVar, validate='all', validatecommand=vcmd, width=int((subsection.winfo_width()-13)/7)+1)
    cpyval = meanVar.get()
    meanentry.delete(0,END)
    meanentry.insert(0,cpyval)
    meanentry.grid(row=6)

    labspread = Label(subsection, text=lang["settings-gen"]["generator"]["spread"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
    labspread.grid(row=7)
    if not spreadVar:
        spreadVar = DoubleVar()
        spreadVar.set(2.5)
    vcmd = (subsection.register(validate_floatentries),'%P')
    spreadentry = Entry(subsection, textvariable=spreadVar, validate='all', validatecommand=vcmd, width=int((subsection.winfo_width()-13)/7)+1)
    cpyval = spreadVar.get()
    spreadentry.delete(0,END)
    spreadentry.insert(0,cpyval)
    spreadentry.grid(row=8)

    labcpspread = Label(subsection, text=lang["settings-gen"]["generator"]["cpspread"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
    labcpspread.grid(row=9)
    if not cpspreadVar:
        cpspreadVar = DoubleVar()
        cpspreadVar.set(0.75)
    vcmd = (subsection.register(validate_floatentries),'%P')
    cpspreadentry = Entry(subsection, textvariable=cpspreadVar, validate='all', validatecommand=vcmd, width=int((subsection.winfo_width()-13)/7)+1)
    cpyval = cpspreadVar.get()
    cpspreadentry.delete(0,END)
    cpspreadentry.insert(0,cpyval)
    cpspreadentry.grid(row=10)

    labspreadcpspread = Label(subsection, text=lang["settings-gen"]["generator"]["spreadcpspread"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
    labspreadcpspread.grid(row=11)
    if not spreadcpspreadVar:
        spreadcpspreadVar = DoubleVar()
        spreadcpspreadVar.set(0.0)
    vcmd = (subsection.register(validate_floatentries),'%P')
    spreadcpspreadentry = Entry(subsection, textvariable=spreadcpspreadVar, validate='all', validatecommand=vcmd, width=int((subsection.winfo_width()-13)/7)+1)
    cpyval = spreadcpspreadVar.get()
    spreadcpspreadentry.delete(0,END)
    spreadcpspreadentry.insert(0,cpyval)
    spreadcpspreadentry.grid(row=12)

def buildSubSectionExportData(subsection: Frame):
    subsection.grid_columnconfigure(0, weight=1)

    btnupdate = Button(subsection, text=lang["settings-gen"]["output"]["update"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
    btnupdate.grid(row=1)

    btnexport = Button(subsection, state="disabled", text=lang["settings-gen"]["output"]["export"], pady=5, width=int((subsection.winfo_width()-13)/7)+1)
    btnexport.grid(row=2)

    def updateChart():
        global samples, meanVar, spreadVar, cpspreadVar, spreadcpspreadVar, sectionchart, df, cpCount, cps, means, spreads
        for widget in sectionchart.winfo_children():
            widget.destroy()

        step = samples/(cpCount+1)

        x = 0
        cps = [0]
        means = [random.uniform(meanVar.get()-spreadVar.get(), meanVar.get()+spreadVar.get())]
        spreads = [abs(random.uniform(cpspreadVar.get()-spreadcpspreadVar.get(), cpspreadVar.get()+spreadcpspreadVar.get()))]

        for i in range(cpCount):
            x += step
            cps.append(random.randint(int(x-step/2+1), int(x+step/2-1)))
            means.append(random.uniform(meanVar.get()-spreadVar.get(), meanVar.get()+spreadVar.get()))
            spreads.append(abs(random.uniform(cpspreadVar.get()-spreadcpspreadVar.get(), cpspreadVar.get()+spreadcpspreadVar.get())))
        

        dfdatay = []
        rects = []
        cps.append(samples)
        
        for i in range(len(cps)-1):
            cplen = cps[i+1]-cps[i]
            data = numpy.random.normal(means[i], spreads[i], cplen)
            dfdatay.extend(data)
            rects.append(patches.Rectangle((cps[i], means[i]-spreads[i]), cplen, 2*spreads[i], linewidth=2, edgecolor='#FFFF00', facecolor='none'))

        dfdata = {
            "X": [x for x in range(samples)],
            "Y": dfdatay
        }

        df = DataFrame(dfdata,columns=["X","Y"])
        figure = plt.Figure(dpi=100)
        ax = figure.add_subplot(111)

        figure = FigureCanvasTkAgg(figure, sectionchart)
        figure.get_tk_widget().grid(row=0)

        df = df[["X", "Y"]].groupby("X").sum()
        df.plot(kind='line', legend=FALSE, ax=ax, color='r',marker='o', fontsize=4, markersize=2)

        for patch in rects:
            ax.add_patch(patch)

        ax.set_title(lang["settings-gen"]["chartname"])
        btnexport['state'] = "normal"

    def export():
        global df, cps, means, spreads
        if not df.empty:
            f = open(directories["geninfo"], "w")
            f.write(lang["settings-gen"]["results"]["cps"] + "\n")
            f.write(' '.join([str(e) for e in cps]))
            f.write("\n\n")
            f.write(lang["settings-gen"]["results"]["means"] + "\n")
            f.write(' '.join([str(e) for e in means]))
            f.write("\n\n")
            f.write(lang["settings-gen"]["results"]["spreads"] + "\n")
            f.write(' '.join([str(e) for e in spreads]))
            f.close()
            df.to_csv(directories["gen"])
            messagebox.showinfo(lang["messagebox"]["info"], lang["settings-gen"]["results"]["exportinfo"] + "\n" + directories["geninfo"] + "\n" + directories["gen"])

    btnupdate.configure(command=updateChart)
    btnexport.configure(command=export)
    

def buildSectionChart(section: Frame):
    section.grid_columnconfigure(0, weight=1)
    section.grid_rowconfigure(0, weight=1)

def buildSectionSettings(section: Frame):
    section.grid_columnconfigure(0, weight=1)
    section.grid_rowconfigure(0, weight=1)

    notebook = ttk.Notebook(section)

    chartgeneratorsubsection = Frame(notebook,width=section.winfo_width(),height=section.winfo_height())
    exportdatasubsection = Frame(notebook,width=section.winfo_width(),height=section.winfo_height())

    notebook.add(chartgeneratorsubsection, text=lang["settings-gen"]["generator"]["header"])
    notebook.add(exportdatasubsection, text=lang["settings-gen"]["output"]["header"])

    notebook.pack(expand=1, fill='both')

    chartgeneratorsubsection.update()
    exportdatasubsection.update()
    notebook.select(0)
    buildSubSectionChartGenerator(chartgeneratorsubsection)

    chartgeneratorsubsection.update()
    exportdatasubsection.update()
    notebook.select(1)
    buildSubSectionExportData(exportdatasubsection)

    chartgeneratorsubsection.update()
    exportdatasubsection.update()
    notebook.select(0)

def buildRoot():
    global root, sectionchart
    root = Tk()
    root.title(lang["titlegen"])
    root.iconbitmap(directories["icon"])
    root.geometry(f'{appconfig["width"]}x{appconfig["height"]}')
    root.minsize(appconfig["width"], appconfig["height"])
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    sectionchart = Frame(root,bg='white',width=appconfig["width"])
    sectionsettings = Frame(root,width=appconfig["width"])

    sectionchart.grid(column=0,row=0,columnspan=1,rowspan=1,sticky=NSEW)
    sectionsettings.grid(column=0,row=1,columnspan=1,rowspan=1,sticky=NSEW)

    sectionchart.update()
    sectionsettings.update()

    buildSectionChart(sectionchart)
    buildSectionSettings(sectionsettings)

    root.mainloop()

appconfig, directories, lang = loader.loadConfig()
buildRoot()