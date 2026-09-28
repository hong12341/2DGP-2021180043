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
    for x in range(0, 750, 5):
        draw_character(x)
    pass

def draw_character(x):
    clear_canvas()
    character.draw(x, 550)
    update_canvas()
    delay(0.02)

def draw_left():
    print('left')
    pass
def draw_bottom():
    print('bottom')
    pass
def draw_right():
    print('right')
    pass

def move_rectangle():
    print('rectangle')
    draw_top()
    draw_left()
    draw_bottom()
    draw_right()
    pass

def move_triangle():
    print('triangle')
    pass
while True:
    # move_circle()
    move_rectangle()
    move_triangle()
    pass

close_canvas()