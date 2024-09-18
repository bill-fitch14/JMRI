import java
import jmri
import sys


#allow import of pyj2D
my_path_to_pyj2d = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/jars/pyj2d')
sys.path.append(my_path_to_pyj2d)  # add my_path_to_pyj2d to your path
my_path_to_pyj2d = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/jars')
sys.path.append(my_path_to_pyj2d)  # add my_path_to_pyj2d to your path
print "sys.path", sys.path

import pyj2d as pygame

class Class1(jmri.jmrit.automat.AbstractAutomaton):

    def __init__(self, mode):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        # running = True
        pygame_running = True
        print "£$%^&*()_"

        while pygame_running:
            # print "fred"

            if pygame_running:
                # Your game logic here
                if mode == "black":
                    screen.fill((0, 0, 0))  # Example: fill screen with black
                    # pygame.display.flip()
                    print "fred"
                    # pygame_running = False

                # event = pygame.event.wait()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # pygame_running = False  # Stop the Pygame loop
                        # pygame.display.quit()  # Close the Pygame display
                        print "close button pressed"
                        pass

            # self.waitMsec(500)

            # Additional logic outside of Pygame loop
            print("Pygame window closed, but program is still running.")
            # Add any additional code here

if __name__ == "__builtin__":
    # print "running new8.py"
    # Class1("black")
    # Class1("white")
    # Additional code can be placed here as well
    # print("Program is still running after Pygame window is closed.")
    pass