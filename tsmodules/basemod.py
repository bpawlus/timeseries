from pandas.core.frame import DataFrame
from tkinter import *
from tkinter import ttk
import loader

class TSModule:
    """Base class for implementation of single time series module.
    """

    __name = "Unnamed Module"
    """Name of time series module."""
    __outvarActive = None
    """Should this module be considered in time series data analysis."""
    outputDf = DataFrame()
    """Data frame with processed time series module data, that was displayed on chart's axes, or that couldn't be displayed with line graph."""
    __dictColor = None
    """Dictionary of colors, that can be used to display module's data."""
    __outvarColor = None
    """Chosen color used to display module's data."""

    def getModuleName(self) -> str:
        """ Returns name of time series module.

        :returns: Name of time series module.
        """
        return self.__name

    def isModelActive(self) -> str:
        """ Returns true if this module be considered in time series data analysis.

        :returns: Should this module be considered in time series data analysis.
        """
        if self.__outvarActive and self.__outvarActive.get():
            return True
        else:
            return False

    def getDisplayColor(self) -> str:
        """ Returns color used to display module's data.

        :returns: Color used to display module's data.
        """
        if self.__dictColor and self.__outvarColor:
            return self.__dictColor[self.__outvarColor.get()]
        else:  
            return "red"
        

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

    def __init__(self, __name):
        self.__name = __name
        self.__dictColor =  {
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
        labelActive = Label(section, text=loader.lang["modules"]["isactive"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labelActive.grid(row=1)
        if not self.__outvarActive:
            self.__outvarActive = BooleanVar()
        checkModule = Checkbutton(section ,variable=self.__outvarActive, onvalue=1, offvalue=0)
        checkModule.grid(row=2)

        labelColor = Label(section, text=loader.lang["modules"]["color"], pady=5, width=int((section.winfo_width()-13)/7)+1)
        labelColor.grid(row=3)
        if not self.__outvarColor:
            self.__outvarColor = StringVar()
            self.__outvarColor.set(loader.lang["modules"]["colors"]["red"])
        comboboxColor = ttk.Combobox(section, state="readonly", textvariable=self.__outvarColor, width=int((section.winfo_width()-13)/7)+1)
        comboboxColor.grid(row=4)
        comboboxColor['values'] = list(self.__dictColor.keys())

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
