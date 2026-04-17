import pygame
from datetime import datetime

def mickclock():
    pygame.init()

    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()

    bg = pygame.image.load("images/b.jpg")
    lh = pygame.image.load("images/lll.png")
    rh = pygame.image.load("images/rrr.png")

    center = (250, 250)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        now = datetime.now()
        sec = now.second
        minute = now.minute

        sec_angle = -sec * 6
        min_angle = -minute * 6

        screen.blit(bg, (0, 0))

        sec_rot = pygame.transform.rotate(lh, sec_angle)
        screen.blit(sec_rot, sec_rot.get_rect(center=center))
        min_rot = pygame.transform.rotate(rh, min_angle)
        screen.blit(min_rot, min_rot.get_rect(center=center))
        pygame.display.update()
        clock.tick(60)

    pygame.quit()