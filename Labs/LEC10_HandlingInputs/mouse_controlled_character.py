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
WALKING_ROW_BOTTOM = 302
CHARACTER_WIDTH = 42
CHARACTER_HEIGHT = 92
CHARACTER_RADIUS_X = 32
CHARACTER_RADIUS_Y = 45
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


def draw_character(idle_image, walking_sheet, x, y, is_moving, frame, facing_left):
	if is_moving:
		walking_sheet.clip_composite_draw(
			frame * FRAME_WIDTH,
			WALKING_ROW_BOTTOM,
			FRAME_WIDTH,
			FRAME_HEIGHT,
			0,
			"h" if facing_left else "",
			x,
			y,
			FRAME_WIDTH,
			FRAME_HEIGHT,
		)
	else:
		idle_image.clip_composite_draw(
			0,
			0,
			CHARACTER_WIDTH,
			CHARACTER_HEIGHT,
			0,
			"h" if facing_left else "",
			x,
			y,
			CHARACTER_WIDTH,
			CHARACTER_HEIGHT,
		)


def main():
	open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
	try:
		idle_image = load_image(str(ASSET_DIR / "character.png"))
		walking_sheet = load_image(str(ASSET_DIR / "animation_sheet.png"))
		ground = load_image(str(ASSET_DIR / "grass.png"))

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
				animation_elapsed += delta_time
				if move_x:
					facing_left = move_x < 0
				if animation_elapsed >= FRAME_INTERVAL:
					frame = (frame + 1) % FRAME_COUNT
					animation_elapsed %= FRAME_INTERVAL
			else:
				frame = 0
				animation_elapsed = 0.0

			character_x = max(CHARACTER_RADIUS_X, min(WINDOW_WIDTH - CHARACTER_RADIUS_X, character_x))
			character_y = max(CHARACTER_RADIUS_Y, min(WINDOW_HEIGHT - CHARACTER_RADIUS_Y, character_y))

			clear_canvas()
			ground.draw(WINDOW_WIDTH // 2, 30)
			draw_character(
				idle_image,
				walking_sheet,
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
