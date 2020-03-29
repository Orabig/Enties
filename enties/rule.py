import yaml

from .entity import Entity

class Rules:
    def __init__(self):
        self.entities = []

    def load(self, path, sources_by_id):
        with open(path, 'r') as stream:
            try:
                rules = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        entity_rules = rules["entities"]
        self.entities = [Entity(sources_by_id, rule) for rule in entity_rules]
