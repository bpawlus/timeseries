from pandas.core.frame import DataFrame
from tkinter import *
from tkinter import ttk
import loader

class TSModule:
    """Base class for implementation of single time series module.
    """

    name = "Unnamed Module"
    """Name of time series module."""
    isactive = None
    """Should this module be considered in time series data analysis."""
    outputDataframe = DataFrame()
    """Data frame with processed time series module data, that was displayed on chart's axes, or that couldn't be displayed with line graph."""
    __colorDict = None
    """Dictionary of colors, that can be used to display module's data."""
    __colorcbvar = None
    """Chosen color used to display module's data."""

    def getDisplayColor(self) -> str:
        """ Returns color used to display module's data.

        :returns: Color used to display module's data.
        """
        return self.__colorDict[self.__colorcbvar.get()]

    def buildMenu(self, section: ttk.Frame):
        """Provides GUI elements for time series module items.

        :param section: GUI component where module items should be displayed.
        """
        for widget in section.winfo_children():
            widget.destroy()
        section.update()

        moduleFrameHeader = Frame(section, width=section.winfo_width())
        moduleFrameHeader.grid(row=1)

        moduleFrameConfig = Frame(section, width=section.winfo_width())
        moduleFrameConfig.grid(row=2)

        moduleFrameHeader.update()
        moduleFrameConfig.update()

        self.buildCheckbox(section=moduleFrameHeader)
        self.buildConfig(section=moduleFrameConfig)

    def __init__(self, name):
        self.name = name
        self.__colorDict =  {
            loader.lang["modules"]["colors"]["red"]: "red",
            loader.lang["modules"]["colors"]["orange"]: "orange",
            loader.lang["modules"]["colors"]["yellow"]: "yellow",
            loader.lang["modules"]["colors"]["green"]: "green",
            loader.lang["modules"]["colors"]["blue"]: "blue"
        }

    def buildCheckbox(self, section: ttk.Frame):
        """Provides GUI elements for time series module activation.

        :param section: GUI component where module activation should be displayed.
        """
        labactive = Label(section, text=loader.lang["modules"]["isactive"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labactive.grid(row=1)
        if not self.isactive:
            self.isactive = BooleanVar()
        moduleCheck = Checkbutton(section ,variable=self.isactive, onvalue=1, offvalue=0)
        moduleCheck.grid(row=2)

        labcolor = Label(section, text=loader.lang["modules"]["color"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labcolor.grid(row=3)
        if not self.__colorcbvar:
            self.__colorcbvar = StringVar()
            self.__colorcbvar.set(loader.lang["modules"]["colors"]["red"])
        colorcb = ttk.Combobox(section, state="readonly", textvariable=self.__colorcbvar, width=int((section.winfo_width()-13)/7)+1)
        colorcb.grid(row=4)
        colorcb['values'] = list(self.__colorDict.keys())

    def buildConfig(self, section: ttk.Frame):
        """Method meant to be overwritten.
        Provides GUI elements for time series module configuration.

        :param section: GUI component where module configuration should be displayed.
        """
        pass

    def displayModule(self, ax, plotdf: DataFrame):
        """Method meant to be overwritten.
        Processes analyzing module and displays results on chart's axes.

        :param ax: Reference to plot's axes.
        :param plotdf: Data frame with original signal.
        """
        pass
