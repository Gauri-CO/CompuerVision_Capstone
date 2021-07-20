import os
import yaml
from datetime import datetime
import pathlib

def load_config():
    dir_root = os.path.dirname(os.path.abspath(__file__))

    with open(dir_root + "/config.yaml", "r") as yamlfile:
        try:
            return yaml.load(yamlfile, Loader=yaml.FullLoader)
        except yaml.YAMLError as e:

            print(f"Failure: {e}")


class addTimestamp:

    def __init__(self, config):
        self.config = config

    def updatetimestamp(self):
        path1 = self.config[0]["source_folder"] + "/videos"
        path2 = self.config[0]["source_folder"] + "/targetvideos"
        for filename in os.listdir(path1):
            filext = filename.split(".")[-1]
            if filext == "mp4":
                name = filename.replace('.mp4', '')
                date = datetime.now().strftime("%Y%m%d")
                newfilename = name + "_" + date + ".mp4"
                print(f"{newfilename}")
                p1 = pathlib.PureWindowsPath(path1)
                p2 = pathlib.PureWindowsPath(path2)

                cmd = f"copy {p1}\{filename} {p2}\{newfilename}"
                print(f"Running ....{cmd}")
                os.system(cmd)
