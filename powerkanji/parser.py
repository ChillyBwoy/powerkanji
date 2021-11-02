import re
from typing import List
from bs4 import BeautifulSoup
from bs4.element import Tag

from powerkanji.models import KanjiNode, KanjiReading, Jlpt

class KanjiParseException(Exception):
    pass

class KanjiNodeParser:
    re_onyomi = re.compile(r"ОН-чтение:\s+(?P<kanji_reading>([^<])+)")
    re_kunyomi = re.compile(r"КУН-чтение:\s+(?P<kanji_reading>([^<])+)")
    re_reading = re.compile(r"(?P<reading>[ぁ-んァ-ン、\s]+)(?P<meaning>[^ぁ-んァ-ン]*)")
    re_key = re.compile(r"Ключ:\s+(?P<key>(\d+))")
    re_strokes = re.compile(r"Число черт:\s+(?P<strokes>(\d+))")

    def __init__(self, tag: Tag) -> None:
        self.tag = tag

    def parse(self) -> KanjiNode:
        key, strokes, onyomi, kunyomi = self.__parse_title()

        return KanjiNode(
            kanji=self.__parse_kanji(),
            id=self.__parse_data_id(),
            key=key,
            strokes=strokes,
            jlpt=self.__parse_jlpt(),
            onyomi=onyomi,
            kunyomi=kunyomi,
        )

    def __parse_kanji(self):
        return self.tag.text.strip()

    def __parse_data_id(self):
        return int(self.tag.attrs["data-id"])

    def __parse_jlpt(self):
        jlpt = int(self.tag.attrs["data-jlpt"])

        match jlpt:
            case 1:
                return Jlpt.n1
            case 2:
                return Jlpt.n2
            case 3:
                return Jlpt.n3
            case 4:
                return Jlpt.n4
            case 5:
                return Jlpt.n5
            case _:
                raise KanjiParseException(f'Unknown JLPT level: {self.jlpt}')

    def __parse_reading(self, src: str, pattern: re.Pattern) -> List[KanjiReading]:
        search = pattern.search(src)
        match = search.group("kanji_reading") if search else None

        if not match:
            return []

        reading_search = self.re_reading.findall(match)

        result: List[KanjiReading] = []

        for group in reading_search:
            reading = group[0].strip()
            meanings = [s.strip() for s in group[1].strip().split(";")]

            result.append(KanjiReading(reading=reading, meanings=meanings))

        return result

    def __parse_key(self, src: str) -> int:
        search = self.re_key.search(src)
        value = search.group("key")

        return int(value)

    def __parse_strokes(self, src: str) -> int:
        search = self.re_strokes.search(src)
        value = search.group("strokes")

        return int(value)


    def __parse_title(self):
        title = self.tag.attrs["title"]
        
        key = self.__parse_key(title)
        strokes = self.__parse_strokes(title)
        onyomi = self.__parse_reading(title, self.re_onyomi)
        kunyomi = self.__parse_reading(title, self.re_kunyomi)

        return key, strokes, onyomi, kunyomi


class KanjiParser:
    def __init__(self, html: str) -> None:
        self.html = html

    def parse(self) -> List[KanjiNode]:
        result: List[KanjiNode] = []
            
        soup = BeautifulSoup(self.html, "html.parser")

        for tag in soup.select(".kanji"):
            node = KanjiNodeParser(tag)

            result.append(node.parse())

        return result
