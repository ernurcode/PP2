import pygame

pygame.init()

w, h = 800, 600
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

canvas = pygame.Surface((w, h))
canvas.fill((255, 255, 255))

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

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

            

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if tool == "rect":
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                w_ = abs(start_pos[0] - end_pos[0])
                h_ = abs(start_pos[1] - end_pos[1])
                pygame.draw.rect(canvas, color, (x, y, w_, h_), 4)

            if tool == "square":
               size = max(abs(end_pos[0] - start_pos[0]),
               abs(end_pos[1] - start_pos[1]))

               x = start_pos[0]
               y = start_pos[1]
               if end_pos[0] < start_pos[0]:
                   x = start_pos[0] - size
               if end_pos[1] < start_pos[1]:
                   y = start_pos[1] - size
               pygame.draw.rect(canvas, color, (x, y, size, size), 4)

            if tool == "circle":
                radius = int(((end_pos[0] - start_pos[0])**2 +
                              (end_pos[1] - start_pos[1])**2) ** 0.5)
                pygame.draw.circle(canvas, color, start_pos, radius, 4)

            if tool == "right_triangle":
                pygame.draw.polygon(canvas, color, [
                    start_pos,
                    (start_pos[0], end_pos[1]),
                    end_pos
                ], 4)

            if tool == "equilateral_triangle":
                x1, y1 = start_pos
                x2, y2 = end_pos
                mid_x = (x1 + x2) // 2
                pygame.draw.polygon(canvas, color, [
                    (mid_x, y1),
                    (x1, y2),
                    (x2, y2)
                ], 4)

            if tool == "rhombus":
                x1, y1 = start_pos
                x2, y2 = end_pos
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                pygame.draw.polygon(canvas, color, [
                    (cx, y1),
                    (x2, cy),
                    (cx, y2),
                    (x1, cy)
                ], 4)

    if drawing and tool == "draw":
        pos = pygame.mouse.get_pos()
        pygame.draw.circle(canvas, color, pos, 5)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
        tool = "rect"
    if keys[pygame.K_c]:
        tool = "circle"
    if keys[pygame.K_d]:
        tool = "draw"
    if keys[pygame.K_e]:
        tool = "eraser"

    if keys[pygame.K_s]:
        tool = "square"
    if keys[pygame.K_t]:
        tool = "right_triangle"
    if keys[pygame.K_y]:
        tool = "equilateral_triangle"
    if keys[pygame.K_h]:
        tool = "rhombus"

    if keys[pygame.K_1]:
        color = BLACK
    if keys[pygame.K_2]:
        color = RED
    if keys[pygame.K_3]:
        color = GREEN
    if keys[pygame.K_4]:
        color = BLUE

    if tool == "eraser" and drawing:
        pos = pygame.mouse.get_pos()
        pygame.draw.circle(canvas, WHITE, pos, 15)

    pygame.display.update()
    clock.tick(400)

pygame.quit()