#!/usr/bin/env python

import os
import json
import argparse
from pathlib import Path
from typing import Optional

from powerkanji.models import KanjiTree, KanjiList
from powerkanji.parser import KanjiParser
from powerkanji.renderer import KanjiHTMLRenderer

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

def write_to_output(payload: str, out_path: Optional[str]):
    if not out_path:
        print(payload)
        return

    file_name = Path(out_path).resolve()

    with open(file_name, "w") as f:
        f.write(payload)


def parse() -> KanjiList:
    raw_html_path = os.path.join(BASE_PATH, "data", "raw.html")

    with open(raw_html_path) as f:
        html = f.read()
        parser = KanjiParser(html)
        return parser.parse()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--format", help="Parse raw html", type=str, choices=["list", "tree", "html"])
    parser.add_argument("-o", "--out", help="Output file", type=str)

    args = parser.parse_args()

    match args.format:
        case 'list':
            kanji_list = parse()
            payload = json.dumps([item.to_dict() for item in kanji_list], ensure_ascii=False, indent=4)

            write_to_output(payload, args.out)

        case 'tree':
            kanji_list = parse()
            tree = KanjiTree(kanji_list)
            payload = json.dumps(tree.to_dict(), ensure_ascii=False, indent=4)

            write_to_output(payload, args.out)

        case 'html':
            kanji_list = parse()
            payload = KanjiHTMLRenderer(58).render_html(kanji_list)

            write_to_output(payload, args.out)


if __name__ == "__main__":
    main()
