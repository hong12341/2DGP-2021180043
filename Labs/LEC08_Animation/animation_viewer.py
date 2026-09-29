import os

from pico2d import *


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
SHEET_HEIGHT = 789
FRAME_DELAY = 0.12
SPRITE_SCALE = 12
BASELINE_Y = 145

# Pixel bounds for the four Pikachu walking poses in pikachu_sprite_sheet.png.
WALK_FRAMES = [
	(26, 80, 37, 31),
	(65, 79, 39, 34),
	(106, 80, 37, 31),
	(149, 78, 32, 35),
]
RUN_FRAMES = [
	(30, 141, 50, 30),
	(89, 144, 51, 23),
	(149, 142, 52, 27),
	(209, 144, 51, 24),
]


open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
sheet_path = os.path.join(os.path.dirname(__file__), 'pikachu_sprite_sheet.png')
sheet = load_image(sheet_path)
active_frames = RUN_FRAMES
frame_index = 0
running = True

while running:
	clear_canvas()

	source_x, source_top, frame_width, frame_height = active_frames[frame_index]
	source_bottom = SHEET_HEIGHT - source_top - frame_height
	draw_width = frame_width * SPRITE_SCALE
	draw_height = frame_height * SPRITE_SCALE
	sheet.clip_draw(
		source_x, source_bottom, frame_width, frame_height,
		CANVAS_WIDTH // 2,
		BASELINE_Y + draw_height // 2,
		draw_width, draw_height,
	)

	update_canvas()
	frame_index = (frame_index + 1) % len(active_frames)

	for event in get_events():
		if event.type == SDL_QUIT:
			running = False
		elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
			running = False
		elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
			active_frames = WALK_FRAMES if active_frames is RUN_FRAMES else RUN_FRAMES
			frame_index = 0

	delay(0.08 if active_frames is RUN_FRAMES else FRAME_DELAY)

close_canvas()
