import yaml

conf = None
dirs = None
lang = None

class Loader:
    @staticmethod
    def loadConfig():
        global conf, dirs, lang
        with open("config.yml", 'r') as stream:
            try:
                configloaded = yaml.safe_load(stream)
                conf = configloaded["app"]
                dirs = configloaded["directories"]
                languages = configloaded["languages"]

                with open(dirs["lang"] + "/" + languages[configloaded["language"]]["filename"], 'r') as streamlang:
                    try:
                        lang = yaml.safe_load(streamlang)
                    except yaml.YAMLError as exc:
                        print("YAML EXCEPTION:" + exc)
                        lang = None

            except yaml.YAMLError as exc:
                print("YAML EXCEPTION:" + exc)