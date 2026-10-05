from pathlib import Path
from time import monotonic
from dataclasses import dataclass
from typing import NamedTuple

from pico2d import (
    SDL_QUIT,
    SDL_KEYDOWN,
    SDLK_ESCAPE,
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
ANIMATION_PAUSE_SECONDS = 1.0
SPRITE_SHEET_PATH = Path(__file__).with_name("sonic-sprite.png")


class AnimationStrip(NamedTuple):
    name: str
    top: int
    height: int
    frames: tuple[tuple[int, int], ...]


@dataclass
class PlaybackState:
    animation_index: int = 0
    frame_index: int = 0
    repeats_completed: int = 0
    pause_started_at: float | None = None


FRAME_STRIPS = tuple(AnimationStrip(*strip) for strip in (
    ("애니메이션 1", 39, 39, ((1, 29), (31, 56), (58, 86), (87, 115), (118, 147), (150, 179), (182, 210), (211, 239), (240, 268), (270, 293), (302, 330))),
    ("애니메이션 2", 79, 39, ((8, 33), (37, 63), (65, 95), (97, 133), (135, 166), (170, 201), (206, 231), (238, 261), (263, 292), (295, 330), (334, 365), (370, 398))),
    ("애니메이션 3", 121, 43, ((1, 33), (39, 73), (89, 123), (130, 163), (181, 214), (228, 260))),
    ("애니메이션 4", 167, 33, ((1, 29), (35, 63), (67, 96), (98, 128), (131, 159), (162, 190), (193, 222), (230, 260), (268, 297))),
    ("애니메이션 5", 206, 27, ((1, 30), (36, 64), (70, 98), (105, 133), (139, 167), (174, 202))),
    ("애니메이션 6", 238, 36, ((1, 29), (36, 65), (74, 104), (111, 141), (149, 178), (186, 216))),
    ("애니메이션 7", 283, 35, ((1, 29), (36, 65), (72, 110), (123, 161), (172, 210), (218, 255))),
    ("애니메이션 8", 326, 45, ((1, 24), (31, 59), (65, 84), (90, 114), (119, 143), (149, 168), (184, 223), (232, 270))),
    ("애니메이션 9", 377, 40, ((1, 27), (31, 61), (64, 94), (99, 131), (136, 167), (176, 208), (217, 249), (254, 286))),
    ("애니메이션 10", 426, 43, ((6, 39), (49, 82), (96, 118), (125, 147))),
))


def draw_frame(sprite_sheet, animation_index, frame_index):
    animation = FRAME_STRIPS[animation_index]
    left, right = animation.frames[frame_index]
    frame_width = right - left + 1
    sprite_sheet.clip_composite_draw(
        left,
        SPRITE_SHEET_HEIGHT - animation.top - animation.height,
        frame_width,
        animation.height,
        0,
        "",
        WINDOW_WIDTH // 2,
        WINDOW_HEIGHT // 2,
        frame_width * SPRITE_SCALE,
        animation.height * SPRITE_SCALE,
    )


def advance_playback(state, current_time):
    if state.pause_started_at is not None:
        if current_time - state.pause_started_at >= ANIMATION_PAUSE_SECONDS:
            state.animation_index = (state.animation_index + 1) % len(FRAME_STRIPS)
            state.frame_index = 0
            state.repeats_completed = 0
            state.pause_started_at = None
        return

    frames = FRAME_STRIPS[state.animation_index].frames
    state.frame_index += 1
    if state.frame_index < len(frames):
        return

    state.repeats_completed += 1
    if state.repeats_completed >= REPEATS_PER_ANIMATION:
        state.frame_index = len(frames) - 1
        state.pause_started_at = current_time
    else:
        state.frame_index = 0


def main():
    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    try:
        if not SPRITE_SHEET_PATH.is_file():
            raise FileNotFoundError(f"스프라이트 시트를 찾을 수 없습니다: {SPRITE_SHEET_PATH}")

        try:
            sprite_sheet = load_image(str(SPRITE_SHEET_PATH))
        except Exception as error:
            raise RuntimeError(f"스프라이트 시트를 읽지 못했습니다: {SPRITE_SHEET_PATH}") from error

        state = PlaybackState()
        running = True

        while running:
            clear_canvas()
            draw_frame(sprite_sheet, state.animation_index, state.frame_index)
            update_canvas()

            for event in get_events():
                if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
                    running = False

            advance_playback(state, monotonic())
            delay(FRAME_DELAY_SECONDS)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()