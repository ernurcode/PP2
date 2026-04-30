import pygame
import datetime
import tools

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

color = BLACK
tool = "pencil"
brush_size = 5

drawing = False
start_pos = (0, 0)
prev_mouse = None

line_preview = None

font = pygame.font.SysFont("Arial", 24)
text_mode = False
text_pos = (0, 0)
current_text = ""


running = True
while running:
    screen.fill((200, 200, 200))
    screen.blit(canvas, (0, 0))

    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ---------------- MOUSE DOWN ----------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

            if tool == "fill":
                tools.flood_fill(canvas, event.pos[0], event.pos[1], color)

            if tool == "text":
                text_mode = True
                text_pos = event.pos
                current_text = ""

            if tool == "line":
                line_preview = event.pos

        # ---------------- MOUSE MOVE (LINE PREVIEW) ----------------
        if event.type == pygame.MOUSEMOTION:
            if drawing and tool == "line":
                line_preview = event.pos

        # ---------------- MOUSE UP ----------------
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if tool == "rect":
                tools.draw_rect(canvas, color, start_pos, end_pos, brush_size)

            elif tool == "square":
                tools.draw_square(canvas, color, start_pos, end_pos, brush_size)

            elif tool == "circle":
                tools.draw_circle(canvas, color, start_pos, end_pos, brush_size)

            elif tool == "line":
                tools.draw_line(canvas, color, start_pos, end_pos, brush_size)
                line_preview = None

            elif tool == "right_triangle":
                tools.draw_right_triangle(canvas, color, start_pos, end_pos, brush_size)

            elif tool == "equilateral_triangle":
                tools.draw_equilateral_triangle(canvas, color, start_pos, end_pos, brush_size)

            elif tool == "rhombus":
                tools.draw_rhombus(canvas, color, start_pos, end_pos, brush_size)

        # ---------------- TEXT INPUT ----------------
        if event.type == pygame.KEYDOWN and text_mode:
            if event.key == pygame.K_RETURN:
                img = font.render(current_text, True, color)
                canvas.blit(img, text_pos)
                text_mode = False

            elif event.key == pygame.K_ESCAPE:
                text_mode = False
                current_text = ""

            elif event.key == pygame.K_BACKSPACE:
                current_text = current_text[:-1]

            else:
                current_text += event.unicode

    # ---------------- PENCIL ----------------
    if drawing and tool == "pencil":
        tools.pencil(canvas, color, prev_mouse, mouse, brush_size)
        prev_mouse = mouse
    else:
        prev_mouse = None

    # ---------------- ERASER ----------------
    if drawing and tool == "eraser":
        tools.erase(canvas, mouse, brush_size * 2)

    # ---------------- LINE PREVIEW ----------------
    if tool == "line" and drawing and line_preview:
        pygame.draw.line(screen, color, start_pos, line_preview, brush_size)

    # ---------------- TEXT PREVIEW ----------------
    if text_mode:
        img = font.render(current_text, True, color)
        screen.blit(img, text_pos)

    # ---------------- KEYS ----------------
    keys = pygame.key.get_pressed()

    # tools
    if keys[pygame.K_d]: tool = "pencil"
    if keys[pygame.K_e]: tool = "eraser"
    if keys[pygame.K_r]: tool = "rect"
    if keys[pygame.K_s]: tool = "square"
    if keys[pygame.K_c]: tool = "circle"
    if keys[pygame.K_l]: tool = "line"
    if keys[pygame.K_t]: tool = "right_triangle"
    if keys[pygame.K_y]: tool = "equilateral_triangle"
    if keys[pygame.K_h]: tool = "rhombus"
    if keys[pygame.K_f]: tool = "fill"
    if keys[pygame.K_x]: tool = "text"

    # brush sizes
    if keys[pygame.K_1]: brush_size = 2
    if keys[pygame.K_2]: brush_size = 5
    if keys[pygame.K_3]: brush_size = 10

    # colors
    if keys[pygame.K_4]: color = BLACK
    if keys[pygame.K_5]: color = RED
    if keys[pygame.K_6]: color = GREEN
    if keys[pygame.K_7]: color = BLUE

    # save PNG
    if keys[pygame.K_LCTRL] and keys[pygame.K_s]:
        filename = datetime.datetime.now().strftime("paint_%Y-%m-%d_%H-%M-%S.png")
        pygame.image.save(canvas, filename)

    pygame.display.update()
    clock.tick(120)

pygame.quit()