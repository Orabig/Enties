
class Entity:
    def __init__(self, sources_by_id, rules):
        self.source = sources_by_id[rules['source']]
