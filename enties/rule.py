import yaml

from .entity import Entity


class Rules:
    def __init__(self, path):
        self.entities = []
        with open(path, 'r') as stream:
            try:
                self.rules = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise exc
        self.entity_rules = self.rules["entities"]

    def exec(self, sources_by_id):
        self.entities = [Entity(sources_by_id, rule) for rule in self.entity_rules]
        for entity in self.entities:
            entity.parse()
