#!/usr/bin/env python3
import json

from enties.source import Sources
from enties.rule import Rules


def main(arguments):
    sources = Sources(args.sources)
    rules = Rules(args.rules)
    print(json.dumps(rules.exec(sources)))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Extract graph of objects from raw files.')
    parser.add_argument('rules', help='path to a yaml rules file')
    parser.add_argument('-s', '--sources', help='path to a yaml sources file', required=True)
    args = parser.parse_args()
    main(args)
