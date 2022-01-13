from tkinter import Frame
from pandas import DataFrame
import re

from chart import Chart

class HubCharts:
    """Class with methods concerning loaded data in form of charts.
    """

    __allCharts = []
    """List containing loaded data."""
    __id = 0
    """ID that will be assigned to next generated chart."""

    def getAllCharts(self):
        return self.__allCharts

    def getAllChartDisplayNames(self):
        """Returns display names for all loaded charts.

        :returns: Requested list.
        """
        return [f'{ch.title} ({ch.id})' for ch in self.__allCharts]

    def getChartById(self, chartId: int) -> Chart:
        """Returns chart of argument's id.
        Names should be unique in order to find a single instance

        :param chartId: ID of the chart.
        :returns: Requested list.
        """
        return next((ch for ch in self.__allCharts if ch.id == chartId), None)

    def getChartIdByDisplayName(self, name: str) -> int:
        """Returns id of chart with given display name.

        :param name: Display name, with format '{chart title} ({chart id})'.
        :returns: Requested list.
        """
        return int(re.findall("[0-9]+\\)$", name)[0][:-1])

    def addChart(self, df: DataFrame, title: str):
        """Adds chart to list.

        :param df: Data frame from which charty will be built.
        :param sectititleon: Title of chart.
        """
        self.__allCharts.append(Chart(df, title, self.__id))
        self.__id += 1

    def removeChart(self, chartId: int):
        """Removes chart from list.

        :param chartId: ID of chart to remove.
        """
        self.__allCharts.remove(next((ch for ch in self.__allCharts if ch.id == chartId),None))

    def displayChart(self, chartId: int, section: Frame, moduleDisplayer):
        """Displays chart in specified location.

        :param chartId: ID of chart to display.
        :param section: GUI component where chart should be displayed.
        :param moduleDisplayer: Method called in-line, that applies patches on chart from all active time series modules.
        """
        chart = self.getChartById(chartId)
        chart.displayChart(section, moduleDisplayer)
