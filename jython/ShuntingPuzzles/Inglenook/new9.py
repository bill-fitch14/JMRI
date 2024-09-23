import jmri
import sys

my_path_to_pyj2d = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/jars')
sys.path.append(my_path_to_pyj2d)  # add my_path_to_pyj2d to your path

import pyj2d as pygame
import threading
import time


def run_pygame():
    print "running pygame"
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Window")

    running = True
    count = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 128, 255))
        pygame.draw.rect(screen, (255, 0, 0), (100, 100, 200, 100))
        print "z"
        # pygame.display.flip()
        pygame.display.update()
        print "a"
        # time.sleep(5)
        print "b"
        count += 1
        if count == 1:
            return
    print "c"
    # pygame.quit()

def main_program():
    print("Main program running...")
    time.sleep(2)
    print("Starting Pygame...")
    run_pygame()
    print("Pygame window closed. Main program continues...")
    time.sleep(2)
    print("Main program finished.")


main_program()
