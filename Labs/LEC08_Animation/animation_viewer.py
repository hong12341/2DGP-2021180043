import os
import time

from pico2d import *


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
# 스프라이트 시트 전체 크기와 프레임 사이의 기본 간격
SHEET_HEIGHT = 789
FRAME_DELAY = 0.12
# 캐릭터의 화면 위치, 크기, 바닥 높이
CHARACTER_X = 380
DEFAULT_X_OFFSET = -100
CHARACTER_SCALE = 12
BASELINE_Y = 0
DEFAULT_BASELINE_Y = -100
# 각 동작을 반복할 횟수와 기본 자세를 유지할 시간
REPEATS_PER_ANIMATION = 5
DEFAULT_HOLD_SECONDS = 1.0

# 각 프레임 좌표는 (시트 왼쪽, 위쪽, 너비, 높이) 순서
# 걷기 동작의 프레임 좌표
WALK_FRAMES = [
	(26, 80, 37, 31),
	(65, 79, 39, 34),
	(106, 80, 37, 31),
	(149, 78, 32, 35),
]
# 동작 사이에 보여 줄 기본 서기 프레임
DEFAULT_STANDING_FRAME = (20, 17, 43, 45)
# 달리기 동작의 프레임 좌표
RUN_FRAMES = [
	(30, 141, 50, 30),
	(89, 144, 51, 23),
	(149, 142, 52, 27),
	(209, 144, 51, 24),
]
# 점프 동작의 프레임 좌표
JUMP_FRAMES = [
	(25, 379, 39, 51),
	(65, 386, 41, 29),
	(110, 379, 29, 43),
	(143, 386, 43, 29),
]
# 번개 공격 동작의 피카츄 프레임 좌표
ATTACK_FRAMES = [
	(21, 500, 44, 42),
	(67, 500, 35, 42),
	(110, 501, 34, 40),
]
# 몸통박치기 동작의 프레임 좌표
BODY_SLAM_FRAMES = [
	(20, 321, 64, 30),
	(86, 321, 54, 29),
	(149, 321, 51, 30),
	(209, 321, 52, 29),
]
# 파이터 스탠스 동작의 프레임 좌표
FIGHTER_STANCE_FRAMES = [
	(27, 561, 46, 39),
	(77, 562, 46, 38),
	(126, 562, 47, 38),
	(176, 561, 47, 39),
]
# 번개 공격에 사용할 이펙트 프레임과 화면상 위치 조정값
THUNDER_EFFECT = (324, 584, 62, 56)
GROUND_IMPACT_EFFECT = (315, 625, 90, 60)
EFFECT_Y_OFFSET = 100
EFFECT_X_OFFSET = 50
# 자동 재생할 애니메이션 순서
ANIMATIONS = [
	WALK_FRAMES,
	RUN_FRAMES,
	JUMP_FRAMES,
	ATTACK_FRAMES,
	BODY_SLAM_FRAMES,
	FIGHTER_STANCE_FRAMES,
]


# 프레임을 시트에서 잘라 지정한 위치와 크기로 그린다.
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


# 캔버스와 스프라이트 시트를 준비한다.
open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
sheet_path = os.path.join(os.path.dirname(__file__), 'pikachu_sprite_sheet.png')
sheet = load_image(sheet_path)
# 현재 애니메이션, 프레임, 반복 횟수와 기본 자세 대기 시간을 초기화한다.
animation_index = 0
active_frames = ANIMATIONS[animation_index]
frame_index = 0
repeats_completed = 0
show_default = True
default_started_at = time.monotonic()
running = True

# 기본 자세와 여섯 애니메이션을 순서대로 계속 재생한다.
while running:
	# 기본 자세를 1초 보여 준 뒤 다음 동작으로 넘어간다.
	if show_default and time.monotonic() - default_started_at >= DEFAULT_HOLD_SECONDS:
		show_default = False

	clear_canvas()

	# 현재 상태에 맞는 프레임과 캐릭터 위치를 선택한다.
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

	# 번개 공격 프레임에는 번개 기둥을 함께 그린다.
	if not show_default and animation_index == 3 and frame_index >= 1:
		draw_frame(
			THUNDER_EFFECT,
			640 + EFFECT_X_OFFSET,
			BASELINE_Y + 210 + EFFECT_Y_OFFSET,
			3.5,
		)

	# 번개 공격 마지막 프레임에는 지면 타격 이펙트를 추가한다.
	if not show_default and animation_index == 3 and frame_index == 2:
		draw_frame(
			GROUND_IMPACT_EFFECT,
			640 + EFFECT_X_OFFSET,
			BASELINE_Y + EFFECT_Y_OFFSET,
			3.5,
		)

	update_canvas()
	# 프레임을 진행하고 동작을 다섯 번 재생하면 다음 동작으로 바꾼다.
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

	# 창 닫기 또는 ESC 입력으로 프로그램을 종료한다.
	for event in get_events():
		if event.type == SDL_QUIT:
			running = False
		elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
			running = False

	# 기본 자세는 남은 시간만큼 기다리고, 애니메이션은 동작별 속도로 재생한다.
	if show_default:
		remaining = DEFAULT_HOLD_SECONDS - (time.monotonic() - default_started_at)
		delay(min(FRAME_DELAY, max(0.0, remaining)))
	else:
		delay(0.10 if animation_index == 4 else 0.18 if animation_index == 3 else 0.08 if animation_index == 1 else FRAME_DELAY)

# 사용이 끝난 캔버스를 닫는다.
close_canvas()
