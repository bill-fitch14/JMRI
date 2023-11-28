# from timeout import timeout,  alternativeaction, thread_with_trace, variableTimeout
# import pyj2d as pygame
# from pyj2d.locals import *
# import time
# from inglenook import Inglenook
# import config
#
# SPACE_PER_PEG = 50
#
# from timeout import alternativeaction, variableTimeout, print_name, timeout
#
# @print_name()
# def display_pile_of_pegs(pegs, start_x, start_y, peg_height, screen, base_width):
#     """
#     Given a pile of pegs, displays them on the screen, nicely inpilated
#     like in a piramid, the smaller in lighter color.
#     """
#     for i, pegwidth in enumerate(pegs):
#         #print ("enumerate pegs",i)
#         #pegwidth = pegs[i] * base_width
#         #self.factor = 1
#         #pw = pegwidth* base_width
#         pw = base_width* 8.0/3 + 2*pegwidth* base_width/3  #make the decrease in width smaller
#         pygame.draw.rect(
#             screen,
#             # Smaller pegs are ligher in color
#             #(255-pegwidth*base_width, 255-pegwidth*base_width, 255-pegwidth*base_width),
#             (255 - 100, 255 - 100, 255 - 100),
#             #pyj2d.locals.blue,
#             (
#               start_x + SPACE_PER_PEG * i +(SPACE_PER_PEG - pw)/2 , # Handles alignment putting pegs in the middle, like a piramid
#               start_y, #- peg_height * i,         # Pegs are one on top of the other, height depends on iteration
#               pw,
#               peg_height
#             )
#         )
#         # draw the truck number
#         #print("xx")
#         font = pygame.font.SysFont('Arial', 12)
#         #print("yy")
#         xcoord = start_x + SPACE_PER_PEG * i + (SPACE_PER_PEG - pegwidth* base_width)/2 + pegwidth* base_width/2 - base_width/3
#         ycoord = start_y #- peg_height * i
#         black = (0,0,0)
#         screen.blit(font.render(str(pegwidth), True, black), (xcoord, ycoord))
#
# def setup(pegs, noPegs):
#     print ("setup")
#     #for i in range(0,2):
#     #    assert len(pegs[i]) == noPegs[i], 'not enough disks on peg'
#     yield pegs
#     #now run the shunting puzzle
#     ingle = Inglenook(pegs)
#     print("fghkl***********************************************************************************************************")
#     #don't need these
#     #ingle.init_position_branch()
#     for p in ingle.solvePuzzle():
#         yield p
#     print ("end of setup")
#
#     #assert ingle.positions.count(1) == 1
#     #assert ingle.branches.count(1) == 5
#     #assert ingle.branches.count(2) == 3
#
#
# # def setupBlocks(noPegs, base_width, peg_height, sleeping_interval):
# #     # pegs = [[i  for i in reversed(range(1, noPegs[0]+1))],
# #     #         #[i  for i in reversed(range(noPegs[0]+1, noPegs[0]+ noPegs[1]+1))],
# #     #         [1,2,3],[],[]]
# #     #         #[i  for i in reversed(range(noPegs[0]+ noPegs[1]+1, noPegs[0]+ noPegs[1]+ noPegs[2]+1))],
# #     #         #[i  for i in reversed(range(noPegs[0]+ noPegs[1]+ noPegs[2]+1, noPegs[0]+ noPegs[1]+ noPegs[2]+ noPegs[3]+1))]]
# #
# #     print ("in setupBlocks")
# #     # import sys;sys.path.append(r'C:\Users\bill_\.p2\pool\plugins\org.python.pydev.core_7.2.1.201904261721\pysrc')
# #     # import pydevd;pydevd.settrace()
# #     pegs = [[2,1,5,3,4],[6,7,8],[],[],[]]
# #
# #
# #
# #     positions = setup(pegs, noPegs)
# #
# #     pygame.init()
# #     screen = pygame.display.set_mode( (650, 200) )
# #     pygame.display.set_caption('Shunting Puzzle')
# #     index = 0
# #     print("setupblocksa index != 1 " + str(index))
# #     for position in positions:
# #
# #         screen.fill((255, 255, 255))
# #         # if type (position[0]) != "list":
# #         #     pass
# #         # else:
# #         #     for i, pile in enumerate(position):
# #         #         display_pile_of_pegs(pile, 50 + SPACE_PER_PEG*i, 500, peg_height, screen, base_width)
# #         #         # if type(pile[1])== "str":
# #         #         #     pass
# #         #         # else:
# #         #         #     display_pile_of_pegs(pile, 50 + SPACE_PER_PEG * i, 500, peg_height, screen, base_width)
# #         #     pygame.display.update()
# #         #     time.sleep(sleeping_interval)
# #         if type(position[0]) is str:
# #             #this is a command for the train
# #             #print("setupblocksb index = " + str(index))
# #             index += 1
# #             #print("setupblocksc index = " + str(index))
# #             #print (">> setup Blocks: position = ", position )
# #             #print (position)
# #             #print("setupblocksd index = " + str(index))
# #             if index == 1:
# #                 print("setupblockse index == 1 " + str(index))
# #                 print("setupblocks index = 1")
# #                 config.t.decide_what_to_do_first()
# #             #print("setupblocksf index = " + str(index))
# #             config.t.decide_what_to_do(position)
# #
# #             ##train.update_position(position)
# #             pass
# #         else:
# #             #print("setupblocksg index != 1 " + str(index))
# #             #print (">> setup Blocks2: position = " )
# #             #print (position)
# #             for i, pile in enumerate(position):
# #                 print("i=",i)
# #                 if i == 0:
# #                     starty = 50
# #                     j = 0
# #                     startdraw = 2
# #                     enddraw = 8
# #                     vstartdraw = 0
# #                     venddraw = 1
# #                 elif i == 1:
# #                     starty = 100
# #                     j = 0
# #                     startdraw = 3
# #                     enddraw = 8
# #                     vstartdraw = 0
# #                     venddraw = 1
# #                 elif i == 2:
# #                     starty = 150
# #                     j = 0
# #                     startdraw = 4
# #                     enddraw = 8
# #                     vstartdraw = 0
# #                     venddraw = 1
# #                 elif i == 3:
# #                     starty = 50
# #                     j = 0
# #                     startdraw = 1
# #                     enddraw = 2
# #                     vstartdraw = 100
# #                     venddraw = 1
# #                 startx = 1000 #+ SPACE_PER_PEG * (j+1)
# #                 starty += 0
# #                 #startx = 20 + SPACE_PER_PEG * i
# #                 #starty = 50 * (j+1)
# #                 display_pile_of_pegs(pile, 20 + startx+ startdraw * SPACE_PER_PEG, starty, peg_height, screen, base_width)
# #                 h = 30
# #                 if i == 0  or i == 1 or i == 2 or i == 3:
# #                     color = (0,0,0)
# #                     pygame.draw.line(screen, color, (startx+ startdraw * SPACE_PER_PEG,starty+peg_height ),
# #                     (startx+enddraw * SPACE_PER_PEG, starty+peg_height), 2)
# #                 if i == 0 or i == 1 :
# #                     pygame.draw.line(screen, color, (startx+ startdraw * SPACE_PER_PEG + vstartdraw * SPACE_PER_PEG,starty+peg_height ),
# #                     (startx+ startdraw * SPACE_PER_PEG + venddraw * SPACE_PER_PEG, starty+peg_height+50), 2)
# #                 # if i == 2:
# #                     # pygame.draw.line(screen, (0,0,0), (startx+ 1 * SPACE_PER_PEG,starty+peg_height ),
# #                     # (startx+1.1 * SPACE_PER_PEG, starty+peg_height+50), 2)
# #             pygame.display.update()
# #             time.sleep(sleeping_interval)
# #
# #     pygame.quit()
#
# # def run_inglenook():
# #     setupBlocks(
# #         noPegs = 5,
# #         base_width = 5,
# #         peg_height = 15,
# #         sleeping_interval = 1
# #     )
# #     print ("end of run_inglenook")
#
# def setup_thread():
#     print ("hi")
#     #t = threading.Thread(target=run_inglenook, name="run Shunting Puzzle")
#     t = thread_with_trace(target=run_inglenook, name="run Shunting Puzzle")
#     t.daemon = True
#     t.start()