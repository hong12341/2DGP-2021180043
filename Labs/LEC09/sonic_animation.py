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
SPRITE_SHEET_HEIGHT = 525
SPRITE_SCALE = 8
FRAME_DELAY_SECONDS = 0.08
REPEATS_PER_ANIMATION = 5
SPRITE_SHEET_PATH = Path(__file__).with_name("sonic-sprite.png")
FRAME_STRIPS = (
    (39, 39, ((1, 29), (31, 56), (58, 86), (87, 115), (118, 147), (150, 179), (182, 210), (211, 239), (240, 268), (270, 293), (302, 330))),
    (79, 39, ((8, 33), (37, 63), (65, 95), (97, 133), (135, 166), (170, 201), (206, 231), (238, 261), (263, 292), (295, 330), (334, 365), (370, 398))),
    (121, 43, ((1, 33), (39, 73), (89, 123), (130, 163), (181, 214), (228, 260))),
    (167, 33, ((1, 29), (35, 63), (67, 96), (98, 128), (131, 159), (162, 190), (193, 222), (230, 260), (268, 297))),
    (206, 27, ((1, 30), (36, 64), (70, 98), (105, 133), (139, 167), (174, 202))),
    (238, 36, ((1, 29), (36, 65), (74, 104), (111, 141), (149, 178), (186, 216))),
    (283, 35, ((1, 29), (36, 65), (72, 110), (123, 161), (172, 210), (218, 255))),
    (326, 45, ((1, 24), (31, 59), (65, 84), (90, 114), (119, 143), (149, 168), (184, 223), (232, 270))),
    (377, 40, ((1, 27), (31, 61), (64, 94), (99, 131), (136, 167), (176, 208), (217, 249), (254, 286))),
    (426, 43, ((6, 39), (49, 82), (96, 118), (125, 147))),
)


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

    animation_index = 0
    frame_index = 0
    repeats_completed = 0
    running = True

    while running:
        clear_canvas()
        top, height, frames = FRAME_STRIPS[animation_index]
        left, right = frames[frame_index]
        frame_width = right - left + 1
        sprite_sheet.clip_composite_draw(
            left,
            SPRITE_SHEET_HEIGHT - top - height,
            frame_width,
            height,
            0,
            "",
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            frame_width * SPRITE_SCALE,
            height * SPRITE_SCALE,
        )
        update_canvas()

        for event in get_events():
            if event.type == SDL_QUIT:
                running = False

        frame_index += 1
        if frame_index >= len(frames):
            frame_index = 0
            repeats_completed += 1
            if repeats_completed >= REPEATS_PER_ANIMATION:
                repeats_completed = 0
                animation_index = (animation_index + 1) % len(FRAME_STRIPS)
        delay(FRAME_DELAY_SECONDS)

    close_canvas()


if __name__ == "__main__":
    main()