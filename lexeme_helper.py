from typing import Dict

import pymorphy2

part_of_speach_list = {"СУЩ": "Существительное", "ГЛ": "Глагол", "ПРИЛ": "Прилагательное",
                      "КР_ПРИЧ": "Краткое причастие", "СОЮЗ": "Союз", "ПР": "Предлог",
                      "КР_ПРИЛ": "Краткое прилагательное", "КОМП": "Компаротив", "ИНФ": "Инфинитив",
                      "ПРИЧ": "Причастие", "ДЕЕПР": "Деепричастие", "ЧИСЛ": "Числительное", "Н": "Наречие",
                      "МС": "Местоимение", "ЧАСТ": "Частица", "МЕЖД": "Междометие"}

list_cases = {"nomn": "Именительный", "gent": "Родительный", "datv": "Дательный",
                        "accs": "Винительный", "ablt": "Творительный", "loct": "Предложный"}


class LexemeHelper:
    def __init__(self, lexeme: str):
        self._lexeme = lexeme
        self._analyzer = pymorphy2.MorphAnalyzer()
        self._parsed = self._analyzer.parse(lexeme)[0]
        self._plural_cases = []  # склонения во множественном числе
        self._cases = []  # склонения
        self._current_case = ""
        self._generate_cases()
        self._part_of_speech = self._analyzer.lat2cyr(self._parsed.tag.POS)  # часть речи
        self._normal_form = self._parsed.normal_form
        self._stem = self._get_stem()
        self._struct = {}
        self._generate_lexeme_struct()

    def _generate_cases(self):
        try:
            for case in list_cases.keys():
                case_word = self._parsed.inflect({case}).word
                self._cases.append(case_word)
                if self._current_case == "" and case_word == self._lexeme:
                    self._current_case = list_cases.get(case)

            for case in list_cases.keys():
                case_word = self._parsed.inflect({'plur', case}).word
                self._plural_cases.append(case_word)
                if self._current_case == "" and case_word == self._lexeme:
                    self._current_case = list_cases.get(case)
        except AttributeError:
            print("Не найдено разбора для лексемы \"" + self._lexeme + "\"")

    def _get_stem(self):
        if len(self._cases) == 1:
            return self._cases[0]
        if not self._cases or len(self._cases[0]) == 0:
            return ""
        stem = ""
        for i in range(len(self._cases[0])):
            for j in range(len(self._cases[0]) - i + 1):
                if j > len(stem) and all(self._cases[0][i:i + j] in x for x in self._cases):
                    stem = self._cases[0][i:i + j]
        return stem

    def _generate_lexeme_struct(self):
        if self._current_case == "":
            self._current_case = "Отсутствует"
        if self._stem == "":
            self._stem = "Не определена"
        self._struct = {self._lexeme: {
            "Основа": self._stem,
            "Окончание": self._lexeme.replace(self._stem, ""),
            "Часть речи": part_of_speach_list.get(self._part_of_speech),
            "Начальная форма": self._normal_form,
            "Падеж": self._current_case}}

    def get_lexeme_struct(self) -> Dict:
        return self._struct
