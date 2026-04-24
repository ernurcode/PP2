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

# snake body (list of segments)
snake = [(100, 100), (80, 100), (60, 100)]
direction = (CELL, 0)  # initial movement direction

def random_food():
    while True:
        pos = (random.randrange(0, WIDTH, CELL),
               random.randrange(0, HEIGHT, CELL))  # random grid position
        if pos not in snake:
            return pos

food = random_food()  # spawn food

score = 0
level = 1
speed = 7

running = True

while running:
    clock.tick(speed)  # control game speed

    for event in pygame.event.get():  # events
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # direction control (prevent reverse movement)
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
        score += 1
        food = random_food()  # new food

        # level up logic
        if score % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()  # remove tail

    screen.fill(BLACK)  # background

    pygame.draw.rect(screen, RED, (*food, CELL, CELL))  # draw food

    for s in snake:
        pygame.draw.rect(screen, GREEN, (*s, CELL, CELL))  # draw snake

    # score text
    font = pygame.font.SysFont(None, 30)
    screen.blit(font.render(f"Score: {score} LVL: {level}", True, WHITE), (10, 10))

    pygame.display.update()  # refresh screen

pygame.quit()  # exit