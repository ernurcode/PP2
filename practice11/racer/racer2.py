import pygame
import random

pygame.init()

w,h = 400, 600
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()


player_img = pygame.image.load("carp.png")
enemy_img = pygame.image.load("care.png")
coin_img = pygame.image.load("imas.png")
bg = pygame.image.load("road.png")

bg = pygame.transform.scale(bg, (400, 600))
player_img = pygame.transform.scale(player_img, (50, 80))
enemy_img = pygame.transform.scale(enemy_img, (55, 80))
v = random.randrange(20, 51, 5)
coin_img2 = pygame.transform.scale(coin_img, (v, v))

player_rect = player_img.get_rect(center=(200, 540))
player_speed = 6

enemy_rect = enemy_img.get_rect(center=(random.randint(40, w - 100), -100))
enemy_speed = 10
lvl = 1
coin_rect = coin_img2.get_rect(center=(170, -60))
coin_speed = 8
y=0
coins = 0
money = 0
font = pygame.font.SysFont(None, 30)
gameover = False
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not gameover:

        screen.blit(bg, (0, y - 600))
        screen.blit(bg, (0, y))
        y = (y + 8) % 600
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < w:
            player_rect.x += player_speed

        enemy_rect.y += enemy_speed
        if enemy_rect.top > h:
            enemy_rect.y = -100
            enemy_rect.x = random.randint(40, w - 100)

        coin_rect.y += coin_speed
        if coin_rect.top > h:
            coin_rect.y = -200
            coin_rect.x = random.randint(40, w - 60)

        if player_rect.colliderect(coin_rect):
            money += v
            v = random.randrange(20, 51, 5)
            coin_img2 = pygame.transform.scale(coin_img, (v, v))
            coin_rect = coin_img2.get_rect(center=(170, -60))
            coins += 1
            if coins % 3 == 0:
                enemy_speed +=2
            coin_rect.y = -50
            coin_rect.x = random.randint(40, w - 60)

        if player_rect.colliderect(enemy_rect):
            gameover = True

        screen.blit(player_img, player_rect)
        screen.blit(enemy_img, enemy_rect)
        screen.blit(coin_img2, coin_rect)

        text = font.render(f"Coins: {coins}", True, (255, 255, 255))
        text2 = font.render(f"Money: {money}", True, (255, 255, 255))
        screen.blit(text, (w - 120, 10))
        screen.blit(text2, (w - 240, 10))

    else:
        screen.fill((0, 0, 0))

        over_text = pygame.font.SysFont(None, 60).render("GAME OVER", True, (255, 0, 0))
        score_text = pygame.font.SysFont(None, 40).render(f"Coins: {coins}", True, (255, 255, 255))

        screen.blit(over_text, (w//2 - 130, h//2 - 60))
        screen.blit(score_text, (w//2 - 80, h//2))

    pygame.display.update()
    clock.tick(60)
pygame.quit()