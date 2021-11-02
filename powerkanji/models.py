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


class KanjiBase:
    def to_dict(self):
        return asdict(self)


@dataclass
class KanjiReading(KanjiBase):
    reading: str
    meanings: List[str]

    def __repr__(self) -> str:
        return f'"{self.reading}": "{"; ".join(self.meanings)}"';


@dataclass
class KanjiNode(KanjiBase):
    kanji: str
    id: int
    key: int
    strokes: int
    jlpt: Jlpt
    onyomi: List[KanjiReading]
    kunyomi: List[KanjiReading]

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
