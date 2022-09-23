from random import randint, random
from typing import List, Tuple, Union

import pygame, sys

from geometry import Polygon
import geometry as gmt

pygame.init()

from random import randint
from typing import Tuple


def rand_color(minv: int = 0, maxv: int = 255) -> Tuple[int, int, int]:
    """returns a random RGB color with min and max as min and max threshold"""
    return randint(minv, maxv), randint(minv, maxv), randint(minv, maxv)


def rand_bw_color(minv: int, maxv: int) -> Tuple[int, int, int]:
    """returns a random RGB BW color"""
    shade = randint(minv, maxv)
    return shade, shade, shade


# Constants and font --------------------------
FONT = pygame.font.SysFont("Consolas", 25, True)
FPS = 30
ALPHA_VALUE = 80
SUB_TEXT_ALPHA = 180
SHAPES_NUMBER = 1000
MIN_CIRCLE_RADIUS = 3
MAX_CIRCLE_RADIUS = 15
MIN_RECT_WIDTH = 5
MAX_RECT_WIDTH = 25
MIN_RECT_HEIGHT = 5
MAX_RECT_HEIGHT = 25
BACKGROUND_COLOR = (20, 30, 40)
WIDTH, HEIGHT = 1000, 800
# --------------------------------------------

# Game variables and fundamentals --------------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
keep: bool = True

shapes: List[Polygon] = []
colors: List[Tuple[int, int, int]] = []
colliding_colors: List[Tuple[int, int, int]] = []

feed_active: bool = True
some_polygon: Polygon = Polygon([100, 100], [150, 150], [200, 100])

mouse_polygon: Polygon = Polygon([300, 50], [345, 30], [365, 85], [350, 105], [325, 115])
poly_color_1 = [0, 255, 255]
poly_color_2 = [255, 255, 0]

mouse_circle: gmt.Circle = gmt.Circle(500, 500, 20)
circle_color_1 = [255, 0, 255]
circle_color_2 = [50, 255, 175]

border_color: str = "green"
acc_amt = 0
acc_multiplier = 0.92
# --------------------------------------------

mouse_rect = pygame.Rect(0, 0, 50, 65)
rect_color_1 = [0, 255, 100]
rect_color_2 = [255, 100, 50]

# Game loop
m_frame_steps = 0
change_dir = False
mouse_bind_state = "circle"
poly_color = poly_color_1.copy()
circle_color = circle_color_1.copy()
rect_color = rect_color_1.copy()

while keep:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                mouse_bind_state = "circle"
            elif event.key == pygame.K_p:
                mouse_bind_state = "polygon"
            elif event.key == pygame.K_r:
                mouse_bind_state = "rect"
    
    m_frame_steps = (m_frame_steps + 1) % 400
    mouse_pos = pygame.mouse.get_pos()
    if mouse_bind_state == "rect":
        mouse_rect.center = mouse_pos
    elif mouse_bind_state == "polygon":
        mouse_polygon.move_ip((mouse_pos[0] - mouse_polygon.c_x, mouse_pos[1] - mouse_polygon.c_y))
    elif mouse_bind_state == "circle":
        mouse_circle.move_ip((mouse_pos[0] - mouse_circle.x, mouse_pos[1] - mouse_circle.y))

    if m_frame_steps == 0:
        change_dir = not change_dir
    
    rect_color = rect_color_1.copy()
    polygon_color = poly_color_1.copy()
    circle_color = circle_color_1.copy()
    '''
    if some_polygon.collidepolygon(mouse_polygon):
        poly_color = poly_color_2.copy()
    '''
    if mouse_polygon.colliderect(mouse_rect):
        rect_color = rect_color_2
        polygon_color = poly_color_2
    
    if mouse_polygon.collidecircle(mouse_circle):
        polygon_color = poly_color_2
        circle_color = circle_color_2
    
    if some_polygon.collidecircle(mouse_circle):
        circle_color = circle_color_2
    
    if some_polygon.colliderect(mouse_rect):
        rect_color = rect_color_2
    
    if not change_dir:
        some_polygon.move_ip((1, 1))
    else:
        some_polygon.move_ip((-1, -1))

    screen.fill(BACKGROUND_COLOR)
    clock.tick_busy_loop(FPS)
    pygame.draw.polygon(screen, (250, 0, 250), some_polygon.vertices)
    pygame.draw.polygon(screen, poly_color, mouse_polygon.vertices)
    pygame.draw.circle(screen, circle_color, mouse_circle.center, mouse_circle.r)
    pygame.draw.rect(screen, rect_color, mouse_rect)
    pygame.display.set_caption(str(clock.get_fps()))
    pygame.display.update()


pygame.quit()
