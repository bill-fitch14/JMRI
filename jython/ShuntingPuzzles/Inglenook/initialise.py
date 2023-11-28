import jmri
from InglenookSystem import get_no_trucks, get_turnout_direction
import inglenookMaster
from move_train import Move_train2
from collections import deque


#
# assume we have backed a train with the correct number of trucks to the sensor with the longest siding
#
# we put the correct number of trucks in each siding, and move the engine to siding spur
#

# find the number of trucks that have been specified in the setup of the Inglenook system
#

class Initialise:

    def __init__(self):
        self.IM = inglenookMaster()
        self.train = Move_train2()

    def get_no_trucks(self):

        ntrucksstr = "%no_trucks_"+ "long" +"^^%"
        no_trucks_short = get_no_trucks(ntrucksstr)

        ntrucksstr = "%no_trucks_"+ "long" +"^^%"
        no_trucks_long = get_no_trucks(ntrucksstr)

        ntrucksstr = "%no_trucks_"+ "total" +"^^%"
        no_trucks_total = get_no_trucks(ntrucksstr)

        return [no_trucks_short, no_trucks_long, no_trucks_total]

    def get_sidings(self):

        [turnout_short, turnout_long, turnout_main] = ["turnout_short", "turnout_long", "turnout_main"]

        # msg = "turnout to 1 & 2"
        # siding = "#IS_"+msg.replace(" ","").replace("to","_").replace("&","")+"#"
        # turnout_short = get_siding_turnout(siding)
        #
        # msg = "turnout to 3    "
        # siding = "#IS_"+msg.replace(" ","").replace("to","_").replace("&","")+"#"
        # turnout_long = get_siding_turnout(siding)
        #
        # msg = "turnout to main "
        # siding = "#IS_"+msg.replace(" ","").replace("to","_").replace("&","")+"#"
        # turnout_main = get_siding_turnout(siding)

        return [turnout_short, turnout_long, turnout_main]

    def get_turnout_directions(self):

        [turnout_short_dir, turnout_long_dir, turnout_main_dir] = self.get_turnout_dir_str()

        turnout_short_direction = get_turnout_direction(turnout_short_dir)
        turnout_long_direction = get_turnout_direction(turnout_long_dir)
        turnout_main_direction = get_turnout_direction(turnout_main_dir)

        return [turnout_short_direction, turnout_long_direction, turnout_main_direction]

    def get_turnout_dir_str(self):

        turnout_dir_str = ["dir to long", "dir to 2", "dir to main"]
        return turnout_dir_str

    # RunInglenookMaster()
    #
    # train = Move_train2()
    # train.decide_what_to_do_first()       # initialise

    def run(self):
        # get trucks and turnouts

        [no_trucks_short, no_trucks_long, no_trucks_total] = self.get_no_trucks()
        [turnout_short, turnout_long, turnout_main] = self.get_sidings()
        [turnout_short_direction, turnout_long_direction, turnout_main_direction] = self.get_turnout_directions()

        # put no_trucks_long on siding_long
        # put rest on siding_short
        # move engine to spur
        positions = self.move_to_initial_position()
        count = 0
        for position in positions:
            print "next position"
            count += 1
            print ("******************", count, position)
            if type(position[0]) is str:
                # this is a command for the train
                self.IM.decide_what_to_do(position)
                self.train.update_position
                if position[0] == "display_message":
                    [instruction, message] = position
                    self.dialogs.displayMessage("msg = : " + message)
            else:
                print("!!!!!!!!!!! this is a command for simulation 1", position)
                # this is a command for pygame simulation
                self.IM.display_trucks_on_insert(position, screen)
                print "display truck on panel"
                self.IM.display_trucks_on_panel(position)
            pygame.display.update()
            print "displayed update"

    def move_to_initial_position(self):


        no_trucks = self.get_no_trucks()

        # assume trucks have been backed up to siding_long

        # note position
        positions_of_trucks = self.set_positions_of_trucks()

        # need to distribute them
        [no_trucks_short, no_trucks_long, no_trucks_total] = self.get_no_trucks()
        [turnout_short, turnout_long, turnout_main] = self.get_sidings()
        [turnout_short_direction, turnout_long_direction, turnout_main_direction] = self.get_turnout_directions()

        # put no_trucks_long on siding_long

        no_trucks_to_move = no_trucks_long
        destBranch = 1      # siding_long
        fromBranch = 4      # sput

        for p in self.moveTrucksCreatingYieldStatements(no_trucks_to_move, fromBranch, destBranch): yield p

        # put rest of trucks on siding 2

        no_trucks_to_move = 0
        destBranch = 4      # sput
        fromBranch = 1      # siding_long

        for p in self.moveTrucksCreatingYieldStatements(no_trucks_to_move, fromBranch, destBranch): yield p

        # put rest on siding_short

        no_trucks_to_move = no_trucks_total - no_trucks_long
        destBranch = 4      # sput
        fromBranch = 1      # siding_long

        for p in self.moveTrucksCreatingYieldStatements(no_trucks_to_move, fromBranch, destBranch): yield p

# move engine to spur
Initialise = Initialise()








