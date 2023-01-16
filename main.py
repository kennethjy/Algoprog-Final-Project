import pygame
from Classes import Settings, Tap, Hold, Arc, Mouse
import gfs

# initializing pygame and classes
pygame.display.init()
pygame.init()
settings = Settings("chart.txt")
screen = pygame.display.set_mode(settings.windowed)
mouse = Mouse(settings)


# initializing values
run = True
pygame.mixer.init()
song = pygame.mixer.Sound("Chronomia.mp3")
tap = pygame.mixer.Sound("tap.wav")
to_draw = []
held = []
holds = []
beat_no = 0


def main():
    global run, beat_no
    # playing the song, setting previous time to 0, locking all inputs to the program when selected
    song.play()
    prev = 0
    pygame.event.set_grab(True)

    while run:
        # setting array to keep track of keydown events
        pressed_lanes = [False for _ in range(4)]

        for event in pygame.event.get():
            # code to end program when window is closed
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                break

            # code to check for inputs. controls are F,G,H,and K. Esc brings up the pause menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    pressed_lanes[0] = True
                if event.key == pygame.K_g:
                    pressed_lanes[1] = True
                if event.key == pygame.K_h:
                    pressed_lanes[2] = True
                if event.key == pygame.K_j:
                    pressed_lanes[3] = True
                if event.key == pygame.K_ESCAPE:
                    prev = menu(prev)
                    if run:
                        pygame.event.set_grab(True)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_f:
                    for i in held:
                        if i.lane == 1:
                            held.remove(i)
                            i.is_hit = False
                if event.key == pygame.K_g:
                    for i in held:
                        if i.lane == 2:
                            held.remove(i)
                            i.is_hit = False
                if event.key == pygame.K_h:
                    for i in held:
                        if i.lane == 3:
                            held.remove(i)
                            i.is_hit = False
                if event.key == pygame.K_j:
                    for i in held:
                        if i.lane == 4:
                            held.remove(i)
                            i.is_hit = False
        # immediately ends the program if run is set to false
        if not run:
            break

        # code to check for tapped notes if a keydown event is detected
        notes: dict = gfs.get_bottom_notes(to_draw)
        if True in pressed_lanes:
            for lane in range(4):
                if pressed_lanes[lane]:
                    if notes.get(lane + 1):
                        if type(notes[lane + 1]) == Tap:
                            tap.stop()
                            tap.play()
                            to_draw.remove(notes[lane + 1])
                            if abs(notes[lane + 1].time) <= 50:
                                settings.amounts[0] += 1
                                settings.combo += 1
                            elif abs(notes[lane + 1].time) <= 100:
                                settings.amounts[1] += 1
                                settings.combo += 1
                            else:
                                settings.amounts[2] += 1
                                settings.combo = 0
                        if type(notes[lane + 1]) == Hold:
                            tap.stop()
                            tap.play()
                            notes[lane + 1].is_hit = True
                            held.append(notes[lane + 1])
                            holds.append(notes[lane + 1])
                            if abs(notes[lane + 1].time) <= 50:
                                settings.amounts[0] += 1
                                settings.combo += 1
                            elif abs(notes[lane + 1].time) <= 100:
                                settings.amounts[1] += 1
                                settings.combo += 1
                            else:
                                settings.amounts[2] += 1
                                settings.combo = 0

        # code to append hold notes into holds
        for lane in range(4):
            if notes.get(lane + 1):
                if type(notes[lane + 1]) == Hold and notes[lane + 1].time < 0:
                    if notes[lane + 1] not in holds:
                        holds.append(notes[lane + 1])

        # code to check mouse position for arcs
        if notes.get(5):
            if notes[5] not in holds:
                holds.append(notes[5])
            points = notes[5].get_rect(settings)
            if points[0][1] >= settings.judge_line + 10 >= points[3][1]:
                left = gfs.get_x_in_line(settings.judge_line + 10, [points[0], points[3]])
                right = gfs.get_x_in_line(settings.judge_line + 10, [points[1], points[2]])
                if left - 25 <= mouse.position <= right + 25:
                    notes[5].is_hit = True
                    if notes[5] not in held:
                        held.append(notes[5])
                else:
                    notes[5].is_hit = False
                    if notes[5] in held:
                        held.remove(notes[5])

        # filling screen with white background
        screen.fill((255, 255, 255))

        # calculate time between this frame and the previous frame
        current = pygame.time.get_ticks()
        diff = current - prev
        prev = pygame.time.get_ticks()

        if current > beat_no * 60000 / settings.bpm:
            beat_no += 1
            settings.amounts[0] += len(held)
            settings.combo += len(held)
            settings.amounts[3] += len(holds) - len(held)
            if len(holds) > len(held):
                settings.combo = 0

        # moving arc catcher (square at the bottom of the screen)
        x, y = pygame.mouse.get_rel()
        mouse.move(x)

        # deletes notes if they go out of the screen
        for note in to_draw:
            if type(note) == Tap:
                if note.time <= -150:
                    to_draw.remove(note)
                    if note in holds:
                        holds.remove(note)
                    settings.amounts[3] += 1
                    settings.combo = 0
            if type(note) == Hold:
                if note.time + note.length <= -150:
                    to_draw.remove(note)
                    settings.amounts[3] += 1
                    settings.combo = 0
                if note.time + note.length <= 90 and note in held:
                    held.remove(note)
                    holds.remove(note)
                    to_draw.remove(note)
            if type(note) == Arc:
                if note.time + note.length <= -150:
                    to_draw.remove(note)
                    if note in held:
                        held.remove(note)
            else:
                break

        # deleting notes in holds automatically
        for note in holds:
            if note.time + note.length <= -150:
                holds.remove(note)
            elif note not in to_draw:
                print(note)
                holds.remove(note)

        # moving notes to draw to to_draw list
        for note in settings.notes:
            note.update(diff)
            if note.time <= 800 and note not in to_draw:
                to_draw.append(note)
                settings.notes.remove(note)

        # drawing all visible notes and moving them all down
        for note in to_draw:
            if type(note) == Tap:
                gfs.draw_note(screen, note.get_rect(settings))
            else:
                gfs.draw_note(screen, note.get_rect(settings), note.is_hit)
            note.update(diff)

        # draw lane boundaries, mouse cursor, and stats
        gfs.draw_lanes(settings, screen)
        pygame.draw.rect(screen, (0, 0, 0), mouse.get_rect(settings))
        gfs.draw_stats(screen, settings)

        # update display
        pygame.display.update()


def menu(prev):
    global run
    # detaches inputs from program so mouse can be moved out, pauses song, and gets current time
    pygame.event.set_grab(False)
    pygame.mixer.pause()
    current = pygame.time.get_ticks()

    # draw pause menu
    polygon = [screen.get_rect().topleft, screen.get_rect().topright, screen.get_rect().bottomright, screen.get_rect().bottomleft]
    pygame.draw.polygon(screen, (150, 150, 150), polygon)
    font = pygame.font.SysFont(None, 48)
    text = font.render("Press Esc to resume", True, (0, 0, 0))
    rect = text.get_rect()
    rect.midtop = (600, 350)
    screen.blit(text, rect)
    pygame.display.update()

    # waiting for inputs
    while True:
        for event in pygame.event.get():
            # ends program if window is closed
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                return 0
            # ends pause state
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.unpause()
                    return pygame.time.get_ticks() - (current - prev)


main()


