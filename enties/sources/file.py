import glob


class File:
    def __init__(self, config):
        self.path = config["path"]

    def provide(self):
        for file in glob.glob(self.path):
            with open(file) as handle:
                file_meta = Meta()
                file_meta.path = file
                file_meta.content = handle.read()
                yield file_meta

class Meta:
    pass