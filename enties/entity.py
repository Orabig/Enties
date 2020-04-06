from parsimonious.exceptions import ParseError
from .parsers.parsimonious import Parsimonious
from .processors.commentStripper import strip_comments


class Entity:
    def __init__(self, rules):
        self.source_id = rules['source']
        self.strip_comments = rules['strip_comments'] if 'strip_comments' in rules else None
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
                if self.strip_comments is not None:
                    content = strip_comments(content, self.strip_comments)
                # TODO : this should be made a real list (with common meta put inside it)
                result['entities'] = self.parser.parse(content)
                entities.append(result)
            except ParseError as parseEx:
                print("EXC in meta=%s" % meta)
            except BaseException as ex:
                raise ex
                # print("ERROR : Could not parse source [%s] '%s' with '%s' : '%s" % (self.source_id, meta.path, self.parser_type, ex))
                # print("        Skipping...")
        return entities
