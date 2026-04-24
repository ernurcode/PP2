import pygame

pygame.init()

w, h = 800, 600
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

canvas = pygame.Surface((w, h))
canvas.fill((255, 255, 255))

# colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

color = BLACK
tool = "brush"

drawing = False
start_pos = (0, 0)

running = True
while running:
    screen.fill((200, 200, 200))
    screen.blit(canvas, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # mouse down
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

            if event.button == 1:
                if tool == "brush":
                    pygame.draw.circle(canvas, color, event.pos, 5)

        # mouse up
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

            end_pos = event.pos

            if tool == "rect":
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                width = abs(start_pos[0] - end_pos[0])
                height = abs(start_pos[1] - end_pos[1])
                pygame.draw.rect(canvas, color, (x, y, width, height), 2)

            if tool == "circle":
                radius = int(((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2) ** 0.5)
                pygame.draw.circle(canvas, color, start_pos, radius, 2)

    # drawing while moving
    if drawing and tool == "brush":
        pos = pygame.mouse.get_pos()
        pygame.draw.circle(canvas, color, pos, 5)

    # keys for tools and colors
    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
        tool = "rect"
    if keys[pygame.K_c]:
        tool = "circle"
    if keys[pygame.K_b]:
        tool = "brush"
    if keys[pygame.K_e]:
        tool = "eraser"

    if keys[pygame.K_1]:
        color = BLACK
    if keys[pygame.K_2]:
        color = RED
    if keys[pygame.K_3]:
        color = GREEN
    if keys[pygame.K_4]:
        color = BLUE

    # eraser
    if tool == "eraser" and drawing:
        pos = pygame.mouse.get_pos()
        pygame.draw.circle(canvas, WHITE, pos, 15)

    pygame.display.update()
    clock.tick(400)

pygame.quit()