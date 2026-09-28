# 도형 경로를 따라 캐릭터를 이동시키는 실습
from pico2d import *
import math

# 게임 화면을 열고 캐릭터 이미지를 준비한다.
open_canvas(800,600)
character = load_image('character.png')

# 캐릭터를 원 궤도 위에서 시계 방향으로 이동시킨다.
def move_circle():
    print('circle')

    # 함수가 다시 호출되어도 이전 각도에서 이어서 시작한다.
    if 'degree' not in globals():
        globals()['degree'] = 0

    # 5도씩 72번 이동하면 원을 한 바퀴 돈다.
    for _ in range(72):
        globals()['degree'] = (globals()['degree'] - 5) % 360
        theta = math.radians(globals()['degree'])

        # 화면 중앙을 중심으로 반지름 230인 원의 좌표를 계산한다.
        x = 400 + 230 * math.cos(theta)
        y = 300 + 230 * math.sin(theta)

        draw_character(x, y)

# 사각형의 위쪽 변을 왼쪽에서 오른쪽으로 이동한다.
def draw_top():
    print('top')
    for x in range(150, 651, 5):
        draw_character(x, 500)

# 전달받은 좌표에 캐릭터를 그리고 한 프레임을 화면에 표시한다.
def draw_character(x, y=550):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.02)

# 사각형의 왼쪽 변을 위에서 아래 방향으로 이동한다.
def draw_left():
    print('left')
    for y in range(500, 99, -5):
        draw_character(650, y)

# 사각형의 아래쪽 변을 오른쪽에서 왼쪽으로 이동한다.
def draw_bottom():
    print('bottom')
    for x in range(650, 149, -5):
        draw_character(x, 100)

# 사각형의 오른쪽 변을 아래에서 위 방향으로 이동한다.
def draw_right():
    print('right')
    for y in range(100, 501, 5):
        draw_character(150, y)

# 네 변을 차례대로 이동시켜 사각형을 그린다.
def move_rectangle():
    print('rectangle')
    draw_top()
    draw_left()
    draw_bottom()
    draw_right()
    clear_canvas()
    update_canvas()

# 세 꼭짓점을 직선으로 연결하며 삼각형을 그린다.
def move_triangle():
    print('triangle')

    # 꼭짓점: 위쪽 -> 왼쪽 아래 -> 오른쪽 아래 -> 위쪽
    points = ((400, 550), (50, 50), (750, 50), (400, 550))

    # 인접한 두 꼭짓점 사이를 순서대로 이동한다.
    for start, end in zip(points, points[1:]):
        start_x, start_y = start
        end_x, end_y = end
        for step in range(101):
            # 비율을 이용해 두 점 사이의 현재 위치를 계산한다.
            ratio = step / 100
            x = round(start_x + (end_x - start_x) * ratio)
            y = round(start_y + (end_y - start_y) * ratio)
            draw_character(x, y)

# 원 -> 사각형 -> 삼각형 순서로 계속 반복한다.
while True:
    move_circle()
    move_rectangle()
    move_triangle()

close_canvas()