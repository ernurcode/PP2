import pygame
import random

pygame.init()  # init pygame

w, h = 400, 600
screen = pygame.display.set_mode((w, h))  # window
clock = pygame.time.Clock()  # FPS control

# load images
player_img = pygame.image.load("carp.png")
enemy_img = pygame.image.load("care.png")
coin_img = pygame.image.load("imas.png")
bg = pygame.image.load("road.png")

# resize images
bg = pygame.transform.scale(bg, (400, 600))
player_img = pygame.transform.scale(player_img, (50, 80))
enemy_img = pygame.transform.scale(enemy_img, (55, 80))
coin_img = pygame.transform.scale(coin_img, (30, 30))

# player setup
player_rect = player_img.get_rect(center=(200, 540))
player_speed = 6

# enemy setup
enemy_rect = enemy_img.get_rect(center=(random.randint(40, w - 100), -100))
enemy_speed = 13

# coin setup
coin_rect = coin_img.get_rect(center=(170, -50))
coin_speed = 8

y = 0  # background scroll
coins = 0  # score

font = pygame.font.SysFont(None, 30)
gameover = False

running = True
while running:

    for event in pygame.event.get():  # events
        if event.type == pygame.QUIT:
            running = False

    if not gameover:

        # background scrolling
        screen.blit(bg, (0, y - 600))
        screen.blit(bg, (0, y))
        y = (y + 8) % 600

        # movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < w:
            player_rect.x += player_speed

        # enemy movement
        enemy_rect.y += enemy_speed
        if enemy_rect.top > h:
            enemy_rect.y = -100
            enemy_rect.x = random.randint(40, w - 100)

        # coin movement
        coin_rect.y += coin_speed
        if coin_rect.top > h:
            coin_rect.y = -200
            coin_rect.x = random.randint(40, w - 60)

        # coin collision
        if player_rect.colliderect(coin_rect):
            coins += 1
            coin_rect.y = -50
            coin_rect.x = random.randint(40, w - 60)

        # enemy collision
        if player_rect.colliderect(enemy_rect):
            gameover = True

        # draw objects
        screen.blit(player_img, player_rect)
        screen.blit(enemy_img, enemy_rect)
        screen.blit(coin_img, coin_rect)

        # score text
        text = font.render(f"Coins: {coins}", True, (0, 0, 0))
        screen.blit(text, (w - 120, 10))

    else:
        # game over screen
        screen.fill((0, 0, 0))

        over_text = pygame.font.SysFont(None, 60).render("GAME OVER", True, (255, 255, 255))
        score_text = pygame.font.SysFont(None, 40).render(f"Coins: {coins}", True, (255, 255, 255))

        screen.blit(over_text, (w//2 - 130, h//2 - 60))
        screen.blit(score_text, (w//2 - 80, h//2))

    pygame.display.update()  # update screen
    clock.tick(60)  # FPS limit

pygame.quit()  # exit pygame