from .parsers.parsimonious import Parsimonious


class Entity:
    def __init__(self, rules):
        self.source_id = rules['source']
        if 'parsimonious' in rules:
            self.parser_type = 'parsimonious'
            self.parser = Parsimonious(rules['parsimonious'])
        else:
            raise BaseException("Rules must use one of the following parsers : [parsimonious]")

    def parse(self, sources_by_id):
        entities = []
        source = sources_by_id[self.source_id]
        for meta in source.provide():
            try:
                content = meta.content
                result = dict()
                result['path'] = meta.path
                result['source'] = self.source_id
                result['entity'] = self.parser.parse(content)
                entities.append(result)
            except BaseException as ex:
                print("ERROR : Could not parse source [%s] '%s' with '%s' : '%s" % (self.source_id, meta.path, self.parser_type, ex))
                print("        Skipping...")
        return entities


class Foo:
    pass