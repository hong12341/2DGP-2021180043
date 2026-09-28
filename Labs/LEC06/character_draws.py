# 도형 경로를 따라 캐릭터를 이동시키는 실습
import math
from pico2d import *

# 화면 크기
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_DELAY = 0.02

# 원의 중심과 크기
CIRCLE_CENTER = (400, 300)
CIRCLE_RADIUS = 230
CIRCLE_STEP_DEGREES = 5
CIRCLE_FRAME_COUNT = 360 // CIRCLE_STEP_DEGREES
CIRCLE_FRAME_DISTANCE = 2 * CIRCLE_RADIUS * math.sin(math.radians(CIRCLE_STEP_DEGREES / 2))

# 사각형의 경계 좌표
RECTANGLE_LEFT = 150
RECTANGLE_RIGHT = 650
RECTANGLE_TOP = 500
RECTANGLE_BOTTOM = 100

# 삼각형의 꼭짓점
TRIANGLE_TOP = (400, 550)
TRIANGLE_LEFT = (50, 50)
TRIANGLE_RIGHT = (750, 50)

# 게임 화면을 열고 캐릭터 이미지를 준비한다.
open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
character = load_image('character.png')
degree = 0

# 공통 함수
# 화면을 지우고 갱신한다.
def clear_and_update_canvas():
    clear_canvas()
    update_canvas()

# 전달받은 좌표에 캐릭터를 그리고 한 프레임을 화면에 표시한다.
def draw_character_at(x, y=550):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(FRAME_DELAY)

# 원과 같은 속도로 두 점 사이를 직선 이동한다.
def move_line(start, end):
    start_x, start_y = start
    end_x, end_y = end
    distance = math.hypot(end_x - start_x, end_y - start_y)
    steps = max(1, round(distance / CIRCLE_FRAME_DISTANCE))

    for step in range(steps + 1):
        ratio = step / steps
        x = round(start_x + (end_x - start_x) * ratio)
        y = round(start_y + (end_y - start_y) * ratio)
        draw_character_at(x, y)

# 원 이동 함수
# 캐릭터를 원 궤도 위에서 시계 방향으로 이동시킨다.
def move_circle():
    print('circle')

    # 함수가 다시 호출되어도 이전 각도에서 이어서 시작한다.
    global degree

    # 일정한 각도만큼 이동하며 원을 한 바퀴 돈다.
    for _ in range(CIRCLE_FRAME_COUNT):
        degree = (degree - CIRCLE_STEP_DEGREES) % 360
        theta = math.radians(degree)

        # 원의 중심과 반지름을 사용해 현재 좌표를 계산한다.
        x = CIRCLE_CENTER[0] + CIRCLE_RADIUS * math.cos(theta)
        y = CIRCLE_CENTER[1] + CIRCLE_RADIUS * math.sin(theta)

        draw_character_at(x, y)

# 사각형 이동 함수
# 사각형의 위쪽 변을 왼쪽에서 오른쪽으로 이동한다.
def move_rectangle_top():
    move_line((RECTANGLE_LEFT, RECTANGLE_TOP), (RECTANGLE_RIGHT, RECTANGLE_TOP))

# 사각형의 왼쪽 변을 위에서 아래 방향으로 이동한다.
def move_rectangle_left():
    move_line((RECTANGLE_RIGHT, RECTANGLE_TOP), (RECTANGLE_RIGHT, RECTANGLE_BOTTOM))

# 사각형의 아래쪽 변을 오른쪽에서 왼쪽으로 이동한다.
def move_rectangle_bottom():
    move_line((RECTANGLE_RIGHT, RECTANGLE_BOTTOM), (RECTANGLE_LEFT, RECTANGLE_BOTTOM))

# 사각형의 오른쪽 변을 아래에서 위 방향으로 이동한다.
def move_rectangle_right():
    move_line((RECTANGLE_LEFT, RECTANGLE_BOTTOM), (RECTANGLE_LEFT, RECTANGLE_TOP))

# 네 변을 차례대로 이동시켜 사각형을 그린다.
def move_rectangle():
    print('rectangle')
    move_rectangle_top()
    move_rectangle_left()
    move_rectangle_bottom()
    move_rectangle_right()
    clear_and_update_canvas()

# 삼각형 이동 함수
# 세 꼭짓점을 직선으로 연결하며 삼각형을 그린다.
def move_triangle():
    print('triangle')

    # 꼭짓점: 위쪽 -> 왼쪽 아래 -> 오른쪽 아래 -> 위쪽
    points = (TRIANGLE_TOP, TRIANGLE_LEFT, TRIANGLE_RIGHT, TRIANGLE_TOP)

    # 인접한 두 꼭짓점 사이를 순서대로 이동한다.
    for start, end in zip(points, points[1:]):
        move_line(start, end)

# 전체 실행부
# 1. 원을 한 바퀴 이동한다.
# 2. 사각형의 네 변을 순서대로 이동한다.
# 3. 삼각형의 세 변을 순서대로 이동한다.
# 삼각형까지 끝나면 다시 1번으로 돌아가 계속 반복한다.
while True:
    move_circle()
    move_rectangle()
    move_triangle()

close_canvas()