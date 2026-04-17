import pygame

def ballgame():
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((600, 600))

    x = 300
    y = 300

    st = True
    while st:
        screen.fill((255, 255, 255))
        pygame.draw.circle(screen, (255, 0, 0), (x,y), 25)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x>40:
            x -= 20
        elif keys[pygame.K_RIGHT] and x<560:
            x += 20
        if keys[pygame.K_UP] and y>40:
             y -= 20
        elif keys[pygame.K_DOWN]and y<560:
            y += 20
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                st = False
                pygame.quit()
        pygame.display.update()
        clock.tick(17)
