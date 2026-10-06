from math import hypot
from pathlib import Path
from time import monotonic

from pico2d import (
	SDL_KEYDOWN,
	SDL_KEYUP,
	SDL_QUIT,
	SDLK_DOWN,
	SDLK_ESCAPE,
	SDLK_LEFT,
	SDLK_RIGHT,
	SDLK_UP,
	clear_canvas,
	close_canvas,
	delay,
	get_events,
	load_image,
	open_canvas,
	update_canvas,
)


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MOVE_SPEED = 240
FRAME_WIDTH = 100
FRAME_HEIGHT = 100
FRAME_COUNT = 8
FRAME_INTERVAL = 0.08
CHARACTER_RADIUS_X = 32
CHARACTER_RADIUS_Y = 45
IDLE_RIGHT_ROW_BOTTOM = 302
IDLE_LEFT_ROW_BOTTOM = 202
RUN_RIGHT_ROW_BOTTOM = 102
RUN_LEFT_ROW_BOTTOM = 2
ASSET_DIR = Path(__file__).parent
MOVEMENT_KEYS = {
	SDLK_UP: (0, 1),
	SDLK_DOWN: (0, -1),
	SDLK_LEFT: (-1, 0),
	SDLK_RIGHT: (1, 0),
}


def handle_events(pressed_keys):
	running = True
	for event in get_events():
		if event.type == SDL_QUIT:
			running = False
		elif event.type == SDL_KEYDOWN:
			if event.key == SDLK_ESCAPE:
				running = False
			elif event.key in MOVEMENT_KEYS:
				pressed_keys.add(event.key)
		elif event.type == SDL_KEYUP and event.key in MOVEMENT_KEYS:
			pressed_keys.discard(event.key)
	return running


def draw_character(animation_sheet, x, y, is_moving, frame, facing_left):
	if is_moving:
		source_y = RUN_LEFT_ROW_BOTTOM if facing_left else RUN_RIGHT_ROW_BOTTOM
	else:
		source_y = IDLE_LEFT_ROW_BOTTOM if facing_left else IDLE_RIGHT_ROW_BOTTOM

	animation_sheet.clip_draw(
		frame * FRAME_WIDTH,
		source_y,
		FRAME_WIDTH,
		FRAME_HEIGHT,
		x,
		y,
	)


def main():
	open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
	try:
		animation_sheet = load_image(str(ASSET_DIR / "animation_sheet.png"))
		background = load_image(str(ASSET_DIR / "TUK_GROUND.png"))

		character_x = WINDOW_WIDTH // 2
		character_y = WINDOW_HEIGHT // 2
		pressed_keys = set()
		frame = 0
		animation_elapsed = 0.0
		previous_time = monotonic()
		facing_left = False
		running = True

		while running:
			running = handle_events(pressed_keys)
			current_time = monotonic()
			delta_time = min(current_time - previous_time, 0.05)
			previous_time = current_time

			move_x = sum(MOVEMENT_KEYS[key][0] for key in pressed_keys)
			move_y = sum(MOVEMENT_KEYS[key][1] for key in pressed_keys)
			is_moving = move_x != 0 or move_y != 0

			if is_moving:
				magnitude = hypot(move_x, move_y)
				character_x += move_x / magnitude * MOVE_SPEED * delta_time
				character_y += move_y / magnitude * MOVE_SPEED * delta_time
				if move_x:
					facing_left = move_x < 0

			animation_elapsed += delta_time
			if animation_elapsed >= FRAME_INTERVAL:
				frame = (frame + 1) % FRAME_COUNT
				animation_elapsed %= FRAME_INTERVAL

			character_x = max(CHARACTER_RADIUS_X, min(WINDOW_WIDTH - CHARACTER_RADIUS_X, character_x))
			character_y = max(CHARACTER_RADIUS_Y, min(WINDOW_HEIGHT - CHARACTER_RADIUS_Y, character_y))

			clear_canvas()
			background.draw(
				WINDOW_WIDTH // 2,
				WINDOW_HEIGHT // 2,
				WINDOW_WIDTH,
				WINDOW_HEIGHT,
			)
			draw_character(
				animation_sheet,
				character_x,
				character_y,
				is_moving,
				frame,
				facing_left,
			)
			update_canvas()
			delay(0.01)
	finally:
		close_canvas()


if __name__ == "__main__":
	main()
