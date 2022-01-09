import argparse
import gui
import loader

parser = argparse.ArgumentParser(description='Starts GUI of time series project')
parser.add_argument('gui', nargs='+', help='gui to start')
parser.add_argument('lang', nargs='+', help='application language')

args = parser.parse_args()
guiname = str(vars(args)['gui'][0])
lang = str(vars(args)['lang'][0])

if guiname == "analyzer":
    if loader.loadConfig(lang):
        gui.AnalyzerGui().buildGui()
elif guiname == "generator":
    if loader.loadConfig(lang):
        gui.GeneratorGui().buildGui()
else:
    print("Unknown GUI")