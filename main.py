import pygame
from Classes import Settings, Tap, Hold, Mouse
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


def main():
    global run
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
        # immediately ends the program if run is set to false
        if not run:
            break

        # code to check for tapped notes if a keydown event is detected
        if True in pressed_lanes:
            notes: dict = gfs.get_bottom_notes(to_draw)
            for lane in range(4):
                if pressed_lanes[lane]:
                    if notes.get(lane + 1):
                        if type(notes[lane + 1]) == Tap:
                            tap.stop()
                            tap.play()
                            to_draw.remove(notes[lane + 1])
                        if type(notes[lane + 1]) == Hold:
                            tap.stop()
                            tap.play()
                            notes[lane + 1].is_hit = True

        # filling screen with white background
        screen.fill((255, 255, 255))

        # calculate time between this frame and the previous frame
        current = pygame.time.get_ticks()
        diff = current - prev
        prev = pygame.time.get_ticks()

        # moving arc catcher (square at the bottom of the screen)
        x, y = pygame.mouse.get_rel()
        mouse.move(x)

        # draw all notes to be drawn, and deletes them if they go out of the screen
        for note in to_draw:
            if type(note) == Tap:
                if note.time <= -150:
                    to_draw.remove(note)
            if type(note) == Hold:
                if note.time + note.length <= -150:
                    to_draw.remove(note)

            else:
                break

        # moving all the notes down
        for note in settings.notes:
            note.update(diff)
            if note.time <= 800 and note not in to_draw:
                to_draw.append(note)
                settings.notes.remove(note)

        # drawing all visible notes and moving them all down
        for note in to_draw:
            gfs.draw_note(screen, note.get_rect(settings))
            note.update(diff)

        # draw lane boundaries and mouse cursor
        gfs.draw_lanes(settings, screen)
        pygame.draw.rect(screen, (0, 0, 0), mouse.get_rect(settings))

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


