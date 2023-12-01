import pygame
from network import Network
import pickle
import os
import socket
import subprocess
from _thread import *

pygame.font.init()

width = 1600
height = 900
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
color = 0, 0, 0
btnWidth = width / 4
btnHeight = height / 6
playerName = "Player"

ip_address = socket.gethostbyname(socket.gethostname())


class Button:
    def __init__(self, text, x, y, color, width, height):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


numberOfQuestion = 0
btns = []
movedPlayer = 0
answer = ()
btnApprove = [Button("Correct", 100, 650, (0, 0, 0), btnWidth, btnHeight),
              Button("Incorrect", 600, 650, (0, 0, 0), btnWidth, btnHeight)]


def redrawWindow(win, network, game, p):
    global movedPlayer, answer
    win.fill((113, 169, 247))
    font = pygame.font.SysFont("comicsans", 40)

    choosed = False
    for player in range(len(game.pWent)):
        if game.pWent[player] == True:
            choosed = True
            movedPlayer = player
            break

    orStatement = lambda a, b: True if a or b else False
    andStatement = lambda a, b: True if a and b else False
    if orStatement(choosed, game.get_player_answer(movedPlayer)):
        x = 100
        y = 100
        width = 1000
        height = 500
        pygame.draw.rect(win, (0, 0, 0), (x, y, width, height))
        text = font.render(game.questions[game.question][0], 1, (255, 255, 255))
        win.blit(text, (
        x + round(width / 2) - round(text.get_width() / 2), y + round(height / 2) - round(text.get_height() / 2)))
        if andStatement(p == movedPlayer, not game.answers[p]):
            inputBox = InputBox(round(width / 2), 550, 200, 50)
            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    answerT = inputBox.handle_event(event)
                    if answerT:
                        game = network.send("Answer: " + answerT)
                        run = False

                inputBox.update()

                win.fill((113, 169, 247))

                pygame.draw.rect(win, (0, 0, 0), (x, y, width, height))
                win.blit(text, (x + round(width / 2) - round(text.get_width() / 2),
                                y + round(height / 2) - round(text.get_height() / 2)))

                inputBox.draw(win)

                pygame.display.flip()
        if andStatement(p == 0, answer):
            text1 = font.render("Player: " + answer[0], 1, (255, 255, 255))
            text2 = font.render("Quiz answer: " + answer[1], 1, (255, 255, 255))
            text3 = font.render("Player answer: " + answer[2], 1, (255, 255, 255))
            win.blit(text1, (100, 450))
            win.blit(text2, (100, 550))
            win.blit(text3, (600, 550))
            for btn in btnApprove:
                btn.draw(win)
    else:
        text1 = font.render("Judge", 1, (0, 0, 0))
        win.blit(text1, (100, 700))
        for i in range(len(game.players)):
            text2 = font.render(game.players[i], 1, (0, 0, 0))
            if (i == 0):
                win.blit(text2, (100, 800))
            else:
                win.blit(text2, (300 * i, 700))
        for i in range(len(game.scores)):
            text3 = font.render(str(game.scores[i]), 1, (0, 0, 0))
            if (i != 0):
                win.blit(text3, (300 * i, 800))

        for i in range(len(btns)):
            if game.showQuestions[i]:
                btns[i].draw(win)

    pygame.display.update()


def main():
    global numberOfQuestion, answer
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    game = n.send("numberOfQuestion")
    numberOfQuestion = game.get_number_of_questions()

    for i in range(numberOfQuestion):
        if player == 0:
            btns.append(Button(game.questions[i][0][:6] + "...", 100 + ((width - 200) / numberOfQuestion) * i, 150,
                               (0, 0, 0), (width - 200) / numberOfQuestion, btnHeight))
        else:
            btns.append(Button(game.questions[i][1], 100 + ((width - 200) / numberOfQuestion) * i, 150, (0, 0, 0),
                               (width - 200) / numberOfQuestion, btnHeight))

    game = n.send("Name: " + playerName)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if player == 0 and game.answer:
            answer = n.send("getAnswer")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                i = 0
                for btn in btns:
                    if btn.click(pos):
                        if player != 0:
                            canChoose = True
                            for w in game.pWent:
                                if w == True:
                                    canChoose = False
                            if canChoose:
                                game = n.send("move " + str(i))
                    i += 1
                if btnApprove[0].click(pos):
                    game = n.send("score " + answer[0] + "|" + game.questions[game.question][1])
                    answer = ()
                if btnApprove[1].click(pos):
                    game = n.send("incorrect")
                    answer = ()

        redrawWindow(win, n, game, player)


