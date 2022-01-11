import yaml
import os

conf = None
"""List with application configurations."""
dirs = None
"""List with directories."""
lang = None
"""List with language labels."""

def loadConfig(language: str) -> bool:
    """Loads with configuration lists from config.yml file.

    :param language: Language to load.
    :returns: Should program be started.
    """
    global conf, dirs, lang
    with open("config.yml", 'r') as stream:
        try:
            configloaded = yaml.safe_load(stream)
            conf = configloaded["app"]
            dirs = configloaded["directories"]

            if not os.path.isfile(dirs["lang"] + "/" + language + ".yml"):
                print("Language: " + language + " doesn't exist!")
                return False

            with open(dirs["lang"] + "/" + language + ".yml", 'r') as streamlang:
                try:
                    lang = yaml.safe_load(streamlang)
                    return True
                except yaml.YAMLError as exc:
                    print("YAML EXCEPTION:" + exc)
                    lang = None
            return False

        except yaml.YAMLError as exc:
            print("YAML EXCEPTION:" + exc)
            return False