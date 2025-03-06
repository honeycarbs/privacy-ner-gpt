import os

import yaml

class Config:
    __slots__ = [
        "path",
        "DEBUG"]

    def __init__(self, yaml_file_path: str):
        self.path = yaml_file_path
        self._read()

    def _read(self):
        if not os.path.exists(self.path):
            raise AttributeError(f"config path does not exist: {self.path}")
        
        with open(self.path) as config_file:
            content = config_file.read()
            config_yaml =  yaml.safe_load(content)

        for k,v in config_yaml.items():
            k = k.upper()
            if k in self.__slots__:
                setattr(self, k, v)