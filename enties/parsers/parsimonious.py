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

    def __init__(self, config):
        # Configuration values
        # Contains all nodes used in any key or value
        self.attr_nodes = set()
        # all parent nodes with the type of attribute (seq/groups/key_value)
        self.parent_nodes = {}
        # for a given parent, the list of keys (resp values)
        self.key_nodes_by_parent = {}
        self.val_nodes_by_parent = {}
        # seq :
        self.child_by_parent = {}
        self.seq_by_child = {}
        self.seq_nodes = set()
        # groups :
        self.groups_by_parent = {}

        # Dynamic state while the tree is visited
        self.output = []
        # the entity which is being built
        self.current_entity = {}
        # key-values : contain last values for keys or values in attr_nodes
        self.current_attrs = {}
        # seq : contain last values for child in seq
        self.current_seq = {}

        self.entity_from = config.get('entity_from', 'entity')
        attributes_from = config.get('attributes_from')
        for attr_from in attributes_from:
            parent = attr_from.get('parent', 'attribute')
            if 'seq' in attr_from.keys():
                self.parent_nodes[parent] = 'seq'
                child = attr_from['child']
                seq = attr_from['seq']
                self.child_by_parent[parent] = child
                self.seq_by_child[child] = seq
                self.seq_nodes.add(child)
            elif 'groups' in attr_from.keys():
                self.parent_nodes[parent] = 'groups'
                groups = attr_from['groups']
                self.groups_by_parent[parent] = groups
            else:
                self.parent_nodes[parent] = 'key_value'
                key = attr_from.get('keys', ['key'])
                val = attr_from.get('values', ['value'])
                if not isinstance(key, list):
                    raise ("'keys' should contain an array")
                if not isinstance(val, list):
                    raise ("'value' should contain an array")
                self.attr_nodes.update(key)
                self.attr_nodes.update(val)
                self.key_nodes_by_parent[parent] = key
                self.val_nodes_by_parent[parent] = val

    def generic_visit(self, node, children):
        node_name = node.expr.name
        if node_name in self.attr_nodes:
            self.current_attrs[node_name] = node.text
        elif node_name in self.seq_nodes:
            if node_name not in self.current_seq.keys():
                self.current_seq[node_name] = []
            self.current_seq[node_name].append(node.text)
        elif node_name in self.parent_nodes:
            parent_type = self.parent_nodes.get(node_name)
            if parent_type == 'seq':
                self.append_seq(node_name)
            elif parent_type == 'groups':
                self.append_groups(node_name, node)
            else:
                self.append_key_val(node_name)
        if node_name == self.entity_from:
            # Stores the currently extracted entity and reset the variable
            self.output.append(self.current_entity.copy())
            self.current_entity = {}
        return self.output

    def append_key_val(self, parent_node):
        keys = self.key_nodes_by_parent[parent_node]
        values = self.val_nodes_by_parent[parent_node]
        key_attrs = [self.current_attrs[k] for k in keys]
        val_attrs = [self.current_attrs[k] for k in values]
        self.current_entity[key_attrs[0]] = val_attrs[0]

    def append_seq(self, parent_node):
        child = self.child_by_parent[parent_node]
        seq_keys = self.seq_by_child[child]
        seq_values = self.current_seq[child]
        self.current_entity.update(dict(zip(seq_keys, seq_values)))
        self.current_seq[child] = []

    def append_groups(self, parent_node, node):
        groups_keys = self.groups_by_parent[parent_node]
        groups_values = node.match.groups()
        self.current_entity.update(dict(zip(groups_keys, groups_values)))
