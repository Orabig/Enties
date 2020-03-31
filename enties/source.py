import yaml
from .sources.file import File


class Sources:
    def __init__(self, path):
        self.sources_by_id = dict()
        with open(path, 'r') as stream:
            try:
                sources = yaml.safe_load(stream)
            except yaml.YAMLError as ex:
                print("ERROR : loading '%s' source : %s" %(path, ex))
        for source in sources:
            self.sources_by_id[source["id"]] = create_provider(source)


def create_provider(config):
    if 'file' in config:
        return File(config["file"])
    else:
        raise BaseException("Sources must use one of the following provider : [file]")