import json


class Util_IO:
    def __init__(self):
        self.defaults = self.read_defaults()

    def read_defaults(self):
        try:
            # Reads json file and creates if json file doesn't exist
            with open('defaults.json', ) as f:
                self.defaults = json.load(f)
        except Exception as e:
            # print ("Let's just ignore all exceptions, like this one: %s" % str(e))
            self.defaults = {
                "new_directory": "new-path",
                "start_directory": "C:\\Users\\silas\\Desktop\\pythonDirectoryScanner\\picturetest",
                "picture_extensions": ["jpg", "png", "tif", "tiff", "arw"]
            }
            with open('defaults.json', 'w', encoding='utf-8') as f:
                json.dump(self.defaults, f, ensure_ascii=False, indent=4)
        return self.defaults

    def new_path(self):
        return self.defaults['new_directory']

    def start_path(self):
        return self.defaults['start_directory']

    def picture_extensions(self):
        return self.defaults['picture_extensions']

    @staticmethod
    def read_known_locations():
        known_locations = {}
        try:
            # Reads json file and creates if json file doesn't exist
            with open('known_locations.json', ) as f:
                known_locations = json.load(f)
        except Exception as e:
            # print ("Let's just ignore all exceptions, like this one: %s" % str(e))
            with open('known_locations.json', 'w', encoding='utf-8') as f:
                json.dump(known_locations, f, ensure_ascii=False, indent=4)
        return known_locations

    @staticmethod
    def save_known_locations(known_locations):
        try:
            with open('known_locations.json', 'w', encoding='utf-8') as f:
                json.dump(known_locations, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print("Error writing known_locations.json", str(e))
