class Question:
    def __init__(self, text: str, answers: list[str], points: int, type_content: str, url: str):
        self.text = text
        self.answers = answers
        self.points = points
        self.type_content = type_content
        self.url = url

    def __str__(self):
        return ("Text: " + self.text + "\n" + "Answer: " + str(self.answers) + "\n"
                + "Points: " + str(self.points) + "\n" + "Type question: " + self.type_content + "\n"
                + "Url: " + self.url)

    def get_text(self) -> str:
        return self.text

    def get_answers(self) -> list[str]:
        return self.answers

    def get_points(self) -> int:
        return self.points

    def get_type_content(self) -> str:
        return self.type_content

    def get_url(self) -> str:
        return self.url
