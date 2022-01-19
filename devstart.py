import loader
import gui
import rupturesefficiency

if loader.loadConfig("pl"):
    gui.AnalyzerGui().buildGui()
    #re = rupturesefficiency.RupturesEfficiency()
    #re.run()