from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('run_animation.png')

FRAME_COUNT = 8
FRAME_WIDTH = 100
FRAME_HEIGHT = 100

frame = 0
x = 0
running = True

while running:
    clear_canvas()

    grass.draw(400, 30)
    character.clip_draw(
        frame * FRAME_WIDTH, 0,
        FRAME_WIDTH, FRAME_HEIGHT,
        x, 90
    )

    update_canvas()

    frame = (frame + 1) % FRAME_COUNT
    x += 5
    if x > 800:
        x = 0

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

    delay(0.05)

close_canvas()

