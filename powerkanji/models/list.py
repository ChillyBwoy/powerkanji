from typing import Iterable
from collections import UserList

from .entity import KanjiEntity, Jlpt


class KanjiList(UserList[KanjiEntity]):
    def __init__(self, initlist: Iterable[KanjiEntity] | None = ...) -> None:
        super().__init__(initlist=initlist)
        self.data.sort(key=lambda ent: -ent.jlpt)

    def sort_by_ext_id(self):
        return self.data[:].sort(key=lambda ent: ent.ext_id)

    def group_by_jlpt(self):
        return [[kanji for kanji in self if kanji.jlpt == lvl.value] for lvl in reversed(Jlpt)]
