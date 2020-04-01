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
    # Configuration values
    # Contains all nodes used in any key or value
    attr_nodes = set()
    # all parent nodes with the type of attribute (seq/groups/key_value)
    parent_nodes = {}
    # for a given parent, the list of keys (resp values)
    key_nodes_by_parent = {}
    val_nodes_by_parent = {}

    # Dynamic state while the tree is visited
    output = []
    # contain last values for keys or values in attr_nodes
    current_attrs = {}
    # the entity which is being built
    current_entity = {}

    def __init__(self, config):
        self.entity_from = config.get('entity_from', 'entity')
        self.attributes_from = config.get('attributes_from')
        for attr_from in self.attributes_from:
            parent = attr_from.get('parent', 'attribute')
            if 'seq' in attr_from.keys():
                raise ("seq pas connu")
            elif 'groups' in attr_from.keys():
                raise ("groups pas connu")
            else:
                key = attr_from.get('keys', ['key'])
                val = attr_from.get('values', ['value'])
                if not isinstance(key, list):
                    raise ("'keys' should contain an array")
                if not isinstance(val, list):
                    raise ("'value' should contain an array")
                self.attr_nodes.update(key)
                self.attr_nodes.update(val)
                self.parent_nodes[parent] = 'key_value'
                self.key_nodes_by_parent[parent] = key
                self.val_nodes_by_parent[parent] = val

    def generic_visit(self, node, children):
        node_name = node.expr.name
        if node_name == self.entity_from:
            # Stores the currently extracted entity and reset the variable
            self.output.append(self.current_entity.copy())
            self.current_entity = {}
        elif node_name in self.attr_nodes:
            self.current_attrs[node_name] = node.text
        elif node_name in self.parent_nodes.keys():
            parent_type = self.parent_nodes.get(node_name)
            if parent_type == 'seq':
                raise ("seq pas connu in visit")
            elif parent_type == 'groups':
                raise ("groups pas connu in visit")
            else:
                self.append_key_val(node_name)
        return self.output

    def append_key_val(self, parent_node):
        keys = self.key_nodes_by_parent[parent_node]
        values = self.val_nodes_by_parent[parent_node]
        key_attrs = [self.current_attrs[k] for k in keys]
        val_attrs = [self.current_attrs[k] for k in values]
        self.current_entity[key_attrs[0]] = val_attrs[0]


class EntityVisitorArchive(NodeVisitor):
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
