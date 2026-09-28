# 실습 과제 진행
from pico2d import *
import math
# 맨처음 해야할 일
open_canvas(800,600)
character = load_image('character.png')

def move_circle():
    print('circle')
    if 'degree' not in globals():
        globals()['degree'] = 0

    for _ in range(72):
        globals()['degree'] = (globals()['degree'] + 5) % 360
        theta = math.radians(globals()['degree'])
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)

        draw_character(x)
    pass

def draw_top():
    print('top')
    for x in range(0, 751, 5):
        draw_character(x)
    pass

def draw_character(x, y=550):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.02)

def draw_left():
    print('left')
    for y in range(550, 49, -5):
        draw_character(750, y)
    pass
def draw_bottom():
    print('bottom')
    for x in range(750, -1, -5):
        draw_character(x, 50)
    pass
def draw_right():
    print('right')
    for y in range(50, 551, 5):
        draw_character(0, y)
    pass

def move_rectangle():
    print('rectangle')
    draw_top()
    draw_left()
    draw_bottom()
    draw_right()
    clear_canvas()
    update_canvas()
    pass

def move_triangle():
    print('triangle')
    points = ((400, 550), (50, 50), (750, 50), (400, 550))
    for start, end in zip(points, points[1:]):
        start_x, start_y = start
        end_x, end_y = end
        for step in range(101):
            ratio = step / 100
            x = round(start_x + (end_x - start_x) * ratio)
            y = round(start_y + (end_y - start_y) * ratio)
            draw_character(x, y)
    pass
while True:
    move_circle()
    move_rectangle()
    move_triangle()
    pass

close_canvas()