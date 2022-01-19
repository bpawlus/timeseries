import random
import numpy
import matplotlib.patches as patches

class SignalGenerator():
    """Class containing sample time series signal.
    """
    
    __genCps = None
    """Generated change point indexes."""
    __genMeans = None
    """Means in area between change points, before applying noise."""
    __genSpreads = None
    """Gaussian noise scale in area between change points."""
    __dataY = None
    """Generated signal."""

    def getGeneratedSignalProperties(self) -> tuple:
        """Returns properties of generated signal.
    
        :returns: Properties of generated signal.
        """

        return (self.__genCps, self.__genMeans, self.__genSpreads)

    def getSignal(self) -> list:
        """Returns generated signal.
        
        :returns: Generated signal.
        """
        return self.__dataY

    def generateSignal(self, samples, cpCount, mean, meanSpread, noiseScale, noiseScaleSpread):
        """Generates signal based on parameters. Data is stored inside the class.
        
        :param samples: Number of samples (data length) in generated signal.
        :param cpCount: Number of change points in generated signal
        :param mean: Mean of all data in generated signal
        :param meanSpread: Spread of mean of all data in generated signal
        :param noiseScale: Gaussian noise scale in areas between change points in generated signal.
        :param noiseScaleSpread: Spread of gaussian noise scale in areas between change points in generated signal.
        """
        step = samples/(cpCount+1)

        x = 0
        self.__genCps = [0]
        self.__genMeans = [random.uniform(mean-meanSpread, mean+meanSpread)]
        self.__genSpreads = [abs(random.uniform(noiseScale-noiseScaleSpread, noiseScale+noiseScaleSpread))]

        for i in range(cpCount):
            x += step
            self.__genCps.append(random.randint(int(x-step/2+1), int(x+step/2-1)))
            self.__genMeans.append(random.uniform(mean-meanSpread, mean+meanSpread))
            self.__genSpreads.append(abs(random.uniform(noiseScale-noiseScaleSpread, noiseScale+noiseScaleSpread)))
            
        self.__dataY.clear()
        self.__genCps.append(samples)

        for i in range(len(self.__genCps)-1):
            cplen = self.__genCps[i+1]-self.__genCps[i]
            data = numpy.random.normal(self.__genMeans[i], self.__genSpreads[i], cplen)
            self.__dataY.extend(data)
           
        self.__genCps[len(self.__genCps)-1] -= 1
        self.__genCps.pop(0)

    def applyPatchesToChart(self, ax):
        """Visualizes change points on charts' axes.

        :param ax: Chart's axes
        """
        self.__genCps.insert(0,0)
        for i in range(len(self.__genCps)-1):
            cplen = self.__genCps[i+1]-self.__genCps[i]
            ax.add_patch(patches.Rectangle((self.__genCps[i], self.__genMeans[i]-self.__genSpreads[i]), cplen, 2*self.__genSpreads[i], linewidth=2, edgecolor='#FFFF00', facecolor='none'))
        self.__genCps.pop(0)

    def __init__(self) -> None:
        self.__genCps = []
        self.__genMeans = []
        self.__genSpreads = []
        self.__dataY = []