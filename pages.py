
import random


class Page(object):
    def __init__(self, chinese, answer, hint='', error_count_before_hint=2, show_survey=0,
                 is_test=False, marker_data=''):
        self.chinese = chinese
        self.answer = answer
        self.error_count_before_hint = error_count_before_hint
        self.hint = hint
        self.show_survey = show_survey
        self.is_test = is_test
        self.marker_data = marker_data

    def set_hint_on(self):
        self.hint = self.answer

    def set_hint_off(self):
        self.hint = ""

    def set_survey(self, n):
        self.show_survey = n

    def join_chinese(self, another_chinese):
        self.chinese = self.chinese + another_chinese.chinese
        self.answer = self.answer + " " + another_chinese.answer
        self.hint = self.answer

    def __repr__(self):
        return (f'The word {self.chinese} means {self.answer} and the hint is {self.hint} and the survey_number is {self.show_survey}')
