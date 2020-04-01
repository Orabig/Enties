import os
import yaml
from .sources.file import File


class Sources:
    def __init__(self, path):
        self.sources_by_id = dict()
        base_path = os.path.dirname(path)
        with open(path, 'r') as stream:
            try:
                sources = yaml.safe_load(stream)
            except yaml.YAMLError as ex:
                print("ERROR : loading '%s' source : %s" %(path, ex))
        for source in sources:
            self.sources_by_id[source["id"]] = create_provider(source, base_path)


def create_provider(config, config_path):
    if 'file' in config:
        return File(config["file"], config_path)
    else:
        raise BaseException("Sources must use one of the following provider : [file]")