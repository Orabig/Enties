from enties.source import Sources
from enties.rule import Rules


def main():
    # TODO : source may be loaded from ENV or option
    sources = Sources("test/sources.yaml")
    # TODO : rules should be given as main parameter
    rules = Rules("test/rules.yaml")
    print(rules.exec(sources.sources_by_id))


if __name__ == '__main__':
    main()
