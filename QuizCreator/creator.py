import os.path

from question import Question


def create_question():
    text = input("Enter question text: ")
    answer = []
    new_answer = input("Enter answer: ")
    answer.append(new_answer)
    while True:
        new_answer = input("Enter another answer, for cancel enter 'Done': ")
        if new_answer == 'Done':
            break
        else:
            answer.append(new_answer)
    points = int(input("Enter number of points: "))
    type_question = "None"
    while True:
        new_type = input("Enter type of question, it can be 'None', 'Photo', 'Video', 'Music': ")
        if new_type == "None" or new_type == "none" or new_type == "n":
            type_question = "None"
            break
        elif new_type == "Photo" or new_type == "photo" or new_type == "p":
            type_question = "Photo"
            break
        elif new_type == "Video" or new_type == "video" or new_type == "v":
            type_question = "Video"
            break
        elif new_type == "Music" or new_type == "music" or new_type == "m":
            type_question = "Music"
            break
        else:
            print("Wrong type, try again.")
    url = None
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
    return Question(text, answer, points, type_question, url)
