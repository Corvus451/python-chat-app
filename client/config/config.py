from configparser import ConfigParser

class Config:
    def __init__(self, file: str):
        self.__file: str = file
        self.__parser = ConfigParser()
        if not self.__parser.read(file):
            self.__create_default_config()


    def __create_default_config(self):
        self.__parser["DEFAULT"] = {
            "placeholder": "placeholder",
        }

        self.__parser["CLIENT"] = self.__parser["DEFAULT"]

        self.save()


    def cfg_set(self, key: str, value: str):
        self.__parser["CLIENT"][key] = value


    def cfg_get(self, key: str):
        return self.__parser["CLIENT"].get(key)


    def save(self):
        with open(self.__file, "w") as f:
            self.__parser.write(f)