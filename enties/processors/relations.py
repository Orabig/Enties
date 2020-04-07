from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

relation_grammar = Grammar(""
                           "lines = identity\n"
                           "identity = attribute '=' attribute\n"
                           "attribute = ~'(\\\\w+)\\\\.(\\\\w+)'\n"
                           "")


def parse_relation(rule):
    tree = relation_grammar.parse(rule)
    extractor = RuleVisitor()
    return extractor.visit(tree)


class RuleVisitor(NodeVisitor):
    def __init__(self):
        pass

    def visit_identity(self, node, children):
        a, _, b = children
        return Identity(a, b)

    def visit_attribute(self, node, _):
        type, name = node.match.groups()
        return Attribute(type, name)

    def generic_visit(self, node, children):
        return node.text


class Attribute:
    def __init__(self, t, n):
        self.type = t
        self.name = n


class Relation:
    def make_edges(self, entities):
        raise NotImplementedError("You must implement make_edges in %s" % type(self))


class Identity(Relation):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def make_edges(self, entities):
        edges = []
        attribute_a_type = self.a.type
        attribute_b_type = self.b.type
        attribute_a_name = self.a.name
        attribute_b_name = self.b.name
        try:
            all_a = entities[attribute_a_type]
        except KeyError as kerr:
            print("Error in relation XXX : '%s' type not found." % attribute_a_type)
        try:
            all_b = entities[attribute_b_type]
        except KeyError as kerr:
            print("Error in relation XXX : '%s' type not found." % attribute_b_type)
        edges = []
        # TODO : do better than a o(n²) algorithm
        index_a = 0
        for ent_a in all_a:
            index_b = 0
            for ent_b in all_b:
                try:
                    if ent_a[attribute_a_name] == ent_b[attribute_b_name]:
                        edge = "%s.%d-%s.%d" % (attribute_a_type, index_a, attribute_b_type, index_b)
                        edges.append(edge)
                except KeyError:
                    # Silently ignore if attribute are not found in any entity
                    pass
                index_b += 1
            index_a += 1
        return edges
