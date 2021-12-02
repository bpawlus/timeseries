import yaml

def loadConfig():
    with open("config.yml", 'r') as stream:
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
            return appconfig, directories, language

        except yaml.YAMLError as exc:
            print("YAML EXCEPTION:" + exc)
            return None, None, None