import socket
from _thread import *
import pickle
from game import Game

quiz = []

f = open("quiz.txt", "r")
for l in f:
  quiz.append(l.split("|"))

listOfClients=[]

game = Game()

for q in quiz:
  game.questions.append((q[0], q[1]))
  game.showQuestions.append(True)

#server = "26.95.134.185"
server = socket.gethostbyname(socket.gethostname())
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

def threaded_client(conn, p):
    conn.send(str.encode(str(p)))

    while True:
        try:
            data = conn.recv(4096).decode()

            if (data != "get"): print(data)

            if not data:
                break
            else:
                if data == "reset":
                    game.resetWent()
                elif data == "numberOfQuestion":
                    game.set_number_of_questions(len(quiz))
                elif data[:6] == "Name: ":
                    game.add_player(p, data[6:])
                elif data[:8] == "Answer: ":
                    game.play(p, data[8:])
                elif data[:5] == "move ":
                    game.move(p, data[5:])
                elif data[:6] == "score " and p == 0:
                    dat = data[6:].split("|")
                    game.score(int(dat[0]), int(dat[1]))
                    game.finQuestion()
                elif data == "incorrect":
                    game.finQuestion()
                elif data == "getAnswer" and p == 0:
                    player = 0
                    for ans in game.answers:
                        if ans != "":
                            answer = (str(player), quiz[game.question][2][:-1], ans)
                            conn.send(pickle.dumps(answer))
                            break
                        player += 1
                elif data != "get":
                    game.play(p, data)

                conn.sendall(pickle.dumps(game))
        except:
            break

    print("Lost connection")
    try:
        listOfClients.pop(p)
        game.pWent.pop(p)
        game.answers.pop(p)
        game.scores.pop(p)
        game.players.pop(p)
    except:
        pass
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    listOfClients.append(conn)
    p = len(listOfClients) - 1
    game.pWent.append(False)
    game.answers.append("")
    game.scores.append(0)
    game.players.append("_")

    start_new_thread(threaded_client, (conn, p))