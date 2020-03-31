from enties.source import Sources
from enties.rule import Rules


def main():
    sources = Sources("test/sources.yaml")
    rules = Rules("test/rules.yaml")
    print(rules.exec(sources.sources_by_id))


if __name__ == '__main__':
    main()
