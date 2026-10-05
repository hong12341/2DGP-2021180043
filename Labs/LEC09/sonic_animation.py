from pathlib import Path

from pico2d import (
    SDL_QUIT,
    clear_canvas,
    close_canvas,
    delay,
    get_events,
    load_image,
    open_canvas,
    update_canvas,
)


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
SPRITE_SHEET_PATH = Path(__file__).with_name("sonic-sprite.png")


def main():
    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    if not SPRITE_SHEET_PATH.is_file():
        close_canvas()
        raise FileNotFoundError(f"스프라이트 시트를 찾을 수 없습니다: {SPRITE_SHEET_PATH}")

    try:
        sprite_sheet = load_image(str(SPRITE_SHEET_PATH))
    except Exception as error:
        close_canvas()
        raise RuntimeError(f"스프라이트 시트를 읽지 못했습니다: {SPRITE_SHEET_PATH}") from error

    running = True

    while running:
        clear_canvas()
        sprite_sheet.draw(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        update_canvas()

        for event in get_events():
            if event.type == SDL_QUIT:
                running = False

        delay(0.01)

    close_canvas()


if __name__ == "__main__":
    main()