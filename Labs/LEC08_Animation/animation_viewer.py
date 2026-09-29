import os

from pico2d import *


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
FRAME_DELAY = 0.12
SPRITE_SCALE = 10
BASELINE_Y = 145

# Pixel bounds for the four Pikachu walking poses in pikachu_sprite_sheet.png.
WALK_FRAMES = [
	(26, 80, 37, 31),
	(65, 79, 39, 34),
	(106, 80, 37, 31),
	(149, 78, 32, 35),
]


open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
sheet_path = os.path.join(os.path.dirname(__file__), 'pikachu_sprite_sheet.png')
sheet = load_image(sheet_path)
frame_index = 0
running = True

while running:
	clear_canvas()

	source_x, source_y, frame_width, frame_height = WALK_FRAMES[frame_index]
	draw_width = frame_width * SPRITE_SCALE
	draw_height = frame_height * SPRITE_SCALE
	sheet.clip_draw(
		source_x, source_y, frame_width, frame_height,
		CANVAS_WIDTH // 2,
		BASELINE_Y + draw_height // 2,
		draw_width, draw_height,
	)

	update_canvas()
	frame_index = (frame_index + 1) % len(WALK_FRAMES)

	for event in get_events():
		if event.type == SDL_QUIT:
			running = False
		elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
			running = False

	delay(FRAME_DELAY)

close_canvas()
