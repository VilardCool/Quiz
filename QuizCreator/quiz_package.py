from typing import Optional

from quiz_round import QuizRound
from question import Question


class QuizPackage:
    def __init__(self, rounds: list[QuizRound], final):
        self.rounds = rounds
        self.final = final

    def add_new_round(self, quiz_round: QuizRound):
        self.rounds.append(quiz_round)

    def add_new_theme_to_round(self, number_of_round: int, name_theme: str, questions: list[Question]) -> Optional[str]:
        if (number_of_round <= len(self.rounds)) and (number_of_round > 0):
            self.rounds[number_of_round - 1].add_new_theme(name_theme, questions)
            return None
        else:
            return "There is no round with such number" + str(number_of_round)

    def add_new_question_to_theme_in_round(self, number_of_round: int, name_theme: str,
                                           question: Question) -> Optional[str]:
        if (number_of_round <= len(self.rounds)) and (number_of_round > 0):
            return self.rounds[number_of_round - 1].add_new_question_to_theme(name_theme, question)
        else:
            return "There is no round with such number" + str(number_of_round)
