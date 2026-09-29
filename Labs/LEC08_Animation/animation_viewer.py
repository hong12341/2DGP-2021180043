import os
import time

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
DEFAULT_HOLD_SECONDS = 1.0

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
EFFECT_Y_OFFSET = 100
EFFECT_X_OFFSET = 50
ANIMATIONS = [WALK_FRAMES, RUN_FRAMES, JUMP_FRAMES, ATTACK_FRAMES, BODY_SLAM_FRAMES]


def draw_frame(frame, center_x, bottom_y, scale):
	source_x, source_top, source_width, source_height = frame
	source_bottom = SHEET_HEIGHT - source_top - source_height
	draw_width = int(source_width * scale)
	draw_height = int(source_height * scale)
	sheet.clip_draw(
		source_x, source_bottom, source_width, source_height,
		center_x, bottom_y + draw_height // 2,
		draw_width, draw_height,
	)


open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
sheet_path = os.path.join(os.path.dirname(__file__), 'pikachu_sprite_sheet.png')
sheet = load_image(sheet_path)
animation_index = 0
active_frames = ANIMATIONS[animation_index]
frame_index = 0
repeats_completed = 0
show_default = True
default_started_at = time.monotonic()
running = True

while running:
	if show_default and time.monotonic() - default_started_at >= DEFAULT_HOLD_SECONDS:
		show_default = False

	clear_canvas()

	if show_default:
		sprite_frame = DEFAULT_STANDING_FRAME
		sprite_x = CHARACTER_X + DEFAULT_X_OFFSET
		jump_height = 0
	else:
		sprite_frame = active_frames[frame_index]
		sprite_x = CHARACTER_X
		jump_height = (0, 30, 45, 0)[frame_index] if animation_index == 2 else 0

	sprite_baseline = DEFAULT_BASELINE_Y if show_default else BASELINE_Y
	draw_frame(sprite_frame, sprite_x, sprite_baseline + jump_height, CHARACTER_SCALE)

	if not show_default and animation_index == 3 and frame_index >= 1:
		draw_frame(
			THUNDER_EFFECT,
			640 + EFFECT_X_OFFSET,
			BASELINE_Y + 210 + EFFECT_Y_OFFSET,
			3.5,
		)

	if not show_default and animation_index == 3 and frame_index == 2:
		draw_frame(
			GROUND_IMPACT_EFFECT,
			640 + EFFECT_X_OFFSET,
			BASELINE_Y + EFFECT_Y_OFFSET,
			3.5,
		)

	update_canvas()
	if not show_default:
		frame_index += 1
		if frame_index >= len(active_frames):
			frame_index = 0
			repeats_completed += 1
			if repeats_completed >= REPEATS_PER_ANIMATION:
				animation_index = (animation_index + 1) % len(ANIMATIONS)
				active_frames = ANIMATIONS[animation_index]
				repeats_completed = 0
				show_default = True
				default_started_at = time.monotonic()

	for event in get_events():
		if event.type == SDL_QUIT:
			running = False
		elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
			running = False

	if show_default:
		remaining = DEFAULT_HOLD_SECONDS - (time.monotonic() - default_started_at)
		delay(min(FRAME_DELAY, max(0.0, remaining)))
	else:
		delay(0.10 if animation_index == 4 else 0.18 if animation_index == 3 else 0.08 if animation_index == 1 else FRAME_DELAY)

close_canvas()
