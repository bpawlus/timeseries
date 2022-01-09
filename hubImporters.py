from importers import baseimport
from importers import csvimport
from importers import xlsimport
import loader

class HubImporters:
    """Class with methods concerning data importers.
    """

    allMethods = ()
    """List containing all import method names."""
    allDrivers = ()
    """List containing all import methods."""

    def getImporterByFileextension(self, fileextension: str) -> baseimport.ImportMethod:
        """Returns import method based on operated file extension.

        :param fileextension: File extension of operated method.
        :returns: Requested method.
        """
        driverlist = [driv for ext, driv in self.allDrivers if ext == fileextension]
        if len(driverlist):
            return driverlist[0]
        else:
            return None

    def addMethod(self, method: baseimport.ImportMethod):
        """Adds file extension method to list.
        
        :param module: Import method to add.
        """
        self.allMethods = ((method.extension, method.displayname),) + self.allMethods
        self.allDrivers = ((method.extension, method),)+self.allDrivers

    def loadImporters(self) -> None:
        """Loads the list with all provided importers.
        """
        self.addMethod(csvimport.CsvImportMethod(".csv", "csv", loader.lang["importer-xls"]["defaultTitle"]))
        self.addMethod(xlsimport.XlsImportMethod(".xls", "xls", loader.lang["importer-csv"]["defaultTitle"]))