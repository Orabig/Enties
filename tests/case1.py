import unittest


class TestSimpleCase1(unittest.TestCase):

    def test_parse_file_with_parcimonious(self):
        from enties.source import Sources
        from enties.rule import Rules
        sources = Sources("files/case1/sources.yaml")
        self.assertIn('type1', sources.sources_by_id)

        source = sources.sources_by_id['type1']
        paths = [meta.path for meta in source.provide()]
        self.assertEqual(paths, ['files/case1/sources/type1/file1.txt', 'files/case1/sources/type1/file2.txt'])

        rules = Rules("files/case1/rules.yaml")
        result = rules.exec(sources.sources_by_id)
        self.assertEqual(result,
                         [
                             {
                                 "entities": {
                                     "abcdef": {
                                         "id": "abcdef",
                                         "name": "first block"
                                     },
                                     "edfgh": {
                                         "name": "second block"
                                     },
                                     "ijkl": {
                                         "id": "mnopq",
                                         "name": "third block"
                                     }
                                 },
                                 "path": "files/case1/sources/type1/file1.txt",
                                 "source": "type1"
                             },
                             {
                                 "entities": {
                                     "xyz": {
                                         "id": "xyz",
                                         "name": "simple block"
                                     }
                                 },
                                 "path": "files/case1/sources/type1/file2.txt",
                                 "source": "type1"
                             }
                         ])
