from parsimonious.exceptions import ParseError
from .parsers.parsimonious import Parsimonious
from .processors.commentStripper import strip_comments


class Entity:
    def __init__(self, rules, rule_path):
        self.source_id = rules['source']
        self.strip_comments = rules['strip_comments'] if 'strip_comments' in rules else None
        if 'parsimonious' in rules:
            self.parser_type = 'parsimonious'
            self.parser = Parsimonious(rules['parsimonious'], rule_path)
        else:
            raise BaseException("Rules must use one of the following parsers : [parsimonious]")

    def parse(self, sources):
        entities = []
        source = sources.sources_by_id[self.source_id]
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
                print("WARNING : ParseError in file:%s :\n%s" % (meta.path, parseEx))
            except BaseException as ex:
                raise ex
        return entities
