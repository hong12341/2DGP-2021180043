from pico2d import *
import math

open_canvas()
grass = load_image('grass.png')
character = load_image('character.png')

center_x, center_y = 400, 300
radius = 200
angle = 0.0

while True:
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)

    clear_canvas()
    grass.draw(400, 30)
    character.draw(x, y)
    update_canvas()

    angle += 0.01
    if angle >= 2 * math.pi:
        angle -= 2 * math.pi
    delay(0.01)