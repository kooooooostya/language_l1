from typing import List
import pymorphy2
from lexeme_helper import LexemeHelper


class DictionaryHelper:
    def __init__(self, text):
        self._dictionary = []
        self._text = text
        self._analyzer = pymorphy2.MorphAnalyzer()
        self._create_dictionary()

    _punctuation_marks = [",", "!", "?", "`", "\"", "\\", "|", "/", "\n", "%", "-"]
    _incorrect_pos = ["NPRO", "PREP", "NUMR", "CONJ", "PRCL", "INTJ", "PRED", "COMP", "ADVB"]

    def _create_dictionary(self):
        for lexeme in self._get_lexems():
            self._dictionary.append(LexemeHelper(lexeme).get_lexeme_struct())

    def get_full_dictionary_string(self):
        dictionary = self._dictionary
        string = ""
        number = 1
        for struct in dictionary:
            string += " " + str(number) + ". " + remove_structure_symbols(str(struct)) + "\n"
            number += 1
        return string

    def _is_correct_pos(self, lexeme: str) -> bool:
        result = self._analyzer.parse(lexeme)
        for pos in self._incorrect_pos:
            if pos in result[0].tag:
                return False
        return True

    def _replace_punctuation(self, word: str) -> str:
        for mark in self._punctuation_marks:
            word = word.replace(mark, "")
        return word

    def _get_lexems(self) -> List[str]:
        sentences = self._text.split(".")
        words = []
        for sentence in sentences:
            word = sentence.split()
            for wrd in word:
                if (self._is_correct_pos(wrd)) and (wrd.isalpha()):
                    wrd = self._replace_punctuation(wrd)
                    words.append(wrd.lower())
        words = list(set(words))
        words.sort(key=str.lower)
        return words


def remove_structure_symbols(structure: str):
    for symbol in ["{", "}", "]", "[", "'"]:
        structure = structure.replace(symbol, "")
    return structure
