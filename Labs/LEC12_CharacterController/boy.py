import os

from pico2d import get_time, load_image
from transitions import Machine

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.frame_duration = 0.1
        self.last_frame_time = get_time()
        image_path = os.path.join(os.path.dirname(__file__), 'animation_sheet.png')
        self.image = load_image(image_path)
        self.machine = Machine(model=self, states=['idle'], initial='idle')

    def update(self):
        if self.state == 'idle':
            self.update_idle()

    def update_idle(self):
        now = get_time()
        elapsed_frames = int((now - self.last_frame_time) / self.frame_duration)
        if elapsed_frames:
            self.frame = (self.frame + elapsed_frames) % 8
            self.last_frame_time += elapsed_frames * self.frame_duration

    def draw(self):
        if self.face_dir == 1:
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)
