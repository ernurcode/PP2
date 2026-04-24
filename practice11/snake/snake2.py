import pygame
import random

pygame.init()  # init pygame

WIDTH, HEIGHT = 600, 400
CELL = 20  # grid size

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # window
clock = pygame.time.Clock()  # FPS control

# colors
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)

v = random.randrange(10, 51, 5)  # food value / color intensity

snake = [(100, 100), (80, 100), (60, 100)]  # snake body
direction = (CELL, 0)  # initial direction

def random_food():
    while True:
        pos = (random.randrange(0, WIDTH, CELL),
               random.randrange(0, HEIGHT, CELL))  # grid position
        if pos not in snake:
            return pos

food = random_food()  # spawn food
food_time = pygame.time.get_ticks()  # timer for food

score = 0
level = 1
money = 0
speed = 7

running = True

while running:
    clock.tick(speed)  # game speed

    for event in pygame.event.get():  # events
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # movement control (no reverse)
    if keys[pygame.K_UP] and direction != (0, CELL):
        direction = (0, -CELL)
    elif keys[pygame.K_DOWN] and direction != (0, -CELL):
        direction = (0, CELL)
    elif keys[pygame.K_LEFT] and direction != (CELL, 0):
        direction = (-CELL, 0)
    elif keys[pygame.K_RIGHT] and direction != (-CELL, 0):
        direction = (CELL, 0)

    # new head position
    x, y = snake[0]
    head = (x + direction[0], y + direction[1])

    # wall collision
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        running = False

    # self collision
    if head in snake:
        running = False

    snake.insert(0, head)  # move snake

    if head == food:
        money += v  # earn money from food
        v = random.randrange(10, 51, 5)  # new food value
        score += 1
        food = random_food()
        food_time = pygame.time.get_ticks()  # reset timer

        # level increase
        if score % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()  # remove tail

    # food timeout (respawn after 5 sec)
    if pygame.time.get_ticks() - food_time > 5000:
        v = random.randrange(10, 51, 5)
        food = random_food()
        food_time = pygame.time.get_ticks()

    screen.fill(BLACK)  # background

    # draw food (color depends on value)
    pygame.draw.rect(screen, (v * 5, 0, 0), (*food, CELL, CELL))

    # draw snake
    for s in snake:
        pygame.draw.rect(screen, GREEN, (*s, CELL, CELL))

    # UI text
    font = pygame.font.SysFont(None, 30)
    screen.blit(font.render(f"Score: {score} LVL: {level}  Money: {money}", True, WHITE), (10, 10))

    pygame.display.update()  # refresh screen

pygame.quit()  # exit pygame