import os
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape

from powerkanji.parser import KanjiParser

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
RAW_HTML_PATH = os.path.join(BASE_PATH, "data", "raw.html")
OUT_HTML_PATH = os.path.join(BASE_PATH, "out", "kanji.html")
OUT_JSON_PATH = os.path.join(BASE_PATH, "out", "kanji.json")

tpl_env = Environment(loader=FileSystemLoader(os.path.join("powerkanji", "templates")), autoescape=select_autoescape())


def main():
    kanji_list = []

    with open(RAW_HTML_PATH) as f:
        html = f.read()
        parser = KanjiParser(html)
        kanji_list = parser.parse()

    tpl = tpl_env.get_template("table.html")

    with open(OUT_HTML_PATH, "w") as f:
        html_str = tpl.render(kanji_list=kanji_list)
        f.write(html_str)

    with open(OUT_JSON_PATH, "w") as f:
        json_str = json.dumps([item.to_dict() for item in kanji_list], ensure_ascii=False, indent=4)
        f.write(json_str)


if __name__ == "__main__":
    main()
