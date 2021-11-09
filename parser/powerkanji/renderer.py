import math
import os
from jinja2 import Environment, FileSystemLoader
from typing import List

from powerkanji.models import KanjiListGroup, KanjiList


def find_first_group(input: List[KanjiListGroup], idx: int):
    matched = [item for item in input if idx < item["size"] and len(item["kanji"]) > 0]

    if len(matched) > 0:
        return matched[0]


tpl_env = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")),
    autoescape=False,
)
tpl_env.filters["find_first_group"] = find_first_group


class KanjiHTMLRenderer:
    def __init__(self, width: int) -> None:
        self.width = width

    def render_html(self, kanji_list: KanjiList) -> str:
        max_height = math.ceil(len(kanji_list) / self.width)
        kanji_grouped = kanji_list.regroup(self.width)
        tpl = tpl_env.get_template("table.html")

        return tpl.render(
            kanji_grouped=kanji_grouped,
            max_width=self.width,
            max_height=max_height,
        )
