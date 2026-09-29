import os

from pico2d import *


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
SHEET_HEIGHT = 789
FRAME_DELAY = 0.12
CHARACTER_X = 380
DEFAULT_X_OFFSET = -100
CHARACTER_SCALE = 12
BASELINE_Y = 0
DEFAULT_BASELINE_Y = -100
REPEATS_PER_ANIMATION = 5
DEFAULT_HOLD_FRAMES = round(1.0 / FRAME_DELAY)

# Pixel bounds for the four Pikachu walking poses in pikachu_sprite_sheet.png.
WALK_FRAMES = [
	(26, 80, 37, 31),
	(65, 79, 39, 34),
	(106, 80, 37, 31),
	(149, 78, 32, 35),
]
DEFAULT_STANDING_FRAME = (20, 17, 43, 45)
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
BODY_SLAM_FRAMES = [
	(20, 321, 64, 44),
	(86, 321, 54, 44),
	(149, 321, 51, 30),
	(209, 321, 52, 29),
]
THUNDER_EFFECT = (324, 584, 62, 56)
GROUND_IMPACT_EFFECT = (315, 625, 90, 60)
ANIMATIONS = [WALK_FRAMES, RUN_FRAMES, JUMP_FRAMES, ATTACK_FRAMES, BODY_SLAM_FRAMES]


open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
sheet_path = os.path.join(os.path.dirname(__file__), 'pikachu_sprite_sheet.png')
sheet = load_image(sheet_path)
animation_index = 0
active_frames = ANIMATIONS[animation_index]
frame_index = 0
repeats_completed = 0
show_default = True
default_frames_remaining = DEFAULT_HOLD_FRAMES
running = True

while running:
	clear_canvas()

	if show_default:
		source_x, source_top, frame_width, frame_height = DEFAULT_STANDING_FRAME
		sprite_x = CHARACTER_X + DEFAULT_X_OFFSET
		jump_height = 0
	else:
		source_x, source_top, frame_width, frame_height = active_frames[frame_index]
		sprite_x = CHARACTER_X
		jump_height = (0, 30, 45, 0)[frame_index] if animation_index == 2 else 0

	source_bottom = SHEET_HEIGHT - source_top - frame_height
	draw_width = frame_width * CHARACTER_SCALE
	draw_height = frame_height * CHARACTER_SCALE
	sprite_baseline = DEFAULT_BASELINE_Y if show_default else BASELINE_Y
	sheet.clip_draw(
		source_x, source_bottom, frame_width, frame_height,
		sprite_x,
		sprite_baseline + jump_height + draw_height // 2,
		draw_width, draw_height,
	)

	if not show_default and animation_index == 3 and frame_index >= 1:
		effect_x, effect_top, effect_width, effect_height = THUNDER_EFFECT
		effect_bottom = SHEET_HEIGHT - effect_top - effect_height
		effect_scale = 3.5
		beam_width = int(effect_width * effect_scale)
		beam_height = int(effect_height * effect_scale)
		sheet.clip_draw(
			effect_x, effect_bottom, effect_width, effect_height,
			640, BASELINE_Y + 210 + beam_height // 2,
			beam_width, beam_height,
		)

	if not show_default and animation_index == 3 and frame_index == 2:
		impact_x, impact_top, impact_width, impact_height = GROUND_IMPACT_EFFECT
		impact_bottom = SHEET_HEIGHT - impact_top - impact_height
		impact_scale = 3.5
		sheet.clip_draw(
			impact_x, impact_bottom, impact_width, impact_height,
			640, BASELINE_Y + int(impact_height * impact_scale) // 2,
			int(impact_width * impact_scale), int(impact_height * impact_scale),
		)

	update_canvas()
	if show_default:
		default_frames_remaining -= 1
		if default_frames_remaining <= 0:
			show_default = False
	else:
		frame_index += 1
		if frame_index >= len(active_frames):
			frame_index = 0
			repeats_completed += 1
			if repeats_completed >= REPEATS_PER_ANIMATION:
				animation_index = (animation_index + 1) % len(ANIMATIONS)
				active_frames = ANIMATIONS[animation_index]
				repeats_completed = 0
				show_default = True
				default_frames_remaining = DEFAULT_HOLD_FRAMES

	for event in get_events():
		if event.type == SDL_QUIT:
			running = False
		elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
			running = False

	if show_default:
		delay(FRAME_DELAY)
	else:
		delay(0.10 if animation_index == 4 else 0.18 if animation_index == 3 else 0.08 if animation_index == 1 else FRAME_DELAY)

close_canvas()
