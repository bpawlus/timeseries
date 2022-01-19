import argparse
import gui
import loader
import rupturesefficiency

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
elif guiname == "efficiency":
    if loader.loadConfig(lang):
        re = rupturesefficiency.RupturesEfficiency()
        re.run()
else:
    print("Unknown GUI")