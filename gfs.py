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


def draw_note(screen, rect, is_hit=True):
    if type(rect) == pygame.Rect:
        pygame.draw.rect(screen, (0, 0, 0), rect)
        if not is_hit:
            pygame.draw.rect(screen, (150, 150, 150), rect)
    else:
        if is_hit:
            pygame.draw.polygon(screen, (150, 150, 150), rect)
            pygame.draw.polygon(screen, (0, 0, 0), rect, 2)
        else:
            pygame.draw.polygon(screen, (150, 0, 0), rect)
            pygame.draw.polygon(screen, (255, 0, 0), rect, 2)


def draw_cursor(screen, points):
    pygame.draw.polygon(screen, (0, 0, 0), points)


def get_bottom_notes(note_list):
    bottom_notes = {}
    for note in note_list:
        if note.lane == 5:
            if 5 in bottom_notes:
                if note.time < bottom_notes[note.lane].time:
                    bottom_notes[note.lane] = note
            else:
                bottom_notes[note.lane] = note
        if note.lane in bottom_notes:
            if note.time < bottom_notes[note.lane].time and abs(note.time) < 150:
                bottom_notes[note.lane] = note
        else:
            if abs(note.time) < 150:
                bottom_notes[note.lane] = note
    return bottom_notes


def get_x_in_line(y, line):
    return line[0][0] + (y - line[0][1]) * (line[1][0] - line[0][0]) / (line[1][1] - line[0][1])


def draw_stats(screen, settings):
    font = pygame.font.SysFont(None, 24)

    perfect = font.render("Perfect: " + str(settings.amounts[0]), True, (0, 0, 0))
    good = font.render("Good: " + str(settings.amounts[1]), True, (0, 0, 0))
    bad = font.render("Bad: " + str(settings.amounts[2]), True, (0, 0, 0))
    miss = font.render("Miss: " + str(settings.amounts[3]), True, (0, 0, 0))
    combo = font.render("Combo: " + str(settings.combo), True, (0, 0, 0))

    rect_p = perfect.get_rect()
    rect_p.topleft = (800, 100)
    rect_g = good.get_rect()
    rect_g.topleft = (800, 125)
    rect_b = bad.get_rect()
    rect_b.topleft = (800, 150)
    rect_m = miss.get_rect()
    rect_m.topleft = (800, 175)
    rect_c = combo.get_rect()
    rect_c.topleft = (800, 200)

    screen.blit(perfect, rect_p)
    screen.blit(good, rect_g)
    screen.blit(bad, rect_b)
    screen.blit(miss, rect_m)
    screen.blit(combo, rect_c)


def hold_offset(offset, time):
    if time > offset:
        return -1
    if time < offset - 1:
        return 1
    return 0
