import sys, os
#sys.path.append('C:\\Program Files (x86)\\JMRI\\jython\\an inglenook puzzle')
#sys.path.append('C:\\Users\\bill\\Dropbox\\Shunting puzzle\\Python\\an inglenook puzzle')
#sys.path.append('Z:\\Shunting puzzle\\Python\\an inglenook puzzle')
#C:\Program Files (x86)\JMRI\jython\an inglenook puzzle
my_path_to_jars = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/jars')
sys.path.append(my_path_to_jars) # add the jar to your path
my_path_to_classes = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/Inglenook')
sys.path.append(my_path_to_classes) # add the jar to your path
import doctest
import time
import pyj2d as pygame
import threading
from inglenook import Inglenook
from move_train import Move_train


SPACE_PER_PEG = 200

def hanoi(pegs, start, target, n):
    yield pegs
    # """
    # From stackoverflow:
    #   http://stackoverflow.com/questions/23107610/towers-of-hanoi-python-understanding-recursion
    #   http://stackoverflow.com/questions/41418275/python-translating-a-printing-recursive-function-into-a-generator
    #
    # This function, given a starting position of an hanoi tower, yields
    # the sequence of optimal steps that leads to the solution.
    #
    # for position in hanoi([ [3, 2, 1], [], [] ], 0, 2, 3): print position
    # [[3, 2], [], [1]]
    # [[3], [2], [1]]
    # [[3], [2, 1], []]
    # [[], [2, 1], [3]]
    # [[1], [2], [3]]
    # [[1], [], [3, 2]]
    # [[], [], [3, 2, 1]]
    #
    # """
    # assert len(pegs[start]) >= n, 'not enough disks on peg'
    # if n == 1:
    #     pegs[target].append(pegs[start].pop())
    #     yield pegs
    # else:
    #     aux = 3 - start - target  # start + target + aux = 3
    #     for i in hanoi(pegs, start, aux, n-1): yield i
    #     for i in hanoi(pegs, start, target, 1): yield i
    #     for i in hanoi(pegs, aux, target, n-1): yield i

def display_pile_of_pegs(pegs, start_x, start_y, peg_height, screen, base_width):
    """
    Given a pile of pegs, displays them on the screen, nicely inpilated
    like in a piramid, the smaller in lighter color.
    """
    for i, pegwidth in enumerate(pegs):
        #print ("enumerate pegs",i)
        #pegwidth = pegs[i] * base_width

        pygame.draw.rect(
            screen,
            # Smaller pegs are ligher in color
            (255-pegwidth*base_width, 255-pegwidth*base_width, 255-pegwidth*base_width),
            (
              start_x + (SPACE_PER_PEG - pegwidth* base_width)/2 , # Handles alignment putting pegs in the middle, like a piramid
              start_y - peg_height * i,         # Pegs are one on top of the other, height depends on iteration
              pegwidth*base_width,
              peg_height
            )
        )

def display_pile_of_pegs1(pegs, start_x, start_y, peg_height, screen):
    """
    Given a pile of pegs, displays them on the screen, nicely inpilated
    like in a piramid, the smaller in lighter color.
    """
    for i, pegwidth in enumerate(pegs):

        pygame.draw.rect(
            screen,
            # Smaller pegs are ligher in color
            (255-pegwidth, 255-pegwidth, 255-pegwidth),
            (
              start_x + (SPACE_PER_PEG - pegwidth)/2 , # Handles alignment putting pegs in the middle, like a piramid
              start_y - peg_height * i,         # Pegs are one on top of the other, height depends on iteration
              pegwidth,
              peg_height
            )
        )
def setup(pegs, noPegs):
    print "setup"
    #for i in range(0,2):
    #    assert len(pegs[i]) == noPegs[i], 'not enough disks on peg'
    yield pegs
    #now run the shunting puzzle
    ingle = Inglenook(pegs)

    #don't need these
    #ingle.init_position_branch()
    for p in ingle.solvePuzzle():
        yield p
    print "end of setup"

    #assert ingle.positions.count(1) == 1
    #assert ingle.branches.count(1) == 5
    #assert ingle.branches.count(2) == 3

def visual_simulation(number_of_pegs, base_width, peg_height, sleeping_interval):
    """
    Visually shows the process of optimal solution of an hanoi tower problem.
    """
    #pegs = [[i* base_width  for i in reversed(range(1, number_of_pegs+1))], [], []]
    pegs = [[i * base_width for i in reversed(range(1, number_of_pegs + 1))], [], []]

    positions = setup(pegs, number_of_pegs)

    pygame.init()
    screen = pygame.display.set_mode( (1650, 1650) )
    pygame.display.set_caption('Towers of Hanoi')

    for position in positions:
        screen.fill((255, 255, 255))
        for i, pile in enumerate(position):
            if type(pile[1])== "str":
                pass
            else:
                display_pile_of_pegs1(pile, 50 + SPACE_PER_PEG*i, 500, peg_height, screen)
        pygame.display.update()
        time.sleep(sleeping_interval)

    pygame.quit()

