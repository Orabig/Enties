import yaml

from .entityDefinition import EntityDefinition
from .processors.relations import parse_relation


class Rules:
    def __init__(self, path):
        self.entities_rules = []
        with open(path, 'r') as stream:
            try:
                self.rules = yaml.safe_load(stream)
                rule_path = stream.name
            except yaml.YAMLError as exc:
                raise exc
        entity_definitions = self.rules["entities"]
        self.entities_rules = [EntityDefinition(rule, rule_path) for rule in entity_definitions]
        relations_definitions = self.rules.get("relations", [])
        self.relations = [parse_relation(rule) for rule in relations_definitions]

    def exec(self, sources):
        enties = self.parse_entities(sources)
        edges = self.build_edges(enties)
        return {"nodes": enties, "edges": edges}

    def build_edges(self, enties):
        edges = []
        for relation in self.relations:
            edges += relation.make_edges(enties)
        return edges

    def parse_entities(self, sources):
        entities = dict()
        for entity in self.entities_rules:
            entity_type = entity.type
            if entity_type in entities:
                entities[entity_type] += entity.parse(sources)
            else:
                entities[entity_type] = entity.parse(sources)
        return entities
