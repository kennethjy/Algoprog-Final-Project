import pygame
pygame.init()


def draw_lane(x, screen):
    pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, screen.get_rect().bottom), 2)


def draw_lanes(settings, screen):
    lanes = settings.lanes
    current_x = lanes[0]
    draw_lane(current_x, screen)
    for line in lanes[1]:
        current_x += line
        draw_lane(current_x, screen)
    pygame.draw.line(screen, (0, 0, 0), (settings.lanes[0], settings.judge_line), (current_x, settings.judge_line), 2)


def draw_note(screen, rect):
    if type(rect) == pygame.Rect:
        pygame.draw.rect(screen, (0, 0, 0), rect)
    else:
        pygame.draw.polygon(screen, (150, 150, 150), rect)
        pygame.draw.polygon(screen, (0, 0, 0), rect, 2)


def get_bottom_notes(note_list):
    bottom_notes = {}
    for note in note_list:
        if note.lane in bottom_notes:
            if note.time < bottom_notes[note.lane].time and abs(note.time) < 150:
                bottom_notes[note.lane] = note
        else:
            if abs(note.time) < 150:
                bottom_notes[note.lane] = note
    return bottom_notes
