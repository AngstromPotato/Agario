import pygame
import socket
import ast
import random
def key_from_value(value, diction):
    return list(diction.keys())[list(diction.values()).index(value)]
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
ADDR = ("192.168.1.37", PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    return ast.literal_eval(str(client.recv(2048).decode(FORMAT)))
pygame.init()
scr = pygame.display.set_mode((500, 350))
pygame.display.set_caption('Agar.io Clone')
run = True
clock = pygame.time.Clock()
direction = None
fps = 20
s = send("PLACEHOLDER")
def draw(size, message, color, xpos, ypos):
    scr.blit(pygame.font.SysFont(None, size).render(message, True, color), (xpos, ypos))
while run:
    scr.fill((255, 255, 255))
    s = send("PLACEHOLDER")
    blobs = s[1]
    values = list(s[0].values())
    draw(25, 'Leaderboard', (0, 0, 0), 380, 10)
    players = s[0]
    leaderboard = s[3]
    leaderboard = sorted(leaderboard, key=lambda l:l[0], reverse=True)[:5]
    startY = 30
    place = 1
    for leader in leaderboard:
        draw(15, f'{place}. Player {leader[1]}: {round(leader[0])}', (0, 0, 0), 385, startY)
        startY += 20
        place += 1
    draw(25, 'You are Player ' + str(s[2][4]), (0, 0, 0), 10, 10)
    for value in values:
        draw(15, 'Player ' + str(value[4]), (0, 0, 0), value[1]+value[3], value[2]+value[3])
    if direction is not None:
        n = send(direction)
        players = n[0]
        blobs = n[1]
        for y in blobs:
            circ = pygame.draw.circle(scr, (random.choice([0, 128, 200]), random.choice([0, 128, 200]), random.choice([0, 128, 200])), (y[0], y[1]), 1)
        values = list(players.values())
        for x in values:
            pygame.draw.circle(scr, x[0], (x[1], x[2]), x[3])
    for z in blobs:
        blob = pygame.draw.circle(scr, (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)), (z[0], z[1]), 1)
        for a in values:
            player = pygame.draw.circle(scr, (a[0][0], a[0][1], a[0][2]), (a[1], a[2]), a[3])
            if player.colliderect(blob):
                send(f"COLLISION {z}")
    if len(values) > 1:
        for b in values:
            for c in values:
                if b != c:
                    player1 = pygame.draw.circle(scr, (b[0][0], b[0][1], b[0][2]), (b[1], b[2]), b[3])
                    player2 = pygame.draw.circle(scr, (c[0][0], c[0][1], c[0][2]), (c[1], c[2]), c[3])
                    if player1.colliderect(player2):
                        send(f"PLAYERCOLL  {b}  {c}  {key_from_value(b, players)}  {key_from_value(c, players)}")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
            elif event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
    clock.tick(fps)
    pygame.display.update()
send("DISCONNECT")
pygame.quit()
quit()
