import argparse
import gui
from loader import Loader

parser = argparse.ArgumentParser(description='Starts GUI of time series project')
parser.add_argument('gui', nargs='+', help='gui to start')

args = parser.parse_args()
guiname = str(vars(args)['gui'][0])
if guiname == "analyzer":
    Loader.loadConfig()
    gui.AnalyzerGui().buildGui()
elif guiname == "generator":
    Loader.loadConfig()
    gui.GeneratorGui().buildGui()
else:
    print("Unknown GUI")