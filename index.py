import pygame
import random

x = 500
y = 500

run = True
lives = 3
coins = 0

racketWidth = 100
racketHeight = 15
racketX = 200
racketY = 450
speed = 0
baseSpeed = 4

ballRadius = 15

balls = [{
    "x": x // 2,
    "y": y // 2,
    "xs": 2,
    "ys": -3
}]

pygame.init()
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Pong mit Shop + Multiball")

font = pygame.font.SysFont(None, 30)
bigFont = pygame.font.SysFont(None, 50)

def reset():
    global lives, balls, racketX, speed

    lives -= 1

    if lives <= 0:
        return False

    balls = [{
        "x": x // 2,
        "y": y // 2,
        "xs": random.choice([-2, -1, 1, 2]),
        "ys": -3
    }]

    racketX = 200
    speed = 0

    pygame.time.wait(800)
    return True

def moveRacket():
    global racketX
    racketX += speed

    if racketX < 0:
        racketX = 0
    if racketX > x - racketWidth:
        racketX = x - racketWidth

def moveBalls():
    for b in balls:
        b["x"] += b["xs"]
        b["y"] += b["ys"]

def ballBlock():
    global coins, run

    for b in balls[:]:
        if b["y"] - ballRadius <= 0:
            b["ys"] *= -1

        if b["x"] - ballRadius <= 0 or b["x"] + ballRadius >= x:
            b["xs"] *= -1

        if b["y"] >= racketY - ballRadius:
            if racketX <= b["x"] <= racketX + racketWidth:
                b["ys"] *= -1
                coins += 1
            else:
                balls.remove(b)

    if len(balls) == 0:
        run = reset()

def shop():
    global coins, racketWidth, baseSpeed, lives, balls

    shopping = True

    while shopping:
        screen.fill((30, 30, 30))

        title = bigFont.render("SHOP", True, (255, 255, 255))
        screen.blit(title, (180, 50))

        items = [
            "1: +20 Breite (5 Coins)",
            "2: +1 Speed (5 Coins)",
            "3: +1 Leben (10 Coins)",
            "4: +1 Ball (10 Coins)",
            "ESC: Zurueck"
        ]

        for i, txt in enumerate(items):
            text = font.render(txt, True, (255, 255, 255))
            screen.blit(text, (120, 150 + i * 40))

        coinText = font.render(f"Coins: {coins}", True, (255, 255, 0))
        screen.blit(coinText, (180, 380))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    shopping = False

                if event.key == pygame.K_1 and coins >= 5:
                    racketWidth += 20
                    coins -= 5

                if event.key == pygame.K_2 and coins >= 5:
                    baseSpeed += 1
                    coins -= 5

                if event.key == pygame.K_3 and coins >= 10:
                    lives += 1
                    coins -= 10

                if event.key == pygame.K_4 and coins >= 10:
                    balls.append({
                        "x": random.randint(50, 450),
                        "y": 200,
                        "xs": random.choice([-2, -1, 1, 2]),
                        "ys": -3
                    })
                    coins -= 10

    return True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed = -baseSpeed
            if event.key == pygame.K_RIGHT:
                speed = baseSpeed
            if event.key == pygame.K_s:
                run = shop()

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                speed = 0

    screen.fill((0, 0, 0))

    moveRacket()
    moveBalls()
    ballBlock()

    pygame.draw.rect(screen, (255, 60, 0), (racketX, racketY, racketWidth, racketHeight))

    for b in balls:
        pygame.draw.circle(screen, (255, 255, 0), (int(b["x"]), int(b["y"])), ballRadius)

    livesText = font.render(f"Leben: {lives}", True, (255, 255, 255))
    coinsText = font.render(f"Coins: {coins}", True, (255, 255, 0))

    screen.blit(livesText, (10, 10))
    screen.blit(coinsText, (10, 40))

    pygame.display.flip()
    pygame.time.wait(5)

pygame.quit()