def visual_hanoi_simulation(number_of_pegs, base_width, peg_height, sleeping_interval):
    """
    Visually shows the process of optimal solution of an hanoi tower problem.
    """
    pegs = [[i * base_width for i in reversed(range(1, number_of_pegs+1))], [3*base_width,2,1], []]
    #pegs = [[5, 4, 3, 2, 1], [8,7,6], [], []]
    #pegs = [[i * base_width for i in pegs1[0]], [i * base_width for i in pegs1[1]], [], []]
    print(pegs)
    print(pegs)
    positions = hanoi(pegs, 0, 2, number_of_pegs)

    pygame.init()
    screen = pygame.display.set_mode( (1650, 1650) )
    pygame.display.set_caption('Towers of Hanoi')

    for position in positions:
        screen.fill((255, 255, 255))
        for i, pile in enumerate(position):
            display_pile_of_pegs(pile, 50 + SPACE_PER_PEG*i, 500, peg_height, screen, base_width)
        pygame.display.update()
        time.sleep(sleeping_interval)

    pygame.quit()



def setupBlocks(noPegs, base_width, peg_height, sleeping_interval):
    # pegs = [[i  for i in reversed(range(1, noPegs[0]+1))],
    #         #[i  for i in reversed(range(noPegs[0]+1, noPegs[0]+ noPegs[1]+1))],
    #         [1,2,3],[],[]]
    #         #[i  for i in reversed(range(noPegs[0]+ noPegs[1]+1, noPegs[0]+ noPegs[1]+ noPegs[2]+1))],
    #         #[i  for i in reversed(range(noPegs[0]+ noPegs[1]+ noPegs[2]+1, noPegs[0]+ noPegs[1]+ noPegs[2]+ noPegs[3]+1))]]
    
    print "hi1"
    pegs = [[2,1,5,3,4],[6,7,8],[],[]]

    train = Move_train()

    positions = setup(pegs, noPegs)

    pygame.init()
    x=100
    y=0
    
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (x,y)
    screen = pygame.display.set_mode( (1650, 1650) )
    pygame.display.set_caption('Shunting Puzzle Dropbox Version')

    for position in positions:
        screen.fill((255, 255, 255))
        # if type (position[0]) != "list":
        #     pass
        # else:
        #     for i, pile in enumerate(position):
        #         display_pile_of_pegs(pile, 50 + SPACE_PER_PEG*i, 500, peg_height, screen, base_width)
        #         # if type(pile[1])== "str":
        #         #     pass
        #         # else:
        #         #     display_pile_of_pegs(pile, 50 + SPACE_PER_PEG * i, 500, peg_height, screen, base_width)
        #     pygame.display.update()
        #     time.sleep(sleeping_interval)
        if type(position[0]) is str:
            #this is a command for the train
            train.decide_what_to_do(position)
            pass
        else:
            print (position)
            for i, pile in enumerate(position):
                display_pile_of_pegs(pile, 50 + SPACE_PER_PEG * i, 500, peg_height, screen, base_width)


            # if type(pile[1])== "str":
            #     pass
            # else:
            #     display_pile_of_pegs(pile, 50 + SPACE_PER_PEG * i, 500, peg_height, screen, base_width)
            pygame.display.update()
            time.sleep(sleeping_interval)

    pygame.quit()


# if __name__ == '__main__':

    # # visual_hanoi_simulation(
    # #       number_of_pegs = 4,
    # #       base_width = 30,
    # #       peg_height = 40,
    # #       sleeping_interval = 0.2
    # # )

    # doctest.testmod()
    # setupBlocks(
        # noPegs = 4,
        # base_width = 30,
        # peg_height = 40,
        # sleeping_interval = 1

# )


def run_inglenook():
    print "lo"
    #doctest.testmod()
    setupBlocks(
        noPegs = 4,
        base_width = 30,
        peg_height = 40,
        sleeping_interval = 0.05
    )
    pygame.quit()
    print "end of run_inglenook"
    
def setup_thread():
    print "hi"
    t = threading.Thread(target=run_inglenook, name="run Shunting Puzzle")
    t.daemon = True
    t.start()


# if __name__ == '__main__':
    # setup_thread()



print "hi this is the dropbox version"
print __name__
setup_thread()
# print "hi"
# t = threading.Thread(target=run_inglenook, name="run Shunting Puzzle")
# t.daemon = True
# t.start()


