from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor


class Parsimonious:
    def __init__(self, config):
        self.grammar = Grammar(config['grammar'])
        self.extractor = EntityVisitor(config['extractor'])

    def parse(self, text):
        tree = self.grammar.parse(text)
        self.extractor.clear()
        return self.extractor.visit(tree)


class EntityVisitor(NodeVisitor):
    current_entity = {}
    current_entity_id = None
    current_attribute = None
    current_attribute_key = None
    current_attribute_value = None

    def __init__(self, config):
        self.type = config.get('type', 'list')
        self.entity_from = config.get('entity_from', 'entity')
        self.id_from = config.get('id_from', 'id')
        self.attribute_from = config.get('attribute_from', 'attribute')
        self.key_from = config.get('key_from', 'label')
        self.value_from = config.get('value_from', 'value')
        self.clear()

    def clear(self):
        self.current_entity = {}
        self.current_entity_id = None
        self.current_attribute = None
        self.current_attribute_key = None
        self.current_attribute_value = None
        self.output = [] if self.type == 'list' else {}

    def generic_visit(self, node, children):
        if node.expr.name == self.entity_from:
            if self.type == 'list':
                self.output.append(self.current_entity.copy())
            else:
                # TODO : check id dup
                self.output[self.current_entity_id] = self.current_entity.copy()
            self.current_entity = {}
        elif node.expr.name == self.attribute_from:
            self.current_entity[self.current_attribute_key] = self.current_attribute_value
        elif node.expr.name == self.id_from:
            self.current_entity_id = node.text
        elif node.expr.name == self.key_from:
            self.current_attribute_key = node.text
        elif node.expr.name == self.value_from:
            self.current_attribute_value = node.text
        return self.output

