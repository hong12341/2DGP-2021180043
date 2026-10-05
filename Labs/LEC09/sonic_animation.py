from pathlib import Path

from pico2d import clear_canvas, close_canvas, delay, load_image, open_canvas, update_canvas


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
SPRITE_SHEET_PATH = Path(__file__).with_name("sonic-sprite.png")


def main():
    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    sprite_sheet = load_image(str(SPRITE_SHEET_PATH))

    while True:
        clear_canvas()
        sprite_sheet.draw(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        update_canvas()
        delay(0.01)

    close_canvas()


if __name__ == "__main__":
    main()