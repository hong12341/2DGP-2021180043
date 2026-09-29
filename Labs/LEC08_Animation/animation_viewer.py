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
JUMP_FRAMES = [
	(25, 379, 39, 51),
	(65, 386, 41, 29),
	(110, 379, 29, 43),
	(143, 386, 43, 29),
]
ATTACK_FRAMES = [
	(21, 500, 44, 50),
	(67, 500, 43, 42),
	(110, 501, 34, 40),
]
THUNDER_EFFECT = (324, 584, 62, 56)
GROUND_IMPACT_EFFECT = (315, 625, 90, 60)
ANIMATIONS = [WALK_FRAMES, RUN_FRAMES, JUMP_FRAMES, ATTACK_FRAMES]


open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
sheet_path = os.path.join(os.path.dirname(__file__), 'pikachu_sprite_sheet.png')
sheet = load_image(sheet_path)
animation_index = 3
active_frames = ANIMATIONS[animation_index]
frame_index = 0
running = True

while running:
	clear_canvas()

	source_x, source_top, frame_width, frame_height = active_frames[frame_index]
	source_bottom = SHEET_HEIGHT - source_top - frame_height
	draw_scale = 8 if animation_index in (2, 3) else SPRITE_SCALE
	draw_width = frame_width * draw_scale
	draw_height = frame_height * draw_scale
	jump_height = (0, 30, 45, 15)[frame_index] if animation_index == 2 else 0
	sheet.clip_draw(
		source_x, source_bottom, frame_width, frame_height,
		250 if animation_index == 3 else CANVAS_WIDTH // 2,
		BASELINE_Y + jump_height + draw_height // 2,
		draw_width, draw_height,
	)

	if animation_index == 3 and frame_index >= 1:
		effect_x, effect_top, effect_width, effect_height = THUNDER_EFFECT
		effect_bottom = SHEET_HEIGHT - effect_top - effect_height
		effect_scale = 3.5
		beam_width = int(effect_width * effect_scale)
		beam_height = int(effect_height * effect_scale)
		sheet.clip_draw(
			effect_x, effect_bottom, effect_width, effect_height,
			565, BASELINE_Y + 210 + beam_height // 2,
			beam_width, beam_height,
		)

	if animation_index == 3 and frame_index == 2:
		impact_x, impact_top, impact_width, impact_height = GROUND_IMPACT_EFFECT
		impact_bottom = SHEET_HEIGHT - impact_top - impact_height
		impact_scale = 3.5
		sheet.clip_draw(
			impact_x, impact_bottom, impact_width, impact_height,
			565, BASELINE_Y + int(impact_height * impact_scale) // 2,
			int(impact_width * impact_scale), int(impact_height * impact_scale),
		)

	update_canvas()
	frame_index = (frame_index + 1) % len(active_frames)

	for event in get_events():
		if event.type == SDL_QUIT:
			running = False
		elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
			running = False
		elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
			animation_index = (animation_index + 1) % len(ANIMATIONS)
			active_frames = ANIMATIONS[animation_index]
			frame_index = 0

	delay(0.18 if animation_index == 3 else 0.08 if animation_index == 1 else FRAME_DELAY)

close_canvas()
