from tkinter import ttk
from pandas import DataFrame

class ImportMethod:
    """Base class responsible for loading time series data from different files.
    """

    __extension: str = ""
    """Supported format of import method."""
    __filedialogTitle: str = ""
    """Format of import method displayed in file dialog."""
    __defaultTitle: str = ""
    """Default, preffered title of dataset, which should be applied after extracting data."""
    __directory: str = ""
    """Directory where data is located."""
    
    def getFiledialogTitle(self) -> str:
        """Returns format of import method displayed in file dialog.
        
        :returns: Format of import method displayed in file dialog.
        """
        return self.__filedialogTitle

    def getExtension(self) -> str:
        """Returns supported format of import method.
        
        :returns: Format of import method displayed in file dialog.
        """
        return self.__extension

    def getDefaultTitle(self) -> str:
        """Returns default, preffered title of dataset, which should be applied after extracting data.
        
        :returns: Default, preffered title of dataset, which should be applied after extracting data.
        """
        return self.__defaultTitle

    def getDirectory(self) -> str:
        """Returns directory where data is located.
        
        :returns: Directory where data is located.
        """
        return self.__directory

    def setDirectory(self, directory):
        """Sets new directory where data should be located.
        
        :param directory: New directory where data should be located.
        """
        self.__directory = directory

    def __init__(self, extension, filedialogTitle, defaultTitle):
        self.__extension = extension
        self.__filedialogTitle = filedialogTitle
        self.__defaultTitle = defaultTitle

    def importSettingsGui(self, section: ttk.Frame):
        """Method meant to be overwritten.
        Provides GUI elements for selection of specific signal from provided data.

        :param section: GUI component where chart should be displayed.
        """
        pass

    def extractData(self) -> DataFrame:
        """Method meant to be overwritten.
        Extracts signal from provided data.
        
        :returns: Data frame of single, selected time series.
        """
        return DataFrame()