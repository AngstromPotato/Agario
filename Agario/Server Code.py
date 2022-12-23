import socket
import threading
import random
import ast
HEADER = 64
PORT = 8000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
players = {}
blobs = []
for _ in range(20):
    blobs.append([random.randint(0, 500), random.randint(0, 350)])
def handle_client(conn, addr):
    print(f"Welcome {addr}!") 
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    players[f'{addr}'] = [color, random.randint(10, 490), random.randint(10, 340), 10, random.randint(10000, 100000)]
    connected = True
    message = ''
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            leaderboard = [[y[3], y[4]] for y in sorted(list(players.values()), key=lambda l:l[3])]
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == 'DISCONNECT':
                break
            if msg == 'DOWN':
                old = players[f'{addr}']
                if old[2] < 350:
                    old[2] += 7/(old[3]**(1/2))
                players[f'{addr}'] = old
            if msg == 'UP':
                old = players[f'{addr}']
                if old[2] > 0:
                    old[2] -= 7/(old[3]**(1/2))
                players[f'{addr}'] = old
            if msg == 'RIGHT':
                old = players[f'{addr}']
                if old[1] < 500:
                    old[1] += 7/(old[3]**(1/2))
                players[f'{addr}'] = old
            if msg == 'LEFT':
                old = players[f'{addr}']
                if old[1] > 0:
                    old[1] -= 7/(old[3]**(1/2))
                players[f'{addr}'] = old
            if msg.startswith('COLLISION'):
                old = players[f'{addr}']
                old[3] += 0.5
                blobs.remove(ast.literal_eval(msg.split(' ')[1]+msg.split(' ')[2]))
                blobs.append([random.randint(0, 500), random.randint(0, 350)])
            if msg.startswith('PLAYERCOLL'):
                one = ast.literal_eval(msg.split('  ')[1])
                two = ast.literal_eval(msg.split('  ')[2])
                if one[3] > two[3]:
                    two[1] = random.randint(0, 500)
                    two[2] = random.randint(0, 350)
                    one[3] += int(two[3]**0.5)
                    two[3] = 10
                    three = msg.split('  ')[3]
                    four = msg.split('  ')[4]
                    players[three] = one
                    players[four] = two
                elif one[3] == two[3]:
                    pass
                else:
                    one[1] = random.randint(0, 500)
                    one[2] = random.randint(0, 350)
                    two[3] += int(one[3]**0.5)
                    one[3] = 10
                    three = msg.split('  ')[3]
                    four = msg.split('  ')[4]
                    players[three] = one
                    players[four] = two
            conn.sendall(str([players, blobs, players[f'{addr}'], leaderboard, message]).encode(FORMAT))
    conn.close()
def start():
    server.listen()
    print(f"Server is running on IP {SERVER} under port {PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
start()
