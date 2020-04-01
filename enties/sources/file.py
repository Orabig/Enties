import os
import glob


class File:
    def __init__(self, config, config_path):
        self.path = config["path"]
        self.base = config_path

    def provide(self):
        path = os.path.normpath(os.path.join(self.base, self.path))
        for file in glob.glob(path):
            with open(file) as handle:
                file_meta = Meta()
                normalized_path = file.replace('\\', '/')
                file_meta.path = normalized_path
                file_meta.content = handle.read()
                yield file_meta

class Meta:
    pass