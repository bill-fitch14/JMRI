from inglenook import Inglenook
from timeout import alternativeaction, variableTimeout, print_name, timeout
import time
import java
import jmri
import copy
from javax.swing import JLabel
from collections import deque
#
# import java
# import jmri
import sys

#my_path_to_pyj2d = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/jars/pyj2d.jar')
#my_path_to_pyj2d = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/Inglenook/pyj2d')
#sys.path.append(my_path_to_pyj2d)  # add the jar to your path
#exec(open (my_path_to_pyj2d).read())
#
#import pyj2d as pygame
#from move_train import Move_train

#move_train = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/inglenook/move_train.py')
#exec(open (move_train).read())

import threading
from threading import Thread

class InglenookMaster(jmri.jmrit.automat.AbstractAutomaton):
    global place_trucks_near_disconnect_siding
    logLevel = 1
    indentno = 0

    place_trucks_near_disconnect_siding = False

    def init(self):
        print "init InglenookMaster"
        global indentno
        indentno = 0
        self.initial_entry = None
        print "CLOSED2",CLOSED
        self.dialogs = OptionDialog()
        self.pegs_updated_by_simulation = None

    def setup(self):
        global do_not_restart_pygame

        if "do_not_restart_pygame" not in globals():
            print "do_not_restart_pygame not in globals()"

        print "do_not_restart_pygame", do_not_restart_pygame

        print "setup InglenookMaster"
        if self.logLevel > 0: print "starting InglenookMaster setup"

        self.get_inglenook_run_or_simulate_buttons = \
            [sensors.getSensor(sensorName) for sensorName in \
             ["justShowSortingInglenookSensor", "simulateInglenookSensor", \
              "simulateErrorsInglenookSensor", \
              "simulateDistributionInglenookSensor", "runRealTrainNoDistributionInglenookSensor", \
              "runRealTrainDistributionInglenookSensor","InglenookHelpSensor"]]

        # read the items set up om stage1 panel
        self.read_memories()
        # print "read memories"

        # set flag to startup pygame unless we are restarting using the stop and run buttons
        print "do_not_restart_pygame", do_not_restart_pygame
        if do_not_restart_pygame == True:
            print "a"
            self.initialise = False
        else:
            print "b"
            self.initialise = True
        print "self.initialise", self.initialise, "True", True
        return True

    def read_memories(self):

        # # sensors set up in move_train
        # # turnouts set up in move_train
        #
        # # sizes of sidings
        # self.Inglenook = Inglenook()
        #
        [self.no_trucks_short, self.no_trucks_long, self.no_trucks_total] = self.get_no_trucks()
        #
        #
        #
        # self.I.get_no_trucks(no_trucks_str)

    def handle(self):

        self.waitSensorActive(self.get_inglenook_run_or_simulate_buttons)

        sensor_that_went_active = [sensor for sensor in self.get_inglenook_run_or_simulate_buttons if sensor.getKnownState() == ACTIVE][0]

        size_long_siding = self.no_trucks_long
        size_short_sidings = self.no_trucks_short

        self.act_on_sensors(sensor_that_went_active, size_long_siding, size_short_sidings)
        # print "qwertyu **************************"
        # print "sensor_that_went_active", sensor_that_went_active.getUserName()
        sensor_that_went_active.setKnownState(INACTIVE)
        # print "set sensor inactive"
        return True

    def act_on_sensors(self, active_sensor, size_long_siding, size_short_sidings):
        global display_message_flag

        # print "handle InglenookMaster"

        # self.no_trucks = self.get_no_trucks()
        # [no_trucks_short, no_trucks_long, no_trucks_total] = self.no_trucks

        # print "[no_trucks_short, no_trucks_long, no_trucks_total]", \
        #     [self.no_trucks_short, self.no_trucks_long, self.no_trucks_total]

        # print "active_sensor", active_sensor, active_sensor.getUserName()
        # print "sensors.getSensor(runRealTrainDistributionInglenookSensor)", sensors.getSensor("runRealTrainDistributionInglenookSensor")

        if active_sensor == sensors.getSensor("InglenookHelpSensor"):
            self.display_help()
            return
        if active_sensor == sensors.getSensor("runRealTrainDistributionInglenookSensor") or \
                active_sensor == sensors.getSensor("simulateDistributionInglenookSensor"):
            distribute_trucks = True
        else:
            distribute_trucks = False

        # print ("distribute_trucks", distribute_trucks, "active_sensor", active_sensor.getUserName())
        if active_sensor == sensors.getSensor("justShowSortingInglenookSensor") and 1==0:      #set 1==1 to iterate through all allowable positions
            result = []
            [no_trucks_short, no_trucks_long, no_trucks_total] = self.get_no_trucks()
            for i in range(1, no_trucks_long + 2*no_trucks_short ): #iterate for all positions
                pos, siding_no = self.siding_no_and_pos(i)
                # print "iteration", i, "pos", pos, "siding_no", siding_no, "set_positions_of_trucks"
                initial_positions_of_trucks = self.set_positions_of_trucks(distribute_trucks, i )
                # print "initial_positions_of_trucks", initial_positions_of_trucks
                position = self.generate_positions_using_yield_statements(active_sensor, distribute_trucks, initial_positions_of_trucks)
                # print "checking final position"
                self.check_final_position(position, i, result)
            # print "result", result
        else:
            initial_positions_of_trucks = self.set_positions_of_trucks(distribute_trucks)
            # print "initial_positions_of_generate_positions_using_yield_statements", initial_positions_of_trucks
            self.generate_positions_using_yield_statements(active_sensor, distribute_trucks, initial_positions_of_trucks)

    def display_help(self):
        ref = "html.scripthelp.DispatcherSystem.DispatcherSystem"
        jmri.util.HelpUtil.displayHelpRef(ref)

    def check_final_position(self, position, i, result):

        pos, siding_no = self.siding_no_and_pos(i)

        # print "position", position
        # print "position[4]", position[4]
        # print "position[4][0]", position[4][0]

        if self.get_no_trucks1("long") == 5:
            requred_arrangement = deque([5, 4, 3, 2, 1])
        elif self.get_no_trucks1("long") == 4:
            requred_arrangement = deque([4, 3, 2, 1])
        else:
            requred_arrangement = deque([3, 2, 1])

        if position[4][0] == requred_arrangement:
            # print "success", str(siding_no) + " " + str(pos) + " success"
            result.append(str(siding_no) + " " + str(pos) + " success")
            # print "result", result
            # print
        else:
            # print "failure", position[4][0]
            result.append("failure: " + str(position[4][0]))
            # print "result", result
            # print
        return result

    def siding_no_and_pos(self, i):
        [no_trucks_short, no_trucks_long, no_trucks_total] = self.get_no_trucks()
        if i < no_trucks_long:
            siding_no = 1
            pos = i
        elif i < no_trucks_long + no_trucks_short:
            siding_no = 2
            pos = i % (no_trucks_long)
        else:
            siding_no = 3
            pos = i % (no_trucks_long) % (no_trucks_short)
        return pos, siding_no

    def startPygame(self):
        global screen
        # if pygame.display.get_init() == False:
        print "self.initialise in startPygame", self.initialise
        if self.initialise:
            pygame.display.init()
            screen = pygame.display.set_mode((700, 250))
            self.initialise = False

        pygame.display.set_caption('Shunting Puzzle')
        screen.fill((255, 255, 255)) # white
        # return screen

    def generate_positions_using_yield_statements(self, active_sensor, distribute_trucks, initial_positions_of_trucks):
        global screen
        # the required positions of the trucks are generated using yield statements
        positions = self.determine_required_positions_of_trucks(
            initial_positions_of_trucks, self.no_trucks_long, self.no_trucks_short, distribute_trucks)
        # # the sequence of required positions are now used to move the train
        # and display visually where the trucks are

        # if pygame.display.get_init():
        #     pygame.display.init()
        #     screen = pygame.display.set_mode((700, 250))
        #
        # pygame.display.set_caption('Shunting Puzzle')
        # screen.fill((255, 255, 255)) # white

        # pygame_thread = Thread(target=self.startPygame)
        print "starting pygame"
        self.startPygame()


        # running = True
        # while running:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             print "!!!!!!!!!!!!!!!!!!!!!!quit!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11"
        #             # pygame.display.quit()  # Close the Pygame window
        #             running = False  # Exit the loop
        #             return


        # self.process_one_item_in_positions(positions, screen)
        train = Move_train2()
        # print "init finished (not there)"
        pegs_updated_by_simulation = None
        if train.setup():
            print "$$$generate_positions_using_yield_statements$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$train setup"
            # self.dialogs.displayMessage("train setup", True)
            train.setName('Start Inglenook')
            print "z"
            train.start()
            print "a"
            train.decide_what_to_do_first(active_sensor)
            print "b"
            if active_sensor == sensors.getSensor("justShowSortingInglenookSensor") or \
                    active_sensor == sensors.getSensor("simulateDistributionInglenookSensor"):
                position = self.justShowSorting(positions, pygame, screen, train)
                # print "end justShowSorting"
                return position
            elif active_sensor == sensors.getSensor("runRealTrainNoDistributionInglenookSensor"):
                print "fred"
                self.print_instructions(positions, pygame, screen, train)
            elif (active_sensor == sensors.getSensor("simulateInglenookSensor") or \
                  active_sensor == sensors.getSensor("simulateErrorsInglenookSensor")):
                self.simulateInglenook(positions, pygame, screen, train)
            elif active_sensor == sensors.getSensor("simulateDistributionInglenookSensor"):
                self.simulateInglenook(positions, pygame, screen, train)
            elif active_sensor == sensors.getSensor("runRealTrainNoDistributionInglenookSensor"):
                self.runRealTrain(positions, pygame, screen, train)
            elif active_sensor == sensors.getSensor("runRealTrainDistributionInglenookSensor"):
                self.runRealTrain(positions, pygame, screen, train)
            else:
                print "invalid option - Contact Developer"

        # if pygame.display != None:
        print "$$$end generate_positions_using_yield_statements$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
        # pygame.display.quit()
        # pygame.quit()
        # sys.exit()
        self.dialogs.displayMessage("closed pygame", True)

        # print  "end of inglenookMaster.py"

    def print_instructions(self, positions, pygame, screen, train):
        count = 0
        my_list = []
        for position in positions:
            # print "next position", count
            count += 1
            # print ("***", count, position)
            if type(position[0]) is str:
                # this is a command for the train
                #train.decide_what_to_do(position)
                #train.update_position
                #print position[0]
                if position[0] == "display_message":
                    [instruction, message] = position
                    # print "instruction", instruction, "message", message
                    # print "instruction", instruction
                    # self.dialogs.displayMessage("msg = : " + message)
                    #print "********************************msg = : " + message
                else:
                    [instruction, noTrucksToMove, fromBranch, destBranch, pegs] = position
                    # my_list.append(position)
                    print "instruction", instruction, noTrucksToMove, fromBranch, destBranch
            else:
                pass
                # # print("!!!!!!!!!!! this is a command for simulation 1", position)
                # # this is a command for pygame simulation
                # self.display_trucks_on_insert(position, screen)
                # #print "display truck on panel"
                # self.display_trucks_on_panel(position)
            # pygame.display.update()
            # print "displayed update1"
        # for l in reversed(my_list):
        #     [instruction, noTrucksToMove, fromBranch, destBranch, pegs] = l
        #     print "instruction", instruction, noTrucksToMove, fromBranch, destBranch
        return position



    def simulateDistributeTrucks(self, pygame, screen, train):
        # print "simulateDistributeTrucks"
        train.move_to_initial_position()

    def justShowSorting(self, positions, pygame, screen, train):
        # print "Called justShowSortingInglenookSensor"

        count = 0
        for position in positions:
            # print "next position", count
            count += 1
            # print ("***", count, position)
            if type(position[0]) is str:
                # this is a command for the train
                #train.decide_what_to_do(position)
                #train.update_position
                #print position[0]
                if position[0] == "display_message":
                    [instruction, message] = position
                    # self.dialogs.displayMessage("msg = : " + message)
                    #print "********************************msg = : " + message
            else:
                # print("!!!!!!!!!!! this is a command for simulation 1", position)
                # this is a command for pygame simulation
                self.display_trucks_on_insert(position, screen)
                #print "display truck on panel"
                self.display_trucks_on_panel(position)
            pygame.display.update()
            # print "displayed update1"
        return position

    def process_one_item_in_positions(self, positions, screen):
        position = next(positions)
        while position <> "end":
            if type(position[0]) is str:
                # check last move was OK
                if position[0] == "display_message":
                    [instruction, message] = position
                    self.dialogs.displayMessage("yielded message: " + message)
                else:
                    [instruction, noTrucksToMove, fromBranch, destBranch, pegs] = position
                    if instruction == "move_trucks_one_by_one":
                        display_message_flag = True
                    else:
                        display_message_flag = False
                    pegs_updated_by_simulation = train.decide_what_to_do(screen, positions, position)
                    pygame.display.update()

    def simulateInglenook_test(self, positions, pygame, screen, train):
        global display_message_flag
        count = 0
        for position in positions:
            # print "next position", count
            count += 1
            # print ("***", count, position)
            if type(position[0]) is str:
                if position[0] == "display_message":
                    pass
                    # [instruction, message] = position
                    # self.dialogs.displayMessage("yielded message: " + message)
                else:
                    [instruction, noTrucksToMove, fromBranch, destBranch, pegs] = position
                    print "position", position
                    # # print "instruction", instruction, "noTrucksToMove", noTrucksToMove
                    # if instruction == "move_trucks_one_by_one":
                    #     display_message_flag = True
                    # else:
                    #     display_message_flag = True
                    # # this is a command for the train
                    # pegs_updated_by_simulation = train.decide_what_to_do(screen, positions, position)
                    # pygame.display.update()
                    # self.pegs_updated_by_simulation = copy.deepcopy(pegs_updated_by_simulation)
                    # # print("pegs_updated_by_simulation1",self.pegs_updated_by_simulation)
                    # # print("*****************")
            else:
                # print("!!!!!!!!!!! this is a command for simulation 1", position)
                # this is a command for pygame simulation
                # self.display_trucks_on_insert(position, screen)
                # print "display truck on panel"
                # self.display_trucks_on_panel(position)
                pass
            pygame.display.update()
            # print "displayed update1"
        return position

    def runRealTrain(self, positions, pygame, screen, train):

        # simulateInglenook includes actions for real trains as well as viewing on screen
        self.simulateInglenook(positions, pygame, screen, train)

    def simulateInglenook(self, positions, pygame, screen, train):
        global display_message_flag
        print "simulatingInglenook"
        pegs_updated_by_simulation = []
        # position = next(positions)
        # while position <> "end":
        count = 0
        for position in positions:
            count += 1
            if type(position[0]) is str:
                # check last move was OK
                # if (position[0] != "display" and pegs_updated_by_simulation != []):
                #     self.check_old_position_is_ok(old_position, position, pegs_updated_by_simulation)      # compare self.pegs with pegs found from old_position
                if position[0] == "display_message":
                    [instruction, message] = position
                    self.dialogs.displayMessage("yielded message: " + message)
                else:
                    [instruction, noTrucksToMove, fromBranch, destBranch, pegs] = position
                    print "position", position
                    # print "instruction", instruction, "noTrucksToMove", noTrucksToMove
                    if instruction == "move_trucks_one_by_one":
                        display_message_flag = True
                    else:
                        display_message_flag = True
                    # this is a command for the train
                    pegs_updated_by_simulation = train.decide_what_to_do(screen, positions, position)
                    pygame.display.update()
                    self.pegs_updated_by_simulation = copy.deepcopy(pegs_updated_by_simulation)
                    # print("pegs_updated_by_simulation1",self.pegs_updated_by_simulation)
                    # print("*****************")
            else:
                # this is a command for the displays

                # show the initial position
                # subsequent positions will be generated in the moves above
                if count == 1:
                    self.display_trucks_on_insert(position, screen)
                    pygame.display.update()
                # self.display_trucks_on_panel(position)

            pygame.display.update()
            # if type(position[0]) is not str:
            #     old_position = copy.deepcopy(position)

    def simulateInglenookrunRealTrain(self, positions, pygame, screen, train):
        # print "Called justShowSortingInglenookSensor"
        count = 0
        for position in positions:
            # print "next position"
            count += 1
            # print ("******************", count, position)
            if type(position[0]) is str:
                # this is a command for the train
                #train.decide_what_to_do(position)
                #train.update_position
                if position[0] == "display_message":
                    [instruction, message] = position
                    self.dialogs.displayMessage("msg = : " + message)
            else:
                # print("!!!!!!!!!!! this is a command for simulation 1", position)
                # this is a command for pygame simulation
                self.display_trucks_on_insert(position, screen)
                # print "display truck on panel"
                self.display_trucks_on_panel(position)
            pygame.display.update()
            # print "displayed update"






    # #same call as for Simulation. Checks for this sensor are done in the call. We use all the chacks tested in Simulation Errors.
    # position = next(positions)
    # if type(position[0]) is str:
    #     train.decide_what_to_do(screen, positions, position)
    # else:
    #     print "position" , position
    #     print("error positions value is wrong type for Simulation - contact Developer3")


    ####################################

    # description for simulate Inglenook

    ####################################

    # the positions are generated using  the next function so that the simulation can mimic the simulated movement of the train
    # the options simulatePerfectSystem or simulate with errors are dealt with in move_train code

    # If simulate with errors we test the following
    # Tests:
    # 1) pop
    #     1)  The train connects to the trucks
    #         a) moves to the disconnect position counting trucks (should be the number that we have popped pop = n)
    #     2)   disconnects
    #         b) counts the trucks moving to spur (should be zero)
    # 1) tests
    #     if pop 1 set (a) to zero;
    #     if pop 2 set (a) to 1
    #     (a) if pop n set (a) to n-x  (x=1 but code generally)
    #         while not pop = x (or pop = n if repeat)
    #             move back count 1 Active and a little bit to connect
    #             draw out and count active x
    #     (b) while count > 0:
    #             move back to inactive
    #             disconnect
    #             move out and count
    #
    # 2) push
    #     1) The train pushes the trucks to the sencor
    #         a) counts the trucKs to push
    #     2) disconnects
    #         b) counts the trucks moving to spur (should be zero)
    # 2) tests
    #     (a) if count of trucks to push < trucks to push
    #         abort shunting puzzle. There has been an error in pop test \
    #     (b) while count > 0:
    #             move back to inactive
    #             disconnect
    #             move out and count

    def get_no_trucks(self):

        no_trucks_short = self.get_no_trucks1("short")
        no_trucks_long = self.get_no_trucks1("long")
        no_trucks_total = self.get_no_trucks1("total")

        return [no_trucks_short, no_trucks_long, no_trucks_total]

    def get_no_trucks1(self, no_trucks_str):
        #no_trucks is of the form short, long, total
        no_trucks = memories.getMemory('IMIS:no_trucks_' + no_trucks_str)
        # print "$$$$$$$$$$$$$$$$%", no_trucks.getValue(), 'IMIS:no_trucks_' + no_trucks_str
        return int(no_trucks.getValue())

    # def get_no_trucks1(self, noTrucks):
    #     #noTrucks is of the form %no_trucks_long^5^% or %no_trucks_short^5^%
    #
    #     ##print "get_no_trucks"
    #
    #     s = noTrucks.split("%")[1]   # notrucks..^5^
    #     s1 = s.split("^")[0]         # notrucks..
    #     s2 = s.split("^")[1]         # 5
    #     #print "siding", s, "s1", s1, "s2", s2
    #     for turnout in turnouts.getNamedBeanSet():
    #         comment = turnout.getComment()
    #         if comment != None:
    #             #print "comment" , comment
    #             if "%" in comment:
    #                 #print "% in comment"
    #                 for t0 in  comment.split('%'):
    #                     if "^" in t0:
    #                         t = str(t0)
    #                 #print "t", t
    #                 t1 = t.split("^")[0]         # notrucks..
    #                 t2 = t.split("^")[1]         # 5
    #                 #print "comment" , comment
    #                 #print "t1", t1, "t2", t2
    #                 #print "s", s, "comment.split('#')[0]", str(comment.split('#')[1]), "sensor", sensor, sensor.getUserName()
    #                 if t1 == s1:
    #                     #print "returning ", t2
    #                     return t2
    #                 #print "s",s,"x", str(comment.split('%')[1])
    #     print "end get_no_trucks"
    #     return None

    def check_old_position_is_ok(self, old_position, position, pegs_updated_by_simulation):
        return
        pegs = copy.deepcopy(old_position)
        pegs1 = copy.deepcopy(pegs_updated_by_simulation)
        pegs2 = copy.deepcopy(position)
        print("*************************")
        print("pegs (old)", pegs)
        print("pegs1 (simu) ", pegs1)
        print("pegs2 (new)", pegs2)
        list2 = self.strip_0(pegs1)
        list1 = self.strip_0(pegs)

        print ("pegs",list1, "pegs_updated_by_simulation", list2)
        if list1 != list2:
            print("***********************************")
            print "error"
            print("***********************************")
        else:
            print("***********************************")
            print("success")
            print("***********************************")

    def strip_0(self, pegs):
        list1 = []
        print("*************")
        print("strip_0 pegs: " , pegs)
        for deque in pegs:
            list = [item for item in deque if item>0]
            list1 .append(list)
        print("*************")
        return list1

    def display_trucks_on_panel(self, position):
        for siding_no, pile in enumerate(position):
            self.display_trucks_in_siding(siding_no, pile)
    def display_trucks_on_insert(self, position, screen):

        global decide_what_to_do_instruction
        global decide_what_to_do_instruction1
        global decide_what_to_do_instruction1a
        global decide_what_to_do_instruction2
        global decide_what_to_do_instruction2a

        # print "display trucks on insert"
        if sensors.getSensor("simulateInglenookSensor").getKnownState() == ACTIVE:
            show_mid_branch = False
        else:
            show_mid_branch = False
        base_width = 3
        peg_height = 20
        sleeping_interval = 1
        space_per_peg = 40

        screen.fill((255, 255, 255))  #blank the screen

        # screen.fill((255, 255, 255))  #blank the screen

        offset = -2
        offset2 = 3
        offset3 = -1
        n = 1

        for i, pile in enumerate(position):
            #print("i=",i)
            if i == 0:
                no_trucks = 5
                starty = 50
                j = 0
                startdraw = 2 + offset2
                enddraw = 8
                vstartdraw = 0
                venddraw = 1
            elif i == 1:
                no_trucks = 3
                starty = 100
                j = 0
                startdraw = 3 + offset2 + offset3
                enddraw = 8
                vstartdraw = 0
                venddraw = 1
            elif i == 2:
                no_trucks = 3
                starty = 150
                j = 0
                startdraw = 4 + offset2
                enddraw = 8
                vstartdraw = 0
                venddraw = 1
            elif i == 3:
                no_trucks = 3   # for positioning trucks on diagram
                if show_mid_branch:
                    starty = 0
                else:
                    starty = 50
                j = 0
                startdraw = -4 + offset2 + n
                enddraw = 2
                vstartdraw = 0
                venddraw = 1
            elif i == 4:
                no_trucks = 5
                starty = 50
                j = 0
                startdraw = 2 + offset - 2 + offset2
                enddraw = 8
                vstartdraw = 0
                venddraw = 1
            elif i == 5:
                no_trucks = 3
                starty = 100
                j = 0
                startdraw = 3 + offset + offset2
                enddraw = 8
                vstartdraw = 0
                venddraw = 1
            elif i == 6:
                no_trucks = 3
                starty = 150
                j = 0
                startdraw = 3  + offset + offset2
                enddraw = 8
                vstartdraw = 0
                venddraw = 1

            startx = 120 #+ SPACE_PER_PEG * (j+1)
            starty += 0
            #startx = 20 + SPACE_PER_PEG * i
            #starty = 50 * (j+1)
            self.display_pile_of_pegs(pile, i, no_trucks, 10 + startx+ startdraw * space_per_peg, starty, \
                                      peg_height, screen, base_width,space_per_peg, show_mid_branch)
            h = 30

        for i in range(8):
            if i == 0:
                no_trucks = 5
                starty = 50
                j = 0
                startdraw = 2
                enddraw = 8 + offset2
                vstartdraw = 0
                venddraw = 1
            elif i == 1:
                no_trucks = 3
                starty = 100
                j = 0
                startdraw = 3
                enddraw = 8 + offset2
                vstartdraw = 0
                venddraw = 1
            elif i == 2:
                no_trucks = 3
                starty = 150
                j = 0
                startdraw = 4
                enddraw = 8 + offset2
                vstartdraw = 0
                venddraw = 1
            elif i == 3:
                no_trucks = 4   # for positioning trucks on diagram
                starty = 50
                j = 0
                startdraw = -6 + n + offset2
                enddraw = 3.4 + n
                vstartdraw = 0
                venddraw = 1
            # elif i == 4:
            #     no_trucks = 5
            #     starty = 50
            #     j = 0
            #     startdraw = 2 + offset + offset2 - n
            #     enddraw = 8
            #     vstartdraw = 0
            #     venddraw = 1
            # elif i == 5:
            #     no_trucks = 3
            #     starty = 100
            #     j = 0
            #     startdraw = 3 + offset + offset2
            #     enddraw = 8
            #     vstartdraw = 0
            #     venddraw = 1
            # elif i == 6:
            #     no_trucks = 3
            #     starty = 150
            #     j = 0
            #     startdraw = 3 + offset + offset2
            #     enddraw = 8
            #     vstartdraw = 0
            #     venddraw = 1

            offset4 = (n + 1.4) * space_per_peg
            offset5 = (n + 1.4) * space_per_peg

            if i == 0 or i == 1 or i == 2 or i == 3:
                pygame.draw.line(screen, (0,0,0), (offset5 + startx + startdraw * space_per_peg,starty+peg_height),
                                 (startx + enddraw * space_per_peg, starty+peg_height), 2)
            if i == 0 or i == 1 :
                pygame.draw.line(screen, (0,0,0), (offset4 +startx+ startdraw * space_per_peg + vstartdraw * space_per_peg,starty+peg_height ),
                                 (offset4 + startx + startdraw * space_per_peg + venddraw * space_per_peg, starty+peg_height+50), 2)
            #draw the sensor markers
            if i <= 3:
                if i == 0: marker_val = 4.8
                elif i == 1: marker_val = 3.8
                elif i == 2: marker_val = 2.8
                elif i == 3: marker_val = 0.1
                pygame.draw.line(screen, (255,0,0), (startx + (enddraw-marker_val) * space_per_peg, starty+peg_height),
                                 (startx + (enddraw-marker_val) * space_per_peg, starty+peg_height-10), 2)


        if 'decide_what_to_do_instruction' in globals():
            startx = 15
            starty = 100
            msg = decide_what_to_do_instruction
            self.display_Instruction(msg, startx, starty, screen, 16)
            startx = 15
            starty += 25
            msg = decide_what_to_do_instruction2
            self.display_Instruction(msg, startx, starty, screen,16)
            startx += 0
            starty += 25
            msg = decide_what_to_do_instruction2a
            self.display_Instruction(msg, startx, starty, screen,15)
            startx = 15
            starty += 30
            msg = decide_what_to_do_instruction1
            self.display_Instruction(msg, startx, starty, screen, 16)
            startx += 0
            starty += 25
            msg = decide_what_to_do_instruction1a
            self.display_Instruction(msg, startx, starty, screen,14)

        pygame.display.update()
        time.sleep(sleeping_interval)


    def set_positions_of_trucks(self, distribute_trucks, item_no = 1 ):

        # print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ set positions of trucks $$$$$$$$$$$$$$$$$$$$$$$$$$$$"
        # print "self.no_trucks", self.no_trucks
        # [no_trucks_short, no_trucks_long, no_trucks_total] = self.no_trucks

        if distribute_trucks:
            print "DISTRIBUTION"
            positions_of_trucks = self.set_positions_of_trucks_distribution()
        else:
            print "NO DISTRIBUTION"
            positions_of_trucks = self.set_positions_of_trucks_no_distribution(item_no)

        return positions_of_trucks

    def set_positions_of_trucks_no_distribution(self, item_no = 1 ):

        # [no_trucks_short, no_trucks_long, no_trucks_total] = self.no_trucks
        item_no = int(item_no)
        if self.no_trucks_long == 5:
            # print "************** item_no" , item_no, type(item_no)
            if item_no == 1:
                # print("item_no == 1")
                positions_of_trucks = [deque([5, 2, 1, 3, 4]), deque([6, 7, 8]), deque([]), deque([0]), deque(), deque(), deque()]
                positions_of_trucks = [deque([2, 6, 3, 8, 4]), deque([5, 7, 1]), deque([]), deque([0]), deque(), deque(), deque()]
                positions_of_trucks = [deque([4, 2, 5, 1, 3]), deque([6, 7, 8]), deque([]), deque([0]), deque(), deque(), deque()]
                positions_of_trucks = [deque([4, 2, 5]), deque([6, 7, 8]), deque([1, 3]), deque([0]), deque(), deque(), deque()]
                positions_of_trucks = [deque([8,7,6,5,4]), deque([3,2,1]), deque([]), deque([0]), deque(), deque(), deque()]
            elif item_no == 2:
                # print("item_no == 2")
                positions_of_trucks = [deque([1, 5, 3, 4, 2]), deque([6, 7, 8]), deque([]), deque([0]), deque(), deque(), deque()]
            elif item_no == 3:
                positions_of_trucks = [deque([4, 2, 5, 1, 3]), deque([6, 7, 8]), deque([]), deque([0]), deque(), deque(), deque()]
            elif item_no == 4:
                positions_of_trucks = [deque([3, 2, 8, 5, 1]), deque([6, 7]), deque([4]), deque([0]), deque(), deque(), deque()]
            elif item_no == 5:
                positions_of_trucks = [deque([4, 2, 1, 3, 5]), deque([6, 7, 8]), deque([]), deque([0]), deque(), deque(), deque()]
            elif item_no == 6:
                positions_of_trucks = [deque([2, 6, 3, 8, 4]), deque([5, 7, 1]), deque([]), deque([0]), deque(), deque(), deque()]
            elif item_no == 7:
                positions_of_trucks = [deque([2, 7, 3, 8, 4]), deque([6, 5, 1]), deque([]), deque([0]), deque(), deque(), deque()]
            elif item_no == 8:
                positions_of_trucks = [deque([2, 6, 3, 8, 4]), deque([7, 1, 5]), deque([]), deque([0]), deque(), deque(), deque()]
            elif item_no == 9:
                positions_of_trucks = [deque([2, 6, 3, 8, 4]), deque([]), deque([5, 7, 1]), deque([0]), deque(), deque(), deque()]
            elif item_no == 10:
                positions_of_trucks = [deque([2, 7, 3, 8, 4]), deque([]), deque([6, 5, 1]), deque([0]), deque(), deque(), deque()]
            elif item_no == 11:
                positions_of_trucks = [deque([2, 6, 3, 8, 4]), deque([]), deque([7, 1, 5]), deque([0]), deque(), deque(), deque()]
            else:
                print "error"
                positions_of_trucks = [deque([2, 6, 3, 8, 4]), deque([]), deque([5, 7, 1]), deque([0]), deque(), deque(), deque()]


        elif self.no_trucks_long == 4:
            if self.no_trucks_short == 3:
                if item_no == 1:
                    # print("item_no == 1")
                    positions_of_trucks = [deque([4, 2, 1, 3]), deque([6, 7, 5]), deque([]), deque([0]), deque(), deque(), deque()]
                elif item_no == 2:
                    # print("item_no == 2")
                    positions_of_trucks = [deque([1, 4, 3, 5]), deque([6, 7, 2]), deque([]), deque([0]), deque(), deque(), deque()]
                elif item_no == 3:
                    positions_of_trucks = [deque([5, 2, 4, 1]), deque([6, 7, 3]), deque([]), deque([0]), deque(), deque(), deque()]
                elif item_no == 4:
                    positions_of_trucks = [deque([1, 3, 2, 4]), deque([5, 6, 7]), deque([5]), deque([0]), deque(), deque(), deque()]
                elif item_no == 5:
                    positions_of_trucks = [deque([5, 2, 1, 3]), deque([4, 6, 7]), deque([]), deque([0]), deque(), deque(), deque()]
                elif item_no == 6:
                    positions_of_trucks = [deque([2, 7, 3, 5]), deque([6, 4, 1]), deque([]), deque([0]), deque(), deque(), deque()]
                elif item_no == 7:
                    positions_of_trucks = [deque([2, 7, 3, 5]), deque([6, 1, 4]), deque([]), deque([0]), deque(), deque(), deque()]
                elif item_no == 8:
                    positions_of_trucks = [deque([2, 6, 3, 5]), deque([]), deque([4, 7, 1]), deque([0]), deque(), deque(), deque()]
                elif item_no == 9:
                    positions_of_trucks = [deque([2, 7, 3, 5]), deque([]), deque([6, 4, 1]), deque([0]), deque(), deque(), deque()]
                elif item_no == 10:
                    positions_of_trucks = [deque([2, 6, 3, 5]), deque([]), deque([7, 1, 4]), deque([0]), deque(), deque(), deque()]
                else:
                    print "error"
                    positions_of_trucks = [deque([2, 6, 3, 5]), deque([]), deque([4, 7, 1]), deque([0]), deque(), deque(), deque()]
            elif self.no_trucks_short == 2:
                if item_no == 1:
                    # print("item_no == 1")
                    positions_of_trucks = [deque([4, 2, 1, 3]), deque([6, 5]), deque([]), deque([0]), deque(), deque(), deque()]
                elif item_no == 2:
                    # print("item_no == 2")
                    positions_of_trucks = [deque([1, 4, 3, 5]), deque([6, 2]), deque([]), deque([0]), deque(), deque(), deque()]
                elif item_no == 3:
                    positions_of_trucks = [deque([5, 2, 4, 1]), deque([6, 3]), deque([]), deque([0]), deque(), deque(), deque()]
                elif item_no == 4:
                    positions_of_trucks = [deque([1, 3, 2, 4]), deque([5, 6]), deque([]), deque([0]), deque(), deque(), deque()]
                elif item_no == 5:
                    positions_of_trucks = [deque([5, 2, 1, 3]), deque([4, 6]), deque([]), deque([0]), deque(), deque(), deque()]
                elif item_no == 6:
                    positions_of_trucks = [deque([2, 6, 3, 5]), deque([1, 4]), deque([]), deque([0]), deque(), deque(), deque()]
                elif item_no == 7:
                    positions_of_trucks = [deque([2, 6, 3, 5]), deque([]), deque([4, 1]), deque([0]), deque(), deque(), deque()]
                elif item_no == 8:
                    positions_of_trucks = [deque([2, 6, 3, 5]), deque([]), deque([1, 4]), deque([0]), deque(), deque(), deque()]
                else:
                    print "error"
                    positions_of_trucks = [deque([2, 1, 3, 5]), deque([4, 6]), deque([]), deque([0]), deque(), deque(), deque()]
            else:
                positions_of_trucks = [deque([2, 1, 3, 5]), deque([4, 6]), deque([]), deque([0]), deque(), deque(), deque()]
        elif self.no_trucks_long == 3:
            if item_no == 1:
                # print("item_no == 1")
                positions_of_trucks = [deque([3, 2, 1]), deque([4]), deque([]), deque([0]), deque(), deque(), deque()]
            elif item_no == 2:
                # print("item_no == 2")
                positions_of_trucks = [deque([1, 3, 4]), deque([2]), deque([]), deque([0]), deque(), deque(), deque()]
            elif item_no == 3:
                positions_of_trucks = [deque([4, 2, 3]), deque([1]), deque([]), deque([0]), deque(), deque(), deque()]
            elif item_no == 4:
                positions_of_trucks = [deque([2, 1, 4]), deque([3]), deque([]), deque([0]), deque(), deque(), deque()]
            else:
                print "error"
                positions_of_trucks = [deque([2, 1, 4]), deque([4]), deque([]), deque([0]), deque(), deque(), deque()]
        else:
            positions_of_trucks = None

        return positions_of_trucks

    def set_positions_of_trucks_distribution(self):

        # [no_trucks_short, no_trucks_long, no_trucks_total] = self.get_no_trucks()

        if self.no_trucks_long == 5:
            # positions_of_trucks = [deque([]), deque([]), deque([]), deque([]), deque([0,1,2,3,4,5,6,7,8]), deque(), deque()]
            positions_of_trucks = [deque([]), deque([]), deque([]), deque([0,1,2,3,4,5,6,7,8]), deque(), deque(), deque()]
        elif no_trucks_long == 4:
            if self.no_trucks_short == 3:
                positions_of_trucks = [deque([]), deque([]), deque([]), deque([]), deque([0,1,2,3,4,5,6,7]), deque(), deque()]
            elif self.no_trucks_short == 2:
                positions_of_trucks = [deque([]), deque([]), deque([]), deque([]), deque([0,1,2,3,4,5,6]), deque(), deque()]
        elif self.no_trucks_long == 3:
            positions_of_trucks = [deque([]), deque([]), deque([]), deque([]), deque([0,1,2,3,4]), deque(), deque()]
        else:
            positions_of_trucks = None

        return positions_of_trucks

    # def distribute_trucks(self):
    #
    #     print "distribute_trucks inglenookMaster"
    #     # no_trucks = self.get_no_trucks()
    #
    #     # assume trucks have been backed up to siding_long
    #
    #     # note position
    #
    #
    #     # need to distribute them
    #     [no_trucks_short, no_trucks_long, no_trucks_total] = self.get_no_trucks()
    #     print "distribute_trucks2"
    #     [turnout_short, turnout_long, turnout_main] = self.get_sidings()
    #     [turnout_short_direction, turnout_long_direction, turnout_main_direction] = self.get_turnout_directions()
    #
    #     # put no_trucks_long on siding_long
    #
    #     no_trucks_to_move = no_trucks_long
    #     destBranch = 1      # siding_long
    #     fromBranch = 5      # sput
    #
    #     for p in self.moveTrucksCreatingYieldStatements(no_trucks_to_move, fromBranch, destBranch): yield p
    #     print "distribute_trucks3"
    #     # put rest of trucks on siding 2
    #
    #     no_trucks_to_move = no_trucks_short
    #     destBranch = 2     # sput
    #     fromBranch = 5      # siding_long
    #
    #     for p in self.moveTrucksCreatingYieldStatements(no_trucks_to_move, fromBranch, destBranch): yield p
    #
    #     # put rest on siding_short
    #
    #     no_trucks_to_move = no_trucks_short
    #     destBranch = 4      # sput
    #     fromBranch = 1      # siding_long
    #
    #     for p in self.moveTrucksCreatingYieldStatements(no_trucks_to_move, fromBranch, destBranch): yield p

    def determine_required_positions_of_trucks(self, positions_of_trucks, size_long_siding, size_short_sidings, distribute_trucks):

        #if we are running the real simulation, then we need to distribute the trucks first

        # print "yield_required_positions_of_trucks", positions_of_trucks
        yield positions_of_trucks
        # print "determine_required_positions_of_trucks2"

        ingle = Inglenook(positions_of_trucks, size_long_siding, size_short_sidings)  # class Inglenook
        if distribute_trucks:        # train comes into sidings from main with all the trucks
            print "distributing trucks"
            for p in ingle.distribute_trucks():
                yield p
        # now run the shunting puzzle
        ingle = Inglenook(positions_of_trucks, size_long_siding, size_short_sidings)  # class Inglenook
        # print "set up ingle"
        # don't need these
        # ingle.init_position_branch()
        # print "calling solvePuzzle1"
        for p in ingle.solvePuzzle():
            if p[0] != "display_message":
                # print "!!!!yielded p" , p
                pass
            yield p
        # print "end of determine_required_positions_of_trucks"




    def display_trucks_in_siding(self, siding_no, truck_nos):
        siding_no_1 = 3-siding_no
        #reset truck_states
        for editor in jmri.InstanceManager.getDefault(jmri.jmrit.display.EditorManager).getAll():
            contents = editor.getContents()   #returns list Positionable
            for item in contents:
                item_name = item.getName()
                if item_name != None:
                    if item_name.startswith("TruckIndication_" + str(siding_no_1)) or \
                        item_name.startswith("TruckIndication_" + "spur"):
                        item.setText("")
                        item.displayState(INACTIVE)


        #update the array
        for truck_position, truck_no in enumerate(truck_nos):
            if siding_no_1 != 0:
                truck_sensor_name = "TruckIndication_"+ str(siding_no_1) + "_" + str(truck_position)
            else:
                truck_sensor_name = "TruckIndication_"+ "spur" + "_" + str(truck_position)
            # print "truck_sensor_name", truck_sensor_name
            for editor in jmri.InstanceManager.getDefault(jmri.jmrit.display.EditorManager).getAll():
                contents = editor.getContents()   #returns list Positionable
                for item in contents:
                    item_name = item.getName()
                    if item_name != None:
                        if item_name == truck_sensor_name:
                            # print ("item_name", item_name)
                            # print "found it"
                            # print "textActive", item.getTextActive()
                            item.setText(str(truck_no))
                            item.displayState(ACTIVE)

    def display_pile_of_pegs(self, pegs, siding_no, max_no_trucks, start_x, start_y, peg_height, screen, base_width, space_per_peg, show_mid_branch):
        """
        Given a pile of pegs, displays them on the screen.
        """
        global place_trucks_near_disconnect_siding
        # siding_no starts at 0
        #print ("display", pegs, max_no_trucks, start_x, start_y, peg_height, screen, base_width, space_per_peg)
        no_items = len(pegs)
        for pegno, pegwidth in enumerate(pegs):
            max = max_no_trucks
            len1 = no_items
            pos = pegno
            peg = max - len1 + pos
            pw = 2.0*float(base_width)* 8.0/3.0 + float(pegwidth)* float(base_width)/3.0  #make the decrease in width smaller
            # if ((siding_no == 3 and not show_mid_branch) or (siding_no == 4 and show_mid_branch and place_trucks_near_disconnect_siding == False)):
            if ((siding_no >= 3 and not show_mid_branch) or (siding_no == 4 and place_trucks_near_disconnect_siding)):
                x_coord = start_x + space_per_peg * peg + (space_per_peg - pw) / 2
                if siding_no == 3: x_coord += space_per_peg
                if siding_no == 6: x_coord += space_per_peg
            # elif (siding_no < 3):
            #     print("x",siding_no,max,len1,pos,peg)
            #     x_coord = start_x + space_per_peg * (max_no_trucks - peg )  + (space_per_peg - pw) / 2

            # elif ((siding_no == 4 and show_mid_branch and place_trucks_near_disconnect_siding) or (siding_no == 3)):
            #     #x_coord = start_x + space_per_peg * (pegno + (max_no_trucks-no_items )) + (space_per_peg - pw) / 2
            #     x_coord = start_x + space_per_peg * pegno + (space_per_peg - pw) / 2
            # elif siding_no == 2 or siding_no == 1:
            #     x_coord = start_x + space_per_peg * (pegno + no_items - max_no_trucks) + (space_per_peg - pw) / 2
            else:
                x_coord = start_x + space_per_peg * (max_no_trucks - peg ) + (space_per_peg - pw) / 2
                if siding_no == 1: x_coord += space_per_peg
                if siding_no == 3: x_coord += space_per_peg
            if pegwidth != 9:
                pygame.draw.rect(
                    screen,
                    # Smaller pegs are lighter in color
                    #(255-pegwidth*base_width, 255-pegwidth*base_width, 255-pegwidth*base_width),
                    (255 - 100, 255 - 50, 255 - 50),
                    #pyj2d.locals.blue,
                    (
                        x_coord , # Handles alignment putting pegs in the middle, like a pyramid
                        start_y, #- peg_height * i,         # Pegs are one on top of the other, height depends on iteration
                        pw,
                        peg_height
                    )
                )
            else:
                # draw transparent (9 represents empty space)
                pygame.draw.rect(
                    screen,
                    (255, 0, 0),
                    (
                        x_coord , # Handles alignment putting pegs in the middle, like a pyramid
                        start_y, #- peg_height * i,         # Pegs are one on top of the other, height depends on iteration
                        pw,
                        peg_height
                    )
                )

            # draw the truck number
            font = pygame.font.SysFont('Arial', 16, True)

            if (siding_no >= 3):
                 x_coord = start_x + space_per_peg * peg + (space_per_peg - pegwidth * base_width) / 2 + pegwidth * base_width / 2 - base_width / 3
                 if siding_no == 3: x_coord += space_per_peg
                 if siding_no == 6: x_coord += space_per_peg
            else:
                # arrange trucks from right
                x_coord = start_x + space_per_peg * (max_no_trucks - peg ) + (space_per_peg - pegwidth * base_width) / 2 + pegwidth * base_width / 2 - base_width / 3
                if siding_no == 1: x_coord += space_per_peg
            # draw the number
            x_coord -= space_per_peg * 0.1
            y_coord = start_y
            black = (0,0,0)
            if pegwidth == 0:
                number = "E"
            elif pegwidth == 9:
                number = ""
            else:
                number = pegwidth
            screen.blit(font.render(str(number), True, black), (x_coord, y_coord))

    def display_Instruction(self, msg, xcoord, ycoord, screen, font):
        font = pygame.font.SysFont('Arial', font, True)
        black = (0,0,0)
        screen.blit(font.render(str(msg), True, black), (xcoord, ycoord))


