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

btnWidth = 300
btnHeight = 150

playerName = "Player"

ip_address = socket.gethostbyname(socket.gethostname())

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = btnWidth
        self.height = btnHeight

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

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
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

numberOfQuestion = 0
btns = []
movedPlayer = 0
answer = ()
btnApprove = [Button("Correct", 100, 650, (0,0,0)), Button("Incorrect", 600, 650, (0,0,0))]

def redrawWindow(win, network, game, p):
    global movedPlayer, answer
    win.fill((128,128,128))
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
        pygame.draw.rect(win, (0,0,0), (x, y, width, height))
        text = font.render(game.questions[game.question][0], 1, (255,255,255))
        win.blit(text, (x + round(width/2) - round(text.get_width()/2), y + round(height/2) - round(text.get_height()/2)))
        if andStatement(p == movedPlayer, not game.answers[p]):
            inputBox = InputBox(round(width/2), 550, 200, 50)
            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    answerT = inputBox.handle_event(event)
                    if answerT:
                        game = network.send("Answer: "+answerT)
                        run = False

                inputBox.update()

                win.fill((128, 128, 128))
                
                pygame.draw.rect(win, (0,0,0), (x, y, width, height))
                win.blit(text, (x + round(width/2) - round(text.get_width()/2), y + round(height/2) - round(text.get_height()/2)))

                inputBox.draw(win)

                pygame.display.flip()
        if andStatement(p == 0, answer):
            text1 = font.render("Player: "+answer[0], 1, (255,255,255))
            text2 = font.render("Quiz answer: "+answer[1], 1, (255,255,255))
            text3 = font.render("Player answer: "+answer[2], 1, (255,255,255))
            win.blit(text1, (100, 450))
            win.blit(text2, (100, 550))
            win.blit(text3, (600, 550))
            for btn in btnApprove:
                btn.draw(win)
    else:
        text1 = font.render("Judge", 1, (0,0,0))
        win.blit(text1, (100, 700))
        for i in range(len(game.players)):
            text2 = font.render(game.players[i], 1, (0,0,0))
            if (i == 0): win.blit(text2, (100, 800))
            else: win.blit(text2, (300*i, 700))
        for i in range(len(game.scores)):
            text3 = font.render(str(game.scores[i]), 1, (0,0,0))
            if (i != 0):
                win.blit(text3, (300*i, 800))
        
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
        if (player == 0):
            btns.append(Button(game.questions[i][0][:12]+"...",300*i,50, (0,0,0)))
        else:
            btns.append(Button(game.questions[i][1],300*i,50, (0,0,0)))

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
                                game = n.send("move "+str(i))
                    i += 1
                if btnApprove[0].click(pos):
                    game = n.send("score "+answer[0]+"|"+game.questions[game.question][1])
                    answer = ()
                if btnApprove[1].click(pos):
                    game = n.send("incorrect")
                    answer = ()
                            

        redrawWindow(win, n, game, player)

menuBtns1 = [Button("Play", (width-btnWidth)/2, 250, (0,0,0)), Button("Create", (width-btnWidth)/2, 450, (0,255,0))]
menuBtns2 = [Button("Host", (width-btnWidth)/2, 250, (255,0,0)), Button("Join", (width-btnWidth)/2, 450, (0,0,255))]
menu = True
menu1 = False
errorFlag = False
errorText = "No error"

def menu_screen():
    global menu, menu1, errorFlag
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((200, 200, 200))
        if(menu):
            if(menu1):
                for btn in menuBtns2:
                    btn.draw(win)
            else:
                for btn in menuBtns1:
                    btn.draw(win)

        if (errorFlag):
            font = pygame.font.SysFont("comicsans", 80)
            text = font.render("Hosting failed", 1, (255,0,0))
            win.blit(text, (width/2 - text.get_width()/2, 50))
        
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
                if menuBtns1[0].click(pos):
                    menu1 = True

    main()

while True:
    menu_screen()
