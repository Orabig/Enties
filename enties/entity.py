from .parsers.parsimonious import Parsimonious


class Entity:
    def __init__(self, sources_by_id, rules):
        self.source = sources_by_id[rules['source']]
        if 'parsimonious' in rules:
            self.parser = Parsimonious(rules['parsimonious'])
        else:
            raise BaseException("Rules must use one of the following parsers : [parsimonious]")

    def parse(self):
        # TODO : il faut boucler sur les fichiers (self.source.path + glob(path))
        print(self.parser.parse("""
            block test {
                a: toto
                    b: 1111
                }
            block test2 {
                a: tata
                    b: 222
                }
            """))
