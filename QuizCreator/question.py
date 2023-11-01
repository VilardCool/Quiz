class Question:
    def __init__(self, text, answer, points, type_question, url):
        self.text = text
        self.answer = answer
        self.points = points
        self.type_question = type_question
        self.url = url

    def __str__(self):
        return ("Text: " + self.text + "\n" + "Answer: " + str(self.answer) + "\n"
                + "Points: " + str(self.points) + "\n" + "Type question: " + self.type_question + "\n"
                + "Url: " + self.url)
