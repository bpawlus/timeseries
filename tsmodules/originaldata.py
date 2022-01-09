from pandas.core.frame import DataFrame
from tsmodules import basemod

class OriginalDataDisplayModule(basemod.TSModule):
    """Class implementing original data display time series module.
    """

    def displayModule(self, ax, plotdf: DataFrame):
        """Processes analyzing module and displays results on chart's axes.

        :param ax: Reference to plot's axes.
        :param plotdf: Data frame with original signal.
        """
        origdf = plotdf[[col for col in plotdf.columns]].groupby(plotdf.columns[0]).sum()
        origdf.plot(kind='line', legend=True, ax=ax, color=self.getDisplayColor(),marker='o', fontsize=4, markersize=2)
        self.outputDataframe = plotdf
