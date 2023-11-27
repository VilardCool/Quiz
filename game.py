class Game:
    def __init__(self):
        self.players = []
        self.pWent = []
        self.answers = []
        self.scores = []
        self.numberOfQuestions = 0
        self.questions = []

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
        self.pWent[player] = True
    
    def went(self, player):
        return self.pWent[player]

    def answered(self, player):
        return self.answers[player] != ""

    def resetWent(self):
        for p in self.pWent:
            p = False