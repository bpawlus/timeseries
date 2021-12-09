import yaml

appconfig = None
directories = None
lang = None

def loadConfig():
    with open("config.yml", 'r') as stream:
        global appconfig, directories, lang
        try:
            config = yaml.safe_load(stream)
            appconfig = config["app"]
            directories = config["directories"]
            languages = config["languages"]
            language = None
 
            with open(directories["lang"] + "/" + languages[config["language"]]["filename"], 'r') as streamlang:
                try:
                    language = yaml.safe_load(streamlang)
                except yaml.YAMLError as exc:
                    print("YAML EXCEPTION:" + exc)
                    language = None
            appconfig, directories, lang = appconfig, directories, language

        except yaml.YAMLError as exc:
            print("YAML EXCEPTION:" + exc)