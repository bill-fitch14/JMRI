'''
Created on 13 Jan 2019

@author: bill
'''
# -*- coding: utf-8 -*-
import doctest
import time
import pyj2d as pygame

SPACE_PER_PEG = 200

def hanoi(pegs, start, target, n):
    """
    From stackoverflow:
      http://stackoverflow.com/questions/23107610/towers-of-hanoi-python-understanding-recursion
      http://stackoverflow.com/questions/41418275/python-translating-a-printing-recursive-function-into-a-generator

    This function, given a starting position of an hanoi tower, yields
    the sequence of optimal steps that leads to the solution.

    for position in hanoi([ [3, 2, 1], [], [] ], 0, 2, 3): print position
    [[3, 2], [], [1]]
    [[3], [2], [1]]
    [[3], [2, 1], []]
    [[], [2, 1], [3]]
    [[1], [2], [3]]
    [[1], [], [3, 2]]
    [[], [], [3, 2, 1]]

    """
    assert len(pegs[start]) >= n, 'not enough disks on peg'
    if n == 1:
        pegs[target].append(pegs[start].pop())
        yield pegs
    else:
        aux = 3 - start - target  # start + target + aux = 3
        for i in hanoi(pegs, start, aux, n-1): yield i
        for i in hanoi(pegs, start, target, 1): yield i
        for i in hanoi(pegs, aux, target, n-1): yield i

def display_pile_of_pegs(pegs, start_x, start_y, peg_height, screen):
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

def visual_hanoi_simulation(number_of_pegs, base_width, peg_height, sleeping_interval):
    """
    Visually shows the process of optimal solution of an hanoi tower problem.
    """
    print "hello";
    pegs = [[i * base_width for i in reversed(range(1, number_of_pegs+1))], [], []]
    positions = hanoi(pegs, 0, 2, number_of_pegs)

    pygame.init()
    print "hello2";	
    screen = pygame.display.set_mode( (1650, 1650) )
    pygame.display.set_caption('Towers of Hanoi')

    for position in positions:
        screen.fill((255, 255, 255))
        for i, pile in enumerate(position):
            display_pile_of_pegs(pile, 50 + SPACE_PER_PEG*i, 500, peg_height, screen)
        pygame.display.update()
        time.sleep(sleeping_interval)

    pygame.quit()

# if __name__ == "__main__":
    # print "hi"	
    # visual_hanoi_simulation(
        # number_of_pegs = 4,
        # base_width = 30,
        # peg_height = 40,
        # sleeping_interval = 0.5
    # )
    #doctest.testmod()
##    visual_hanoi_simulation(
##        number_of_pegs = 8,
##        base_width = 20,
##        peg_height = 30,
##        sleeping_interval = 0.2
##    )


print "hi"
