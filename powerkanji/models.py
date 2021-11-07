from enum import Enum
from dataclasses import asdict, dataclass
from typing import List, Optional

class KanjiCreateException(Exception):
    pass

class Jlpt(int, Enum):
    n1 = 1
    n2 = 2
    n3 = 3
    n4 = 4
    n5 = 5


@dataclass
class KanjiReading:
    reading: str
    meanings: List[str]

    def __repr__(self) -> str:
        return f'"{self.reading}": "{"; ".join(self.meanings)}"';


@dataclass
class KanjiEntity:
    kanji: str
    id: int
    key: int
    strokes: int
    jlpt: Jlpt
    onyomi: List[KanjiReading]
    kunyomi: List[KanjiReading]

    def to_dict(self):
        data = asdict(self)
        data["jlpt"] = self.jlpt.value
        return data

    def __post_init__(self):
        match self.jlpt:
            case 1:
                self.jlpt = Jlpt.n1
            case 2:
                self.jlpt = Jlpt.n2
            case 3:
                self.jlpt = Jlpt.n3
            case 4:
                self.jlpt = Jlpt.n4
            case 5:
                self.jlpt = Jlpt.n5
            case _:
                raise KanjiCreateException(f'Unknown JLPT level: {self.jlpt}')


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

    def __init__(self, kanji_list: List[KanjiEntity]) -> None:
        self.root = self.__create_from_list(kanji_list)

    def __empty_node(self):
        return KanjiNode(jlpt=-1, starts_at=-1, ends_at=-1, kanji_list=[], next_level=None)

    def __create_from_list(self, kanji_list: List[KanjiEntity]) -> KanjiNode:
        kanji_by_level = [[kanji for kanji in kanji_list if kanji.jlpt == lvl.value] for lvl in Jlpt]

        def traverse(result: KanjiNode, count: int=0):
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

            if (result.next_level):
                traverse(result.next_level, count + len(kanji))

        res = self.__empty_node()

        traverse(res)

        return res

    def to_dict(self):
        return asdict(self.root)
