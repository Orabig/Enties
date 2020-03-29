import yaml


class Sources:
    def __init__(self):
        self.sources_by_id = dict()

    def load(self, path):
        with open(path, 'r') as stream:
            try:
                sources = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        for source in sources:
            self.sources_by_id[source["id"]] = source

    def get_by_id(self):
        return self.sources_by_id
