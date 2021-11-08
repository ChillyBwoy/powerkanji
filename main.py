import os
import json

from powerkanji.models import KanjiTree, KanjiList
from powerkanji.parser import KanjiParser
from powerkanji.render import KanjiHTMLRenderer

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
RAW_HTML_PATH = os.path.join(BASE_PATH, "data", "raw.html")
OUT_HTML_PATH = os.path.join(BASE_PATH, "out", "kanji.html")
OUT_JSON_LIST_PATH = os.path.join(BASE_PATH, "out", "kanji_list.json")
OUT_JSON_TREE_PATH = os.path.join(BASE_PATH, "out", "kanji_tree.json")


def save_json_list(kanji_list: KanjiList):
    with open(OUT_JSON_LIST_PATH, "w") as f:
        json_str = json.dumps([item.to_dict() for item in kanji_list], ensure_ascii=False, indent=4)
        f.write(json_str)


def save_json_tree(kanji_list: KanjiList):
    with open(OUT_JSON_TREE_PATH, "w") as f:
        tree = KanjiTree(kanji_list)
        json_str = json.dumps(tree.to_dict(), ensure_ascii=False, indent=4)
        f.write(json_str)


def save_html(kanji_list: KanjiList):
    with open(OUT_HTML_PATH, "w") as f:
        html_str = KanjiHTMLRenderer(58).render_html(kanji_list)
        f.write(html_str)


def parse() -> KanjiList:
    with open(RAW_HTML_PATH) as f:
        html = f.read()
        parser = KanjiParser(html)
        # total: 2136
        return parser.parse()


def main():
    kanji_list = parse()

    save_html(kanji_list)
    save_json_list(kanji_list)
    save_json_tree(kanji_list)


if __name__ == "__main__":
    main()
