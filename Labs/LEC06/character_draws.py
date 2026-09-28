# 실습 과제 진행
from pico2d import *
import math
# 맨처음 해야할 일
open_canvas(800,600)
character = load_image('character.png')

def move_circle():
    if 'degree' not in globals():
        globals()['degree'] = 0

    globals()['degree'] = (globals()['degree'] + 5) % 360
    theta = math.radians(globals()['degree'])
    x = 400 + 200 * math.cos(theta)
    y = 300 + 200 * math.sin(theta)

    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.02)

def draw_top():
    for y in range(300, 500, 5):
        clear_canvas()
        character.draw(400, y)
        update_canvas()
        delay(0.02)
def draw_left():
    for x in range(400, 200, -5):
        clear_canvas()
        character.draw(x, 500)
        update_canvas()
        delay(0.02)
def draw_bottom():
    for y in range(500, 300, -5):
        clear_canvas()
        character.draw(200, y)
        update_canvas()
        delay(0.02)
def draw_right():
    for x in range(200, 400, 5):
        clear_canvas()
        character.draw(x, 300)
        update_canvas()
        delay(0.02)
        
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
    move_circle()
    move_rectangle()
    move_triangle()
    pass

close_canvas()