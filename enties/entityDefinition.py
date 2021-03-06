from parsimonious.exceptions import ParseError
from .parsers.parsimonious import Parsimonious
from .processors.commentStripper import strip_comments


class EntityDefinition:
    def __init__(self, rules, rule_path):
        self.source_id = rules['source']
        self.type = rules['type'] if 'type' in rules else self.source_id
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
                all_entities = self.parser.parse(content)
                # TODO  insert meta in each element
                entities += all_entities
            except ParseError as parseEx:
                print("WARNING : ParseError in file:%s :\n%s" % (meta.path, parseEx))
            except BaseException as ex:
                raise ex
        return entities
