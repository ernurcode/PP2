import pygame
from collections import deque


# ---------------- BASIC SHAPES ----------------

def draw_rect(surface, color, start, end, width):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(start[0] - end[0])
    h = abs(start[1] - end[1])
    pygame.draw.rect(surface, color, (x, y, w, h), width)


def draw_square(surface, color, start, end, width):
    size = max(abs(end[0] - start[0]), abs(end[1] - start[1]))

    x, y = start
    if end[0] < start[0]:
        x = start[0] - size
    if end[1] < start[1]:
        y = start[1] - size

    pygame.draw.rect(surface, color, (x, y, size, size), width)


def draw_circle(surface, color, start, end, width):
    radius = int(((end[0] - start[0])**2 + (end[1] - start[1])**2) ** 0.5)
    pygame.draw.circle(surface, color, start, radius, width)


def draw_line(surface, color, start, end, width):
    pygame.draw.line(surface, color, start, end, width)


# ---------------- TRIANGLES ----------------

def draw_right_triangle(surface, color, start, end, width):
    pygame.draw.polygon(surface, color, [
        start,
        (start[0], end[1]),
        end
    ], width)


def draw_equilateral_triangle(surface, color, start, end, width):
    x1, y1 = start
    x2, y2 = end
    mid_x = (x1 + x2) // 2

    pygame.draw.polygon(surface, color, [
        (mid_x, y1),
        (x1, y2),
        (x2, y2)
    ], width)


def draw_rhombus(surface, color, start, end, width):
    x1, y1 = start
    x2, y2 = end

    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2

    pygame.draw.polygon(surface, color, [
        (cx, y1),
        (x2, cy),
        (cx, y2),
        (x1, cy)
    ], width)


# ---------------- PENCIL ----------------

def pencil(surface, color, prev, current, width):
    if prev:
        pygame.draw.line(surface, color, prev, current, width)


# ---------------- ERASER ----------------

def erase(surface, pos, size):
    pygame.draw.circle(surface, (255, 255, 255), pos, size)


# ---------------- FLOOD FILL ----------------

def flood_fill(surface, x, y, new_color):
    w, h = surface.get_size()
    target = surface.get_at((x, y))

    if target == new_color:
        return

    q = deque()
    q.append((x, y))

    while q:
        cx, cy = q.popleft()

        if 0 <= cx < w and 0 <= cy < h:
            if surface.get_at((cx, cy)) == target:
                surface.set_at((cx, cy), new_color)

                q.append((cx + 1, cy))
                q.append((cx - 1, cy))
                q.append((cx, cy + 1))
                q.append((cx, cy - 1))