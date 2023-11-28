class Game:
    def __init__(self):
        self.players = []
        self.pWent = []
        self.answers = []
        self.answer = False
        self.scores = []
        self.numberOfQuestions = 0
        self.questions = []
        self.question = 0
        self.showQuestions = []

    def add_player(self, p, name):
        self.players[p] = name

    def get_player_answer(self, p):
        return self.answers[p]
    
    def get_number_of_questions(self):
        return self.numberOfQuestions
    
    def set_number_of_questions(self, amount):
        self.numberOfQuestions = amount

    def play(self, player, answer):
        self.answers[player] = answer
        self.answer = True
        self.pWent[player] = False

    def move(self, player, quest):
        self.pWent[player] = True
        self.question = int(quest)
    
    def went(self, player):
        return self.pWent[player]

    def score(self, player, score):
        self.scores[player] = score

    def finQuestion(self):
        self.showQuestions[self.question] = False
        self.question = 0
        self.answer = False
        for i in range(len(self.answers)):
            self.answers[i] = ""