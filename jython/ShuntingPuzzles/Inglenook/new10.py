import jmri
import sys

my_path_to_pyj2d = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/jars')
sys.path.append(my_path_to_pyj2d)  # add my_path_to_pyj2d to your path

import pyj2d as pygame
import threading
import time




class RunProg(jmri.jmrit.automat.AbstractAutomaton):

    def run_main(self):
        running = True
        while running:
            print ("fred")
            time.sleep(10)


    # Define a function to run in a separate thread
    def run_pygame(self):

        # Initialize Pygame
        print "initialising pygame"
        pygame.init()
        pygame.display.set_caption("Pygame in a Thread")
        print "initialised"

        screen = pygame.display.set_mode((800, 600))
        # Fill the screen with a color
        screen.fill((0, 128, 255))

        # Draw a rectangle
        pygame.draw.rect(screen, (255, 0, 0), (100, 100, 200, 100))

        print "drawn"

        running = True
        count = 0
        while running:
            print "count", count
            count += 1
            # if count == 2:
            #     running = False
            # self.waitMsec(3000)

        #
            print "in running", count
            if count == 10:
                pygame.quit()
        #     # for event in pygame.event.get():
        #     #     if event.type == pygame.QUIT:
        #     #         running = False
        #
        #     # # Fill the screen with a color
        #     # screen.fill((0, 128, 255))
        #     #
        #     # # Draw a rectangle
        #     # pygame.draw.rect(screen, (255, 0, 0), (100, 100, 200, 100))
        #
        #     # Update the display
        #     # pygame.display.flip()
        #
        #     # Cap the frame rate



        # pygame.quit()


# # Set up the display

# pygame.display.set_caption("Pygame in a Thread")
print "running pygame"
# pygame.display.set_caption("Pygame")

# Create and start the thread

# pygame_thread = threading.Thread(target=run_pygame)
# pygame_thread.start()
#
# main_thread = threading.Thread(target=run_main)
# main_thread.start()

# Main thread can do other things
print "main thread"

RunProg().run_pygame()
# try:
#     print "in try"
#     # while pygame_thread.isAlive():
#     #     print ("a")
#     #     print("Pygame is running in a thread...")
#     #     time.sleep(1)
# except:
#     print "exception "
#
# while(True):
#     print("b")
#     print("Pygame thread has finished.")
#     # time.sleep(10000)