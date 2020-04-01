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
        self.assertEqual(result, [{'entities': [{'id': 'abcdef', 'name': 'first block'},
                                                {'name': 'second block'},
                                                {'id': 'mnopq', 'name': 'third block'},
                                                {'id': 'xyz', 'name': 'simple block'}],
                                   'path': 'files/case1/sources/type1/file1.txt',
                                   'source': 'type1'},
                                  {'entities': [{'id': 'abcdef', 'name': 'first block'},
                                                {'name': 'second block'},
                                                {'id': 'mnopq', 'name': 'third block'},
                                                {'id': 'xyz', 'name': 'simple block'}],
                                   'path': 'files/case1/sources/type1/file2.txt',
                                   'source': 'type1'}])

    def test_parse_file_key_value(self):
        from enties.source import Sources
        from enties.rule import Rules
        sources = Sources("files/case2/sources.yaml")
        self.assertIn('typeA', sources.sources_by_id)
        self.assertIn('typeB', sources.sources_by_id)

        sourceA = sources.sources_by_id['typeA']
        pathsA = [meta.path for meta in sourceA.provide()]
        self.assertEqual(pathsA, ['files/case2/sources/typeA.txt'])

        sourceB = sources.sources_by_id['typeB']
        pathsB = [meta.path for meta in sourceB.provide()]
        self.assertEqual(pathsB, ['files/case2/sources/typeB.txt'])

        rules = Rules("files/case2/rules_kv.yaml")
        result = rules.exec(sources.sources_by_id)
        self.assertEqual(result, [{'entities': [{'a': '1'},
                                                {'a': '7', 'b': '2'},
                                                {'a': '6', 'c': '3', 'e': '9'},
                                                {'a': '6', 'e': '6'},
                                                {'f': '2'}],
                                   'path': 'files/case2/sources/typeA.txt',
                                   'source': 'typeA'}])
