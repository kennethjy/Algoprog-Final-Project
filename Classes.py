import pygame


class Settings:
    def __init__(self, chart):
        self.file = open(chart, 'r')
        read_chart = False
        for line in self.file.readlines():
            if line.strip() == '':
                read_chart = True
                self.notes = []
                continue
            if not read_chart:
                element = line.strip().split('=')
                if element[0] == "song":
                    self.song_name = element[1]
                if element[0] == "offset":
                    self.offset = int(element[1])
                if element[0] == "bpm":
                    self.bpm = float(element[1])
            else:
                note = line.strip().split(' ')
                if note[1] == "tap":
                    self.notes.append(Tap(int(float(note[0]) * 60000 / self.bpm) + self.offset, int(note[2])))
                if note[1] == "hold":
                    self.notes.append(Hold(int(float(note[0]) * 60000 / self.bpm) + self.offset, int(note[2]), int(float(note[3]) * 60000 / self.bpm), int((float(note[0]) % 1) * 60000 / self.bpm)))
                if note[1] == "arc":
                    self.notes.append(Arc(int(float(note[0]) * 60000 / self.bpm) + self.offset, int(note[2]), int(note[3]), int(float(note[4]) * 60000 / self.bpm)))
        self.file.close()

        self.windowed = (1200, 800)
        self.full_screen = pygame.FULLSCREEN
        self.bg_color = (255, 255, 255)
        self.bg = pygame.rect.Rect(0, 0, self.windowed[0], self.windowed[1])
        self.lanes = (500, [50, 50, 50, 50])
        self.judge_line = 700

        self.amounts = [0, 0, 0, 0]
        self.combo = 0


class Note:
    def __init__(self, time):
        self.time = time

    def update(self, time):
        self.time -= time


class Tap(Note):
    def __init__(self, time, lane):
        super().__init__(time)
        self.lane = lane

    def get_rect(self, settings):
        x_pos = settings.lanes[0]
        for i in range(self.lane - 1):
            x_pos += settings.lanes[1][i]
        rect = pygame.rect.Rect(0, 0, 48, 20)
        rect.midleft = (x_pos + 1, 700 - self.time)
        return rect


class Hold(Note):
    def __init__(self, time, lane, duration, difference_from_beat):
        super().__init__(time)
        self.lane = lane
        self.length = duration
        self.diff = difference_from_beat
        self.is_hit = False

    def get_rect(self, settings):
        x_pos = settings.lanes[0]
        for i in range(self.lane - 1):
            x_pos += settings.lanes[1][i]
        if self.is_hit:
            rect = pygame.rect.Rect(0, 0, 48, 10 + self.length + self.time)
        else:
            rect = pygame.rect.Rect(0, 0, 48, 20 + self.length)
        rect.topleft = (x_pos + 1, 700 - self.time + 10 - self.length)
        return rect


class Arc(Note):
    def __init__(self, time, lane_start, lane_end, duration):
        super().__init__(time)
        self.lane = 5
        self.lane_start = lane_start
        self.lane_end = lane_end
        self.length = duration
        self.is_hit = True

    def get_rect(self, settings):
        x_pos_start = settings.lanes[0]
        for i in range(self.lane_start - 1):
            x_pos_start += settings.lanes[1][i]

        x_pos_end = settings.lanes[0]
        for i in range(self.lane_end - 1):
            x_pos_end += settings.lanes[1][i]

        points = [(x_pos_start - 35, 700 - self.time),
                  (x_pos_start + 35, 700 - self.time),
                  (x_pos_end + 35, 700 - self.time - self.length),
                  (x_pos_end - 35, 700 - self.time - self.length)]
        return points


class Mouse:
    def __init__(self, settings: Settings):
        self.position = settings.lanes[0] + settings.lanes[1][0] + settings.lanes[1][0]
        self.max_left = settings.lanes[0]
        self.max_right = settings.lanes[0] + (settings.lanes[1][0] * 4)

    def move(self, value):
        if self.max_left < self.position + value < self.max_right:
            self.position += value
        else:
            if value < 0:
                self.position = self.max_left + 1
            if value > 0:
                self.position = self.max_right - 1

    def get_rect(self, settings: Settings):
        points = [(self.position, settings.judge_line + 10),
                  (self.position - 15, settings.judge_line + 50),
                  (self.position + 15, settings.judge_line + 50)]
        return points


