from enties.source import Sources
from enties.rule import Rules


def main():
    sources = Sources()
    sources.load("test/sources.yaml")

    rules = Rules()
    rules.load("test/rules.yaml", sources.get_by_id())


if __name__ == '__main__':
    main()
