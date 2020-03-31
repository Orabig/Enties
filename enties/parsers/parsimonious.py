from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor


class Parsimonious:
    def __init__(self, config):
        self.grammar = Grammar(config['grammar'])
        self.extractor = EntityVisitor(config['extractor'])

    def parse(self, text):
        tree = self.grammar.parse(text)
        return self.extractor.visit(tree)


class EntityVisitor(NodeVisitor):
    output = []
    current_entity = {}
    current_entity_id = None
    current_attribute = None
    current_attribute_key = None
    current_attribute_value = None

    def __init__(self, config):
        self.entity_from = config.get('entity_from', 'entity')
        self.id_from = config.get('id_from', 'id')
        self.attribute_from = config.get('attribute_from', 'attribute')
        self.key_from = config.get('key_from', 'label')
        self.value_from = config.get('value_from', 'value')

    def generic_visit(self, node, children):
        if node.expr.name == self.entity_from:
            self.output.append(self.current_entity.copy())
            self.current_entity = {}
        elif node.expr.name == self.attribute_from:
            self.current_entity[self.current_attribute_key] = self.current_attribute_value
        elif node.expr.name == self.key_from:
            self.current_attribute_key = node.text
        elif node.expr.name == self.value_from:
            self.current_attribute_value = node.text
        return self.output

