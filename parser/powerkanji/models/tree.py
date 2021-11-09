from dataclasses import asdict, dataclass
from typing import List, Optional

from .entity import KanjiEntity
from .list import KanjiList


@dataclass
class KanjiNode:
    jlpt: int
    starts_at: int
    ends_at: int
    kanji_list: List[KanjiEntity]
    next_level: Optional["KanjiNode"]


@dataclass
class KanjiTree:
    root: KanjiNode

    def __init__(self, kanji_list: KanjiList) -> None:
        self.root = self.__create_from_list(kanji_list)

    def __empty_node(self):
        return KanjiNode(jlpt=-1, starts_at=-1, ends_at=-1, kanji_list=[], next_level=None)

    def __create_from_list(self, kanji_list: KanjiList) -> KanjiNode:
        kanji_by_level = KanjiList(kanji_list).group_by_jlpt()

        def traverse(result: KanjiNode, count: int = 0):
            if len(kanji_by_level) == 0:
                return

            jlpt = len(kanji_by_level)
            kanji = kanji_by_level.pop()
            size = len(kanji)

            result.jlpt = jlpt
            result.starts_at = count
            result.ends_at = count + size
            result.kanji_list = kanji
            result.next_level = self.__empty_node() if jlpt > 1 else None

            if result.next_level:
                traverse(result.next_level, count + len(kanji))

        res = self.__empty_node()

        traverse(res)

        return res

    def to_dict(self):
        return asdict(self.root)
