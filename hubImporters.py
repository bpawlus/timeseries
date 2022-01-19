from importers import baseimport
from importers import csvimport
from importers import xlsimport
import loader

class HubImporters:
    """Class with methods concerning data importers.
    """

    __allMethods = None
    """List containing all import method names."""
    __allDrivers = None
    """List containing all import methods."""

    def getAllMethods(self):
        return self.__allMethods

    def getAllDrivers(self):
        return self.__allDrivers

    def getImporterByFileextension(self, fileextension: str) -> baseimport.ImportMethod:
        """Returns import method based on operated file extension.

        :param fileextension: File extension of operated method.
        :returns: Requested method.
        """
        driverlist = [driv for ext, driv in self.__allDrivers if ext == fileextension]
        if len(driverlist):
            return driverlist[0]
        else:
            return None

    def addMethod(self, method: baseimport.ImportMethod):
        """Adds file extension method to list.
        
        :param module: Import method to add.
        """
        self.__allMethods = ((method.getExtension(), method.getFiledialogTitle()),) + self.__allMethods
        self.__allDrivers = ((method.getExtension(), method),)+self.__allDrivers

    def loadImporters(self) -> None:
        """Loads the list with all provided importers.
        """
        self.addMethod(csvimport.CsvImportMethod(".csv", "csv", loader.lang["importer-csv"]["defaultTitle"]))
        self.addMethod(xlsimport.XlsImportMethod(".xls", "xls", loader.lang["importer-xls"]["defaultTitle"]))

    def __init__(self) -> None:
        self.__allMethods = ()
        self.__allDrivers = ()