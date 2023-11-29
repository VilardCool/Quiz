from typing import Optional

import xml.etree.ElementTree as ElTree

from quiz_round import QuizRound
from question import Question


class QuizPackage:
    def __init__(self, name: str, rounds: list[QuizRound], final):
        self.name = name
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

    def get_name(self) -> str:
        return self.name

    def set_name(self, new_name: str) -> None:
        self.name = new_name

    def get_rounds(self) -> list[QuizRound]:
        return self.rounds


def write_to_xml(package: QuizPackage):
    data = ElTree.Element("package")

    for quiz_round in package.get_rounds():
        quiz_name_element = ElTree.SubElement(data, "Quiz")
        quiz_name_element.text = package.get_name()

        round_element = ElTree.SubElement(data, "Round")

        themes = quiz_round.get_themes()

        for theme in themes:
            theme_element = ElTree.SubElement(round_element, "Theme")
            name_element = ElTree.SubElement(theme_element, "Title")
            name_element.text = theme
            questions_element = ElTree.SubElement(theme_element, "Questions")

            for question in quiz_round.get_questions_by_theme(theme):
                question_element = ElTree.SubElement(questions_element, "Question")

                text_element = ElTree.SubElement(question_element, "Text")
                text_element.text = question.get_text()

                answers_element = ElTree.SubElement(question_element, "Answers")
                for answer in question.get_answers():
                    answer_element = ElTree.SubElement(answers_element, "Answer")
                    answer_element.text = answer

                points_element = ElTree.SubElement(question_element, "Points")
                points_element.text = str(question.get_points())

                type_content_element = ElTree.SubElement(question_element, "Content")
                type_content_element.text = question.get_type_content()

                url_element = ElTree.SubElement(question_element, "URL")
                url_element.text = question.get_url()

    xml_text = ElTree.tostring(data)

    with open(package.get_name() + ".quiz", "wb") as file_package:
        file_package.write(xml_text)


def read_from_xml(file_path:str) -> QuizPackage:
    tree = ElTree.parse(file_path)
    root = tree.getroot()
    name = root[0].text
    rounds = []
    for i in range(1, len(root)):
        quiz_round = root[i]
        round_ = {}
        for theme in quiz_round:
            title = theme[0].text
            quiz_questions = theme[1]
            questions = []
            for question in quiz_questions:
                text = question[0].text
                answers = []
                for answer in question[1]:
                    answers.append(answer.text)
                points = int(question[2].text)
                content = question[3].text
                url = question[4].text
                questions.append(Question(text, answers, points, content, url))
            round_[title] = questions
        rounds.append(QuizRound(round_))
    return QuizPackage(name, rounds, False)
