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
                normalized_path = file.replace('\\', '/')
                file_meta = Meta(normalized_path, handle.read())
                yield file_meta

class Meta:
  def __init__(self, uri, content):
      self.path = uri
      self.content = content