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
        entity_rules = self.rules["entities"]
        self.entities = [Entity(rule) for rule in entity_rules]

    def exec(self, sources_by_id):
        entities = []
        for entity in self.entities:
            entities += entity.parse(sources_by_id)
        return entities
