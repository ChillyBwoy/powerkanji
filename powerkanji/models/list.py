import math
from typing import Iterable, List, TypedDict
from collections import UserList

from .entity import KanjiEntity, Jlpt


class KanjiListGroup(TypedDict):
    size: int
    count: int
    kanji: List[KanjiEntity]


class KanjiList(UserList[KanjiEntity]):
    def __init__(self, initlist: Iterable[KanjiEntity] | None = ...) -> None:
        super().__init__(initlist=initlist)
        self.data.sort(key=lambda ent: -ent.jlpt)

    def sort_by_ext_id(self):
        return self.data[:].sort(key=lambda ent: ent.ext_id)

    def group_by_jlpt(self) -> List[List[KanjiEntity]]:
        res: List[List[KanjiEntity]] = []

        for lvl in reversed(Jlpt):
            kanji_list = [kanji for kanji in self if kanji.jlpt == lvl.value]
            kanji_list.reverse()
            res.append(kanji_list)

        return res

    def regroup(self, max_width: int) -> List[KanjiListGroup]:
        grouped: List[KanjiListGroup] = []
        kanji_by_jlpt = self.group_by_jlpt()

        for i, kanji in enumerate(kanji_by_jlpt):
            length = len(kanji)

            try:
                count: int = length + grouped[i - 1]["count"]
            except Exception:
                count: int = length

            size = math.floor(math.sqrt(count))

            grouped.append(
                {
                    "count": count,
                    "size": max_width if i == len(kanji_by_jlpt) - 1 else size,
                    "kanji": kanji,
                }
            )

        return grouped
