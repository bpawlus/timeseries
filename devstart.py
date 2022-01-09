import loader
import gui

if loader.loadConfig("pl"):
    gui.AnalyzerGui().buildGui()

