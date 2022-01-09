from tkinter import ttk
from pandas import DataFrame

class ImportMethod:
    """Base class responsible for loading time series data from different files.
    """

    extension: str = ""
    """Supported format of import method."""
    displayname: str = ""
    """Format of import method displayed in file dialog."""
    defaultTitle: str = ""
    """Default, preffered title of dataset, which should be applied after extracting data."""

    directory: str = ""
    """Directory where data is located."""
    
    def __init__(self, extension, displayname, defaultTitle):
        self.extension = extension
        self.displayname = displayname
        self.defaultTitle = defaultTitle

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