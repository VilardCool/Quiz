from typing import Optional

from question import Question


class QuizRound:
    def __init__(self, themes: dict[str, list[Question]]):
        self.themes = themes

    def add_new_theme(self, name_theme: str, questions: list[Question]) -> None:
        self.themes[name_theme] = questions

    def add_new_question_to_theme(self, name_theme: str, question: Question) -> Optional[str]:
        if name_theme in self.themes.keys():
            self.themes[name_theme].append(question)
            return None
        else:
            return "There is no theme with name: " + name_theme

    def remove_theme(self, name_theme: str) -> Optional[str]:
        if name_theme in self.themes.keys():
            self.themes.pop(name_theme)
            return None
        else:
            return "There is no theme with name: " + name_theme

    def remove_question_from_theme(self, name_theme: str, question: Question) -> Optional[str]:
        if name_theme in self.themes.keys():
            if question in self.themes[name_theme]:
                self.themes[name_theme].remove(question)
                return None
            else:
                return "There is no theme with question: " + str(question)
        else:
            return "There is no theme with name: " + name_theme

    def get_round(self) -> dict[str, list[Question]]:
        return self.themes

    def get_themes(self):
        return self.themes.keys()

    def get_questions_by_theme(self, theme: str) -> list[Question]:
        return self.themes[theme]