menuBtns1 = [Button("Play", (width - btnWidth) / 2, height / 2.5, (114, 25, 90), btnWidth, btnHeight),
             Button("Create", (width - btnWidth) / 2, height / 1.7, (114, 25, 90), btnWidth, btnHeight),
             Button("Settings", (width - btnWidth) / 2, height / 1.3, (114, 25, 90), btnWidth, btnHeight)
             ]
menuBtns2 = [Button("Host", (width - btnWidth) / 2, height / 2.5, (48, 76, 137), btnWidth, btnHeight),
             Button("Join", (width - btnWidth) / 2, height / 1.7, (48, 76, 137), btnWidth, btnHeight),
             Button("Back", (width - btnWidth) / 1, height / 1.2, (148, 16, 54), btnWidth, btnHeight)]

menuBtns3 = [Button("Back", (width - btnWidth) / 1, height / 1.2, (148, 16, 54), btnWidth, btnHeight)]
menu = True
menu1 = False
menu2 = False
errorFlag = False
errorText = "No error"


def menu_screen():
    global menu, menu1, menu2, errorFlag, playerName
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((113, 169, 223))

        if (menu):
            if (menu1):
                for btn in menuBtns2:
                    btn.draw(win)
                    font = pygame.font.SysFont("comicsans", 100)
                    text1 = font.render("Super Quiz", 1, (0, 0, 0))
                    win.blit(text1, ((width - btnWidth) / 2 - 70, height / 8))

            elif (menu2):

                for btn in menuBtns3:
                    font = pygame.font.SysFont("comicsans", 100)
                    text1 = font.render("Settings", 1, (0, 0, 0))
                    pl = "Player name: "
                    texttext = pl + playerName
                    font = pygame.font.SysFont("comicsans", 50)
                    text2 = font.render(texttext, 1, (0, 0, 0))
                    font = pygame.font.SysFont("comicsans", 60)
                    text4 = font.render("Change name", 1, (0, 0, 0))
                    inputBox = InputBox((width - btnWidth) / 8, height / 2+100, 500, 50)
                    run_box = True
                    while run_box:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False
                            Player = inputBox.handle_event(event)
                            if Player:
                                playerName=Player
                                run_box = False
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                                if (menuBtns3[0].click(pos)):
                                    run_box = False
                                    menu2=False
                        inputBox.update()

                        win.fill((113, 169, 247))
                        btn.draw(win)
                        pygame.draw.rect(win, (48, 76, 137), ((width - btnWidth) / 8, height / 2, btnWidth, btnHeight))
                        win.blit(text4, ((width - btnWidth) / 8, height / 2))
                        win.blit(text2, ((width - btnWidth) / 8, height / 3))
                        win.blit(text1, ((width - btnWidth) / 2 - 70, height / 8))
                        inputBox.draw(win)

                        pygame.display.flip()


            else:
                for btn in menuBtns1:
                    btn.draw(win)
                    font = pygame.font.SysFont("comicsans", 100)
                    text1 = font.render("Super Quiz", 1, (0, 0, 0))
                    win.blit(text1, ((width - btnWidth) / 2 - 70, height / 8))

        if (errorFlag):
            font = pygame.font.SysFont("comicsans", 80)
            text = font.render("Hosting failed", 1, (255, 0, 0))
            win.blit(text, (width / 2 - text.get_width() / 2, 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (menu1 & menuBtns2[0].click(pos)):
                    try:
                        run = False
                    except:
                        errorText = "Hosting failed"
                        errorFlag = True
                        print(errorText)
                if (menu1 & menuBtns2[1].click(pos)):
                    run = False
                if menuBtns3[0].click(pos):  # settings off
                    menu2 = False

                if menuBtns1[0].click(pos):  # play on
                    menu1 = True
                if menuBtns2[2].click(pos):  # play off
                    menu1 = False
                if menuBtns1[1].click(pos):  # settings on
                    menu2 = True
                    # width = 1500 #test mode
                    # height = 550
                    # pygame.display.update()
                    # pygame.display.set_mode((width, height))
                if menuBtns1[2].click(pos):  # settings on
                    menu2 = True

    main()


while True:
    menu_screen()
