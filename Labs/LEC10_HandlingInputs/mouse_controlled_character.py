from pathlib import Path

from pico2d import (
    SDL_KEYDOWN,
    SDL_MOUSEMOTION,
    SDL_QUIT,
    SDLK_ESCAPE,
    close_canvas,
    clear_canvas,
    delay,
    get_events,
    hide_cursor,
    load_image,
    open_canvas,
    update_canvas,
)


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 1024
FRAME_WIDTH = 100
FRAME_HEIGHT = 100
FRAME_COUNT = 8
FRAME_DELAY_SECONDS = 0.05
ASSET_DIR = Path(__file__).parent


def main():
    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    try:
        ground = load_image(str(ASSET_DIR / "TUK_GROUND.png"))
        character = load_image(str(ASSET_DIR / "animation_sheet.png"))
        hide_cursor()

        character_x = WINDOW_WIDTH // 2
        character_y = WINDOW_HEIGHT // 2
        frame_index = 0
        running = True

        while running:
            for event in get_events():
                if event.type == SDL_QUIT:
                    running = False
                elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                    running = False
                elif event.type == SDL_MOUSEMOTION:
                    character_x = event.x
                    character_y = WINDOW_HEIGHT - 1 - event.y

            clear_canvas()
            ground.draw(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            character.clip_draw(
                frame_index * FRAME_WIDTH,
                FRAME_HEIGHT,
                FRAME_WIDTH,
                FRAME_HEIGHT,
                character_x,
                character_y,
            )
            update_canvas()

            frame_index = (frame_index + 1) % FRAME_COUNT
            delay(FRAME_DELAY_SECONDS)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()