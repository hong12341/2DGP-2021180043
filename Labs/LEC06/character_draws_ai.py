import math
from pico2d import *


# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_DELAY = 0.02

# 출력 메시지
CIRCLE_MESSAGE = 'circle'
RECTANGLE_MESSAGE = 'rectangle'
TRIANGLE_MESSAGE = 'triangle'

# 원 설정
CIRCLE_CENTER = (400, 300)
CIRCLE_RADIUS = 230
CIRCLE_STEP_DEGREES = 5
CIRCLE_FRAME_COUNT = 360 // CIRCLE_STEP_DEGREES
CIRCLE_FRAME_DISTANCE = 2 * CIRCLE_RADIUS * math.sin(
	math.radians(CIRCLE_STEP_DEGREES / 2)
)

# 사각형 꼭짓점
RECTANGLE_POINTS = (
	(150, 500),
	(650, 500),
	(650, 100),
	(150, 100),
	(150, 500),
)

# 삼각형 꼭짓점
TRIANGLE_POINTS = (
	(400, 550),
	(50, 50),
	(750, 50),
	(400, 550),
)


# 게임 화면과 캐릭터 이미지 준비
open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
character = load_image('character.png')
circle_degree = 0


# 화면을 지우고 필요한 그림을 그린 뒤 갱신한다.
def clear_and_update_canvas(draw_action=None):
	clear_canvas()
	if draw_action is not None:
		draw_action()
	update_canvas()


# 현재 좌표에 캐릭터를 그리고 한 프레임을 표시한다.
def draw_character_at(x, y):
	clear_and_update_canvas(lambda: character.draw(x, y))
	delay(FRAME_DELAY)


# 두 점 사이를 원과 같은 속도로 직선 이동한다.
def move_line(start, end):
	start_x, start_y = start
	end_x, end_y = end
	distance = math.hypot(end_x - start_x, end_y - start_y)
	frame_count = max(1, round(distance / CIRCLE_FRAME_DISTANCE))

	for frame in range(frame_count + 1):
		ratio = frame / frame_count
		x = round(start_x + (end_x - start_x) * ratio)
		y = round(start_y + (end_y - start_y) * ratio)
		draw_character_at(x, y)


# 주어진 각도에서 원 위의 좌표를 계산한다.
def get_circle_position(degree):
	theta = math.radians(degree)
	x = CIRCLE_CENTER[0] + CIRCLE_RADIUS * math.cos(theta)
	y = CIRCLE_CENTER[1] + CIRCLE_RADIUS * math.sin(theta)
	return x, y


# 캐릭터를 원 궤도 위에서 시계 방향으로 한 바퀴 이동한다.
def move_circle():
	global circle_degree

	print(CIRCLE_MESSAGE)
	for _ in range(CIRCLE_FRAME_COUNT + 1):
		x, y = get_circle_position(circle_degree)
		draw_character_at(x, y)
		circle_degree = (circle_degree - CIRCLE_STEP_DEGREES) % 360


# 사각형의 네 변을 순서대로 이동한다.
def move_rectangle():
	print(RECTANGLE_MESSAGE)
	for start, end in zip(RECTANGLE_POINTS, RECTANGLE_POINTS[1:]):
		move_line(start, end)
	clear_and_update_canvas()


# 삼각형의 세 변을 순서대로 이동한다.
def move_triangle():
	print(TRIANGLE_MESSAGE)
	for start, end in zip(TRIANGLE_POINTS, TRIANGLE_POINTS[1:]):
		move_line(start, end)


# 원, 사각형, 삼각형을 순서대로 무한 반복한다.
def main():
	while True:
		move_circle()
		move_rectangle()
		move_triangle()


if __name__ == '__main__':
	try:
		main()
	finally:
		close_canvas()
