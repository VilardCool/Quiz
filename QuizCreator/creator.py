import os.path

from question import Question
from quiz_round import QuizRound
from quiz_package import QuizPackage


def create_question() -> Question:
    text = input("Enter question text: ")
    answers = []
    new_answer = input("Enter answer: ")
    answers.append(new_answer)
    while True:
        new_answer = input("Enter another answer, for cancel enter 'Done': ")
        if new_answer == 'Done':
            break
        else:
            answers.append(new_answer)
    points = int(input("Enter number of points: "))
    type_content = "None"
    while True:
        new_type = input("Enter type of question, it can be 'None', 'Photo', 'Video', 'Music': ")
        if new_type == "None" or new_type == "none" or new_type == "n":
            type_content = "None"
            break
        elif new_type == "Photo" or new_type == "photo" or new_type == "p":
            type_content = "Photo"
            break
        elif new_type == "Video" or new_type == "video" or new_type == "v":
            type_content = "Video"
            break
        elif new_type == "Music" or new_type == "music" or new_type == "m":
            type_content = "Music"
            break
        else:
            print("Wrong type, try again.")
    url = "None"
    while True:
        new_url = input("Enter path to your media, if no media enter 'None': ")
        if new_url == "None" or new_url == "none" or new_url == "n":
            url = "None"
            break
        elif os.path.isfile(new_url):
            url = new_url
            break
        else:
            print("File not exists, try again.")
    return Question(text, answers, points, type_content, url)


def create_round() -> QuizRound:
    number_of_themes = int(input("Enter number of themes: "))
    quiz_round = {}
    while number_of_themes > 0:
        theme = input("Enter theme name: ")
        number_of_questions = int(input("Enter number of question: "))
        questions = []
        while number_of_questions > 0:
            questions.append(create_question())
            number_of_questions -= 1
        quiz_round[theme] = questions
        number_of_themes -= 1
    return QuizRound(quiz_round)


def create_quiz() -> QuizPackage:
    name = input("Enter name of quiz: ")
    number_of_rounds = int(input("Enter number of rounds: "))
    rounds = []
    while number_of_rounds > 0:
        rounds.append(create_round())
        number_of_rounds -= 1
    return QuizPackage(name, rounds, None)
