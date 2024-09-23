import jmri

import threading
# import move_train_init as i
# import move_train_helper as h
# import move_train_call as ccc
# import move_train_recovery_helper as r2
# # import move_train_countActive as ca
# import move_train_count as c
# import move_train_recoverActive as ra
# import move_train_recoverInactive as ri
import inspect
import config as co
from threading import Thread
import globals as glb
from timeout import alternativeaction, variableTimeout, print_name, timeout
from javax.swing import JOptionPane, JFrame, JLabel, JButton, JTextField, JFileChooser, JMenu, JMenuItem, JMenuBar,JComboBox,JDialog,JList

threading_local = threading.local()

# New method of splitting files
# https://stackoverflow.com/questions/35059904/splitting-python-class-into-multiple-files

# The below list of methods are in Move_Train but have been moved to seperate files for housekeeping purposed

# unfortunately modules requiring use of jmri AbstractAutomaton tools need to remain in the main routine (such as sensors)

# def add_methods(*methods):
#     def decorator(Class):
#         for method in methods:
#             setattr(Class, method.__name__, method)
#         return Class
#     return decorator

# @add_methods(i.myprint,i.myprint1,i.myprint2,i.indent,i.dedent)
# @add_methods(r2.storeSensorFrom, r2.storeSensorTo, r2.storeSensor, r2.storeFunction, r2.storeCount, r2.storeTimeout)
# @add_methods(ccc.place_trucks_near_disconnect)
# @add_methods(ccc.moveTrucksOneByOne)
# @add_methods(ccc.count_at_spur)
# @add_methods(ccc.moveToDisconnectPosition, ccc.move_to_spur_operations, ccc.move_to_siding_operations, ccc.strip_0)
# @add_methods(c.countTrucksInactive, c.countTrucksActive)
# @add_methods(h.setPointsAndDirection, h.setBranch, h.setMidBranch, h.setSensor)
# @add_methods(h.couple1, h.uncouple1)
# @add_methods(h.swapRouteSameDirectionTravelling,h.swapRouteOppDirectionTravelling,h.sensorName,h.stateName)
# @add_methods(h.noTrucksOnBranches, h.noTrucksOnBranch, h.moveDistance)
#@add_methods(r.returnToBranch)
# @add_methods(ca.moveToBranch, ca.countTrucksActive, ca.waitChangeSensorActive)
#@add_methods(ca.moveToBranch, ca.countTrucksActive)
#@add_methods(ci.countTrucksInactive, ci.waitChangeSensorInactive)

# @add_methods(ri.alt_action_countTrucksInactive)
# @add_methods(ra.alt_action_countTrucksActive2, ra.returnToBranch, ra.countTrucksAgain)



class OptionDialog( jmri.jmrit.automat.AbstractAutomaton ) :
    CLOSED_OPTION = False
    logLevel = 0

    def List(self, title, list_items):
        list = JList(list_items)
        list.setSelectedIndex(0)
        i = []
        self.CLOSED_OPTION = False
        options = ["OK"]
        while len(i) == 0:
            s = JOptionPane.showOptionDialog(None,
                                             list,
                                             title,
                                             JOptionPane.YES_NO_OPTION,
                                             JOptionPane.PLAIN_MESSAGE,
                                             None,
                                             options,
                                             options[0])
            if s == JOptionPane.CLOSED_OPTION:
                self.CLOSED_OPTION = True
                if self.logLevel > 1 : print "closed Option"
                return
            i = list.getSelectedIndices()
        index = i[0]
        return list_items[index]


    #list and option buttons
    def ListOptions(self, list_items, title, options):
        list = JList(list_items)
        list.setSelectedIndex(0)
        self.CLOSED_OPTION = False
        s = JOptionPane.showOptionDialog(None,
                                         list,
                                         title,
                                         JOptionPane.YES_NO_OPTION,
                                         JOptionPane.PLAIN_MESSAGE,
                                         None,
                                         options,
                                         options[1])
        if s == JOptionPane.CLOSED_OPTION:
            self.CLOSED_OPTION = True
            return
        index = list.getSelectedIndices()[0]
        return [list_items[index], options[s]]

        # call using
        # list_items = ["list1","list2"]
        # options = ["opt1", "opt2", "opt3"]
        # title = "title"
        # result = OptionDialog().ListOptions(list_items, title, options)
        # list= result[0]
        # option = result[1]
        # print "option= " ,option, " list = ",list

    def variable_combo_box(self, options, default, msg, title = None, type = JOptionPane.QUESTION_MESSAGE):


        result = JOptionPane.showInputDialog(
            None,                                   # parentComponent
            msg,                                    # message text
            title,                                  # title
            type,                                   # messageType
            None,                                   # icon
            options,                                # selectionValues
            default                                 # initialSelectionValue
        )

        return result


    def displayMessage2(self, msg, title = ""):
        self.displayMessage(msg, "", False)
    def displayMessage1(self, msg, title = ""):
        self.displayMessage(msg, "", False)

    def displayMessage(self, msg, title = "", display = False):
        global display_message_flag

        if 'display_message_flag' not in globals():
            display_message_flag = True

        # if display_message_flag:
        if display:

            s = JOptionPane.showOptionDialog(None,
                                             msg,
                                             title,
                                             JOptionPane.YES_NO_OPTION,
                                             JOptionPane.PLAIN_MESSAGE,
                                             None,
                                             ["OK"],
                                             None)
            if s == JOptionPane.CLOSED_OPTION:
                title = "choose"
                opt1 = "continue"
                opt2 = "stop system"
                msg = "you may wish to abort"
                s1 = self.customQuestionMessage2str(msg, title, opt1, opt2)
                if s1 == opt2:
                    #stop system
                    Mywindow2()
                    StopMaster().stop_all_threads()

                return s
            #JOptionPane.showMessageDialog(None, msg, 'Message', JOptionPane.WARNING_MESSAGE)
            return s
        #     print "display_message_flag ", display_message_flag
        # else:
        #     print "display_message_flag ", display_message_flag

    def customQuestionMessage(self, msg, title, opt1, opt2, opt3):
        self.CLOSED_OPTION = False
        options = [opt1, opt2, opt3]
        s = JOptionPane.showOptionDialog(None,
                                         msg,
                                         title,
                                         JOptionPane.YES_NO_CANCEL_OPTION,
                                         JOptionPane.QUESTION_MESSAGE,
                                         None,
                                         options,
                                         options[2])
        if s == JOptionPane.CLOSED_OPTION:
            self.CLOSED_OPTION = True
            return
        return s

    def customQuestionMessage3str(self, msg, title, opt1, opt2, opt3):
        self.CLOSED_OPTION = False
        options = [opt1, opt2, opt3]
        s = JOptionPane.showOptionDialog(None,
                                         msg,
                                         title,
                                         JOptionPane.YES_NO_CANCEL_OPTION,
                                         JOptionPane.QUESTION_MESSAGE,
                                         None,
                                         options,
                                         options[0])
        if s == JOptionPane.CLOSED_OPTION:
            self.CLOSED_OPTION = True
            return
        if s == JOptionPane.YES_OPTION:
            s1 = opt1
        elif s == JOptionPane.NO_OPTION:
            s1 = opt2
        else:
            s1 = opt3
        return s1

    def customQuestionMessage2(self, msg, title, opt1, opt2):
        self.CLOSED_OPTION = False
        options = [opt1, opt2]
        s = JOptionPane.showOptionDialog(None,
                                         msg,
                                         title,
                                         JOptionPane.YES_NO_OPTION,
                                         JOptionPane.QUESTION_MESSAGE,
                                         None,
                                         options,
                                         options[0])
        if s == JOptionPane.CLOSED_OPTION:
            self.CLOSED_OPTION = True
            return
        return s

    def customQuestionMessage2str(self, msg, title, opt1, opt2):
        self.CLOSED_OPTION = False
        options = [opt1, opt2]
        s = JOptionPane.showOptionDialog(None,
                                         msg,
                                         title,
                                         JOptionPane.YES_NO_OPTION,
                                         JOptionPane.QUESTION_MESSAGE,
                                         None,
                                         options,
                                         options[1])
        if s == JOptionPane.CLOSED_OPTION:
            self.CLOSED_OPTION = True
            return
        if s == JOptionPane.YES_OPTION:
            s1 = opt1
        else:
            s1 = opt2
        return s1

    def customMessage(self, msg, title, opt1):
        self.CLOSED_OPTION = False
        options = [opt1]
        s = JOptionPane.showOptionDialog(None,
                                         msg,
                                         title,
                                         JOptionPane.YES_OPTION,
                                         JOptionPane.PLAIN_MESSAGE,
                                         None,
                                         options,
                                         options[0])
        if s == JOptionPane.CLOSED_OPTION:
            self.CLOSED_OPTION = True
            return
        return s

    def input(self,msg, title, default_value):
        options = None
        x = JOptionPane.showInputDialog( None, msg,title, JOptionPane.QUESTION_MESSAGE, None, options, default_value);
        #x = JOptionPane.showInputDialog(None,msg)
        return x

print_details = False

class Move_train2(jmri.jmrit.automat.AbstractAutomaton):

    # responds to the simulateInglenookSensor, and allows the Inglenook Siding Routine to start

    logLevel = 1
    tender = False
    indentno = 0
    # print_detailed = 'False'

    #set up variables to use timeout decorator
    sensor_name = "sensor_stored"
    sensor_from_name = "sensor_from_stored"
    sensor_to_name = "sensor_to_stored"
    timeout_name = "timeout_stored"

    # myWindows = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/inglenook/myWindows.py')

    point3 = None
    #instanceList = []   # List of file based instances

    display_message_flag = False

    def __init__(self):
        self.spur_branch = 4 # count from `1
        # self.mid_branch = 5
        self.spurPeg = 3    # count from 0
        # self.midPeg = 4
        self.pegs = []

        self.stop_thread_sensor = sensors.getSensor("stopThreadSensor")
        self.stop_thread_sensor.setKnownState(INACTIVE)
        self.stop_thread = False

    def init(self):
        global gbl_simulate_sensor_wait_time
        global indentno
        global decide_what_to_do_instruction, decide_what_to_do_instruction1, decide_what_to_do_instruction1a
        global decide_what_to_do_instruction2, decide_what_to_do_instruction2a
        # print "setup"
        self.logLevel = 0
        if self.logLevel > 0: print 'Create Stop Thread'
        gbl_simulate_sensor_wait_time = 1000
        indentno = 0
        # print "indentno", indentno
        self.dialogs = OptionDialog()
        decide_what_to_do_instruction = ""
        decide_what_to_do_instruction1 = ""
        decide_what_to_do_instruction1a = ""
        decide_what_to_do_instruction2 = ""
        decide_what_to_do_instruction2a = ""



    def setup(self):
        # print "start move_train setup"
        test_sensor = sensors.getSensor("soundInglenookSensor")
        self.simulate_inglenook_sensor = test_sensor
        if test_sensor is None:
            print "returning False"
            return False
        test_sensor.setKnownState(INACTIVE)
        # print "a"
        self.od = OptionDialog()
        # print "b"
        # self.IS = InglenookSystem()
        # print "c"
        # print "returning True"
        if self.setup_sensors_turnouts():
            # print "sensors and turnouts set"
            return True
        else:
            print "sensors and turnouts not set"
        return False

    def choose_action(self):
        title = ""
        msg = "simulate Inglenook"
        opt1 = "with simulated signals"
        opt2 = "with real signals"
        opt3 = "other actions"
        reply = self.od.customQuestionMessage2str(msg, title, opt1, opt2)
        if self.od.CLOSED_OPTION == True:
            return "cancel"
        if reply == opt1:
            return opt1
        elif reply == opt2:
            return opt2
        else:
            pass


    def setup_sensors_turnouts(self):
        # print ("handle")
        try:
            indentno
            # print "handle` Move`_tran2 indentno set up", indentno
        except NameError:
            print "indentno not set up"

        self.indent()
        # print "move_train handle (sets up sensors)"
        self.myprint("in Move_train init")
        global throttle
        #speeds
        # print "waiting for sensor"
        # mysensor = sensors("simulateSensor")
        # self.waitChangeSensorActive(sensor)
        # self.waitChangeSensorInactive(mysensor)

        self.stop = 0
        self.slow = 0.1
        self.vslow = 0.05
        self.uncouple = 0.15
        self.medium = 0.5
        self.couple = 0.3
        self.fast = 0.7

        self.smallDistance = "smallDistance"

        #sensor States
        self.sensorOn = 1
        self.sensorOff = 0

        self.initialmove = True
        self.myprint("Inside init(self)xx")

        sensorManager = jmri.InstanceManager.getDefault(jmri.SensorManager)
        turnoutManager = jmri.InstanceManager.getDefault(jmri.TurnoutManager)
        # print ("setting up sensors")
        try:
            self.myprint ("trying to set up sensors")

            self.sensor4 = self.get_decoupling_sensor("#IS_headshunt_sensor#")
            self.myprint1 ("trying to set up sensor headshunt", self.sensor4)

            self.sensor1 = self.get_decoupling_sensor("#IS_siding1_sensor#")
            self.myprint1 ("trying to set up sensors1", self.sensor1)

            self.sensor2 = self.get_decoupling_sensor("#IS_siding2_sensor#")
            self.myprint1 ("trying to set up sensors2", self.sensor2)

            self.sensor3 = self.get_decoupling_sensor("#IS_siding3_sensor#")
            self.myprint1 ("trying to set up sensor3", self.sensor3)
            self.myprint1 ("sensore set up")
        except:
            self.myprint1 ("sensors not set!")
            self.od.displayMessage("Cannot Proceed: sensors not set!")
            crash_here
            return False
        # self.myprint2("setting up points")
        # self.myprint ("trying to set up points")
        # self.turnout_long = self.get_turnout()
        # self.turnout_long = turnoutManager.getTurnout("SP-T04")
        # self.turnout_short = turnoutManager.getTurnout("SP-T03")
        # self.turnout_main = turnoutManager.getTurnout("SP-T02")
        # self.myprint ("self.turnout_main" + str( self.turnout_main.getUserName()))
        # self.myprint1 ("points set up")
        self.od.displayMessage("trying turnouts")
        state = 0
        try:
            [turnout_long_str, turnout_short_str,   turnout_main_str] = self.get_turnout_str()
            self.myprint ("trying to set up points")
            state = 0
            turnout_long_id = self.get_turnout(turnout_long_str)
            state = 1
            turnout_short_id = self.get_turnout(turnout_short_str)
            state = 2
            turnout_main_id = self.get_turnout(turnout_main_str)
            state = 3

            self.turnout_long = turnouts.getTurnout(turnout_long_id)
            state = 4
            self.turnout_short = turnouts.getTurnout(turnout_short_id)
            state = 5
            self.turnout_main = turnouts.getTurnout(turnout_main_id)
            state = 6
            self.myprint ("turnouts set up")
        except:
            self.myprint1 ("turnouts not set!")
            self.od.displayMessage("turnouts not set")
            # print ("turnouts not set!", "state = ", state, "turnout_long_id", turnout_long_id, "turnout_short_id", turnout_short_id, "turnout_main_id", turnout_main_id)
            #
            return False

        if state != 6:
            OptionDialog().displayMessage("Cannot Proceed: turnouts not set!")
            # print "fred"
        try:
            self.myprint ("trying to set up turnout directions")
            [self.turnout_short_direction, self.turnout_long_direction, self.turnout_main_direction] = self.get_turnout_directions()
        except:
            # print("turnout directions not set up")
            self.dialogs.displayMessage("Cannot Proceed: turnout directions not set!")
            return False



        # get loco address. For long address change "False" to "True"
        # self.myprint("setting up throttle")
        # throttle = self.getThrottle(3, False)  # short address 3
        # self.myprint (throttle)
        # self.set_delay_if_not_simulation(1000)
        # self.setSpeed(self.stop)
        # self.set_delay_if_not_simulation(1000)
        # self.myprint1("throttle set up")
        # "setting up throttle")
        try:
            # print("setting up throttle2")
            # self.myprint1("setting up throttle")
            engine = self.get_engine()
            dccAddress = self.get_dcc_address()
            # print "dccAddress = ", dccAddress, "engine ", engine

            isLong = False
            throttle = self.getThrottle(dccAddress, isLong)  # short address 3
            # print("setting up throttle3")
            # self.myprint (throttle)
            self.set_delay_if_not_simulation(1000)
            self.waitMsec(1000)
            # print("setting up throttle4")
            self.setSpeed(self.stop)
            # print("setting up throttle5")
            self.set_delay_if_not_simulation(1000)
            self.waitMsec(1000)
            self.myprint1("throttle set up")
            # print("throttle set up")
        except:
            self.myprint1("throttle not set up")
            self.myprint2("throttle not set up")

        # sensor = sensors.getSensor("soundInglenookSensor")
        # self.waitSensorActive(sensor)

        self.myprint ("finished init")
        self.myprint(self.__dict__)
        self.myprint(dir())
        # self.dedent()
        # print("end")
        return True

    def get_turnout(turnout_str):
        # print "get_to: qwerty", 'IMIS:the_turnout_' + turnout_str
        turnout = memories.getMemory('IMIS:the_turnout_' + turnout_str)
        if turnout != None:
            # print "$$$$$$$$$$$$$$$$", turnout, 'IMIS:the_turnout_' +turnout_str
            # print "value", turnout.getValue()
            return turnout.getValue()
        else:
            return None

    def get_decoupling_sensor(self, sensor_comment):
        for sensor in sensors.getNamedBeanSet():
            comment = sensor.getComment()
            if comment != None:
                if sensor_comment in comment:
                    return sensor
        return None


    @print_name()
    def decide_what_to_do_first(self, active_sensor):
        # print "calling decide_what_to_do_first in move_train_call"
        self.indent()
        # set up the trucks 5 in branch 3 and 3 in branch 2, and return to branch 4
        # self.noTrucksOnTrain = 0
        if active_sensor == sensors.getSensor("runRealTrainDistributionInglenookSensor") or \
           active_sensor == sensors.getSensor("simulateDistributionInglenookSensor")     :
            self.myprint("decide_what_to_do_first *")

            self.noTrucksOnTrain = 0
            self.previousBranch = self.spur_branch
            # self.noTrucksToMoveFromPreviousStep = 0
            self.numberTrucksToMove_previous = 0

            self.myprint("self.noTrucksOnTrain:" + str(self.noTrucksOnTrain))
            self.myprint("self.previousBranch:" + str(self.previousBranch))
        else:

            # we assume the train is coming from the mainline
            self.myprint("decide_what_to_do_first *")

            self.noTrucksOnTrain = 0
            self.previousBranch = self.spur_branch     # should be mainline branch but we havn't got one
            self.noTrucksToMoveFromPreviousStep = 0
            self.numberTrucksToMove_previous = 0

            self.myprint("self.noTrucksOnTrain:" + str(self.noTrucksOnTrain))
            self.myprint("self.previousBranch:" + str(self.previousBranch))
    @print_name()
    def decide_what_to_do(self, screen, positions, position):
        global display_message_flag
        global decide_what_to_do_instruction
        self.indent()
        self.positions = positions
        self.screen = screen         # for display_update
        self.position = position     # for display_update
        instructions = position

        # self.myprint(instructions)
        [instruction, noTrucksToMove, fromBranch, destBranch, pegs] = position


        if instruction == "move_trucks_one_by_one":

            display_message_flag = True
            self.display_message_flag = True

            if self.pegs == []:
                self.pegs = copy.deepcopy(pegs)  #initialise self.pegs
            else:
                pass # use self.pegs from previous step
            self.myprint1("self.pegs",self.pegs, "pegs", pegs)
            ListOfTrucksInBranches = [len(x) for x in self.pegs]

            # announce action
            self.notrucks = noTrucksToMove
            self.fromBranch = fromBranch
            self.destBranch = destBranch
            decide_what_to_do_instruction = "moveTrucksOneByOne " + str(noTrucksToMove) + "  trucks from " + str(fromBranch) + " to " + str(destBranch)
            self.myprint5("decide_what_to_do_instruction", decide_what_to_do_instruction)
            # self.update_displays(self.pegs)
            self.moveTrucksOneByOne(noTrucksToMove, fromBranch, destBranch, ListOfTrucksInBranches)

        elif instruction == "move_trucks":

            display_message_flag = True
            self.display_message_flag = True

            # announce action
            self.notrucks = noTrucksToMove
            self.fromBranch = fromBranch
            self.destBranch = destBranch
            if self.pegs == []:
                self.pegs = copy.deepcopy(pegs)  #initialise self.pegs
            else:
                pass # use self.pegs from previous step
            stage = "d what to do"
            decide_what_to_do_instruction = "moveTrucks " + str(noTrucksToMove) + " from " + str(fromBranch) + " to " + str(destBranch)
            # print ("decide_what_to_do_instruction", decide_what_to_do_instruction)
            # self.update_displays(self.pegs)
            self.moveTrucks(noTrucksToMove, fromBranch, destBranch, self.pegs)
        else:
            self.myprint("!!!!!!!!!unrecognised instruction " & instruction)
            pass
        self.dedent()
        return self.pegs

    def set_up_display_text(self, stage, deposit, originating_branch, destination_branch):
        global decide_what_to_do_instruction1
        global decide_what_to_do_instruction1a
        global decide_what_to_do_instruction2
        global decide_what_to_do_instruction2a
        msg = "curr: move " + str(stage) + " " + str(deposit) + " trucks from " + str(originating_branch) + \
              " to " + str(destination_branch)
        msg2 = str(self.pegs)
        msg2 = msg2.replace("deque","").replace("[","").replace("]","")
        decide_what_to_do_instruction1 = decide_what_to_do_instruction2.replace("curr","prev")
        decide_what_to_do_instruction1a = decide_what_to_do_instruction2a
        decide_what_to_do_instruction2 = msg
        decide_what_to_do_instruction2a = msg2

    @print_name()
    def moveTrucksOneByOne(self, noTrucksToMove, fromBranch, destBranch, ListOfTrucksInBranches):
        self.indent()

        if self.spur_branch not in [fromBranch, destBranch]:
            noTrucksToMoveInOneGo = 1
            noOfRepetitions = noTrucksToMove
        else: # all can be done in one journey
            noTrucksToMoveInOneGo = noTrucksToMove
            noOfRepetitions = 1
        for i in range(noOfRepetitions):
            self.myprint2(">>>>>movetrucksonebyone  truck", i)
            self.dialogs.displayMessage(">>>>>movetrucksonebyone  truck" + str(i))

            ListOfTrucksInBranches = [len(x) for x in self.pegs]
            self.moveTrucks(noTrucksToMoveInOneGo, fromBranch, destBranch, self.pegs)

            ListOfTrucksInBranches = [len(x) for x in self.pegs]
            self.myprint("ListOfTrucksInBranches after", ListOfTrucksInBranches)
        self.dedent()

    @print_name()
    def moveTrucks(self, numberTrucksToMove, fromBranch, destBranch, pegs):
        # print "in moveTrucks"
        self.indent()
        numberTrucksToMove_old = self.numberTrucksToMove_previous
        stage = "one_move"
        self.myprint3("self.previousBranch", self.previousBranch)
        if self.previousBranch != fromBranch:
            numberTrucksToMove1 = 0
            from_branch = self.previousBranch
            dest_branch = fromBranch
            self.set_up_display_text("stage1", numberTrucksToMove1, from_branch, dest_branch)
            self.myprint3("moving from previous branch to from branch")
            self.moveTrucks2("stage1", from_branch, dest_branch, numberTrucksToMove1, numberTrucksToMove_old, self.pegs)
            numberTrucksToMove_old = numberTrucksToMove1
            stage = "stage2"

        # numberTrucksToMove = numberTrucksToMove_fromBranchToDestBranch
        self.set_up_display_text(stage, numberTrucksToMove, fromBranch, destBranch)
        self.myprint3("moving from from_branch to dest_branch")
        self.moveTrucks2(stage, fromBranch, destBranch, numberTrucksToMove, numberTrucksToMove_old, self.pegs)

        self.previousBranch = destBranch
        self.numberTrucksToMove_previous = numberTrucksToMove

        self.dedent()

    @print_name()
    def moveTrucks2(self, stage, originating_branch, destination_branch, noTrucksToMove, noTrucksToMove_old, pegs):

        # move deposit trucks from originating_branch to destination_branch
        # the number of trucks 'deposited' in the last MoveTrucks2 is stored im deposit_old
        self.indent()

        # go to spur if origin is not the spur
        if originating_branch != self.spur_branch:     # start from a siding, move to spur
            sidingBranch = originating_branch
            self.set_up_display_text("move to spur", noTrucksToMove, originating_branch, self.spur_branch)
            self.move_to_spur_operations(sidingBranch, noTrucksToMove, noTrucksToMove_old)

        # go to siding if destination is a siding
        if destination_branch != self.spur_branch:     # start from spur, move to siding
            sidingBranch = destination_branch
            self.myprint3("go to siding if destination is a siding")
            self.set_up_display_text("move to siding", noTrucksToMove, self.spur_branch, destination_branch)
            self.move_to_siding_operations(sidingBranch, noTrucksToMove)
        self.myprint2(self.pegs)
        self.dedent()
        pass

    def kill_everything(self):
        #this killes everything
        win = Mywindow()
        win.setVisible(1)
        #this prints out what it is killing
        win2 = Mywindow2()
        win2.setVisible(1)


    # def startFromBranch4(self, destBranch, pegs):
    #     self.indent()
    #     self.myprint("In startFromBranch4")
    #     self.noTrucksOnTrain =  self.noTrucksOnStack(pegs, 4)
    #     noTrucksToMove = 0
    #     fromBranch = 4
    #     destBranch = destBranch
    #     self.moveEngineToBranch(noTrucksOnTrain, noTrucksToMove, fromBranch, destBranch)
    #     connectTrucks(fromBranch)
    #     self.dedent()

        # @alternativeaction("alt_action_countTrucksActive2","sensor_stored")
        # @variableTimeout("timeout_stored")


        #@alternativeaction("alt_action_countTrucksInactive",sensor_name)
        #@timeout(3)

        #not used
    # def waitChangeSensor(self, sensor, required_sensor_state):
    #     global gbl_simulate_sensor_wait_time
    #     self.indent()
    #     self.myprint("in waitChangeSensor")
    #     #global config.throttle
    #     self.changeDirection()
    #     self.setSpeed(self.slow)
    #     while 1:
    #         self.myprint("about to waitChangeSensorInactive")
    #         simulate = sensors.getSensor("simulateInglenookSensor")
    #         if simulate.getKnownState() == ACTIVE:
    #             self.waitMsec(gbl_simulate_sensor_wait_time)
    #         else:
    #             self.waitChange([sensor])
    #         got_state = sensor.getKnownState()
    #         self.myprint( ">> moveBackToSensor " + self.stateName(got_state) );
    #         if required_sensor_state == self.sensorOn:
    #             self.myprint( ">> moveBackToSensor" + " sensor state on " + self.stateName(got_state) );
    #             if got_state == ACTIVE:
    #                 self.setSpeed(0)
    #                 #self.set_delay_if_not_simulation(1000)
    #                 self.dedent()
    #                 break
    #             else:
    #                 self.myprint( ">> moveBackToSensor" + " req_sensor_state on " + self.stateName(got_state) );
    #                 pass
    #         elif required_sensor_state == self.sensorOff:
    #             self.myprint( ">> moveBackToSensor" + " sensor state off" );
    #             if got_state == INACTIVE:
    #                 self.setSpeed(0)
    #                 #self.set_delay_if_not_simulation(1000)
    #                 self.dedent()
    #                 break
    #             else:
    #                 self.myprint( ">> moveBackToSensor" + " req_sensor_state off " + self.stateName(got_state) );
    #                 pass
    #         else:
    #             pass
    #     self.dedent()

        #not used
    def alt_action_countTrucksActive1(self,sensor):
        self.indent()
        self.myprint ("in alt_action_countTrucksActive1 ")
        #speak("in alt_action_countTrucksActive1")
        self.myprint ("end alt_action_countTrucksActive1 ")
        self.dedent()

        #not used
    def countTrucks(self, noTrucksToCount, sensor, state_to_use):
        self.indent() #state-to_use can be "ACTIVE" or "INACTIVE"
        self.myprint ("in countTrucks ")
        pass

        #can count 0 to n trucks on active
        #can count 1 to n trucks on inactive

        #check for invalid count
        if state_to_use == "INACTIVE" and noTrucksToCount == 0:
            self.myprint ("!!!!!!!!!!!!!state_to_use == 'INACTIVE' and noTrucksToCount == 0")

        # delay so that we are on a truck then count the number of off events
        self.myprint("counting " + str(noTrucksToCount) + " trucks on " + state_to_use)
        off_count = 0
        on_count = -1
        self.myprint("off_count is " + str(off_count))
        self.myprint("on_count is " + str(on_count))
        while 1:
            self.myprint("waiting change on sensor " + self.sensorName(sensor))
            self.waitChange([sensor])
            sensorstate = sensor.getKnownState()
            self.myprint(">>countTrucks: sensor state is " + self.stateName(sensorstate))
            if sensorstate == INACTIVE and state_to_use == self.stateName(sensorstate):
                self.myprint("off_count is @x " + str(off_count))
                off_count += 1
                self.myprint("off_count is @y " + str(off_count))
                if off_count == noTrucksToCount:
                    self.myprint("Bingo count is " + str(off_count))
                    self.setSpeed(self.stop)
                    self.dedent()
                    break
                else:
                    self.myprint ("off_count is @z " + str(off_count))
                    self.myprint(">>countTrucks: ignoring sensor @1, off_count is " + str(off_count) + " noTrucksToCount " + str(noTrucksToCount))
                    self.myprint(">>countTrucks: ignoring sensor @2, sensor state is " + self.stateName(sensorstate))
            elif sensorstate == ACTIVE and state_to_use == self.stateName(sensorstate):
                on_count+=1
                self.myprint(">>countTrucks: sensor on_count " + self.stateName(sensorstate) + " on_count = " + str(on_count))
                self.myprint("noTrucksToCount " + str(noTrucksToCount))
                if on_count == noTrucksToCount:
                    self.myprint("Bingo on_count is " + str(on_count))
                    self.setSpeed(self.stop)
                    self.dedent()
                    break
                else:
                    self.myprint(">>countTrucks: ignoring sensor @1a, on_count is " + str(on_count) + " noTrucksToCount " + str(noTrucksToCount))
                    self.myprint(">>countTrucks: ignoring sensor @2a, sensor state is " + self.stateName(sensorstate))
            else:
                self.myprint(">>countTrucks: ignoring sensor @1b, off_count is " + str(off_count) + " noTrucksToCount " + str(noTrucksToCount))
                self.myprint(">>countTrucks: ignoring sensor @2b, on_count is " + str(on_count))
                self.myprint(">>countTrucks: ignoring sensor @3b, sensor state is " + self.stateName(sensorstate))
        self.dedent()

        #**********************************************************************************
        # Routines that depend upon globals and cannot be moved to seperate file
        #**********************************************************************************
    def setSpeed(self, speed):
        #global throttle
        self.indent()
        self.myprint("in set speed: setting to " + str(speed))
        if sensors.getSensor("runRealTrainDistributionInglenookSensor").getKnownState() == ACTIVE:
            if throttle.getSpeedSetting() != speed:
                throttle.setSpeedSetting(speed)
                self.myprint("end set speed to " + str(speed))
            else:
                throttle.setSpeedSetting(speed)
                self.myprint("speed already at " + str(speed))

        self.dedent()

    def setSpeedSetDelay(self, speed, delay):
        #global throttle
        self.indent()
        self.myprint("in set speed: setting to " + str(speed))
        if sensors.getSensor("runRealTrainDistributionInglenookSensor").getKnownState() == ACTIVE:
            if throttle.getSpeedSetting() != speed:
                throttle.setSpeedSetting(speed)
                self.myprint("end set speed to " + str(speed) + "with delay " + str(delay))
                self.set_delay_if_not_simulation(delay)
            else:
                self.myprint("speed already at " + str(speed))

        self.dedent()
    @print_name(print_details)
    def setPoints(self, fromBranch, toBranch):
        self.indent()
        self.myprint (">>in setPoints ")

        self.myprint("setting points fromBranch = " + str(fromBranch) + " toBranch = " + str(toBranch))
        self.myprint("get pointx CLOSED")
        self.myprint("self.turnout_main", self.turnout_main)
        self.myprint("self.turnout_main.getState() before" + str(self.turnout_main.getState()))
        self.turnout_main.setState(CLOSED)
        self.myprint("self.turnout_main.getState() after" + str(self.turnout_main.getState()))

        branch_long = 1
        branch_short_2 = 2
        branch_short_1 = 3
        branch_spur = 4

        # if fromBranch == 4:
        #     if toBranch == 1:
        if fromBranch == branch_spur:
            if toBranch == branch_long:
                self.myprint("get point1 CLOSED")
                self.myprint("self.turnout_long.getState() before" + str(self.turnout_long.getState()))
                # if self.turnout_long.getState() != CLOSED:
                # self.myprint("set point1 CLOSED")
                self.set_turnout_long("to_branch_long")
                #self.turnout_long.setState(CLOSED)
                self.myprint("self.turnout_long.getState() after" + str(self.turnout_long.getState()))
            else:
                self.myprint("get point1 THROWN")
                self.myprint("self.turnout_long.getState() before" + str(self.turnout_long.getState()))
                # if self.turnout_long.getState() != THROWN:
                # self.myprint("set point1 THROWN")
                self.set_turnout_long("to_branches_short")
                #self.turnout_long.setState(THROWN)
                self.myprint("self.turnout_long.getState() after" + str(self.turnout_long.getState()))

            self.set_delay_if_not_simulation(3000)

            if toBranch == branch_short_1:
                self.myprint("get point2 CLOSED")
                # if self.turnout_short.getState() != CLOSED:
                # self.myprint("set point2 CLOSED")
                self.set_turnout_short("to_1")
                #self.turnout_short.setState(CLOSED)
                self.set_delay_if_not_simulation(3000)
            elif toBranch == branch_short_2:
                self.myprint("get point2 THROWN")
                self.myprint("self.turnout_short.getState() before" + str(self.turnout_short.getState()))
                # if self.turnout_short.getState() != THROWN:
                # self.myprint("set point2 THROWN")
                self.set_turnout_short("to_2")
                #self.turnout_short.setState(THROWN)
                self.myprint("self.turnout_short.getState() after" + str(self.turnout_short.getState()))
                self.set_delay_if_not_simulation(3000)
            else:
                self.myprint("do not set point2")


        else:
            # if fromBranch == 1:
            if fromBranch == branch_long:
                self.myprint("get point1 CLOSED")
                self.myprint("self.turnout_long.getState() before" + str(self.turnout_long.getState()))
                # if self.turnout_long.getState() != CLOSED:
                # self.myprint("set point1 CLOSED")
                self.set_turnout_long("to_branch_long")
                # self.turnout_long.setState(CLOSED)
                self.myprint("self.turnout_long.getState() after" + str(self.turnout_long.getState()))
            else:
                self.myprint("get point1 THROWN")
                self.myprint("self.turnout_long.getState() before" + str(self.turnout_long.getState()))
                # if self.turnout_long.getState() != THROWN:
                # self.myprint("set point1 THROWN")
                self.set_turnout_long("to_branches_short")
                # self.turnout_long.setState(THROWN)
                self.myprint("self.turnout_long.getState() after" + str(self.turnout_long.getState()))

            self.set_delay_if_not_simulation(3000)

            # if fromBranch == 3:
            if fromBranch == branch_short_1:
                self.myprint("get point2 CLOSED")
                self.myprint("self.turnout_short.getState() before" + str(self.turnout_short.getState()))
                # if self.turnout_short.getState() != CLOSED:
                # self.myprint("set point2 CLOSED")
                self.myprint("self.turnout_short.getState() before" + str(self.turnout_short.getState()))
                self.set_turnout_short("to_branch_1")
                self.turnout_short.setState(CLOSED)
                self.myprint("self.turnout_short.getState() after" + str(self.turnout_short.getState()))
                self.set_delay_if_not_simulation(3000)
            elif fromBranch == branch_short_2:
                self.myprint("get point2 THROWN")
                self.myprint("self.turnout_short.getState() before" + str(self.turnout_short.getState()))
                # if self.turnout_short.getState() != THROWN:
                # self.myprint("set point2 THROWN")
                self.set_turnout_short("to_branch_2")
                # self.turnout_short.setState(THROWN)
                self.myprint("self.turnout_short.getState() after" + str(self.turnout_short.getState()))
                self.set_delay_if_not_simulation(3000)
            else:
                self.myprint("do not set point2")

        # self.myprint("end setting points: waiting 10 secs")
        # self.set_delay_if_not_simulation(10000)
        self.myprint("end setting points")
        self.dedent()
    @print_name(print_details)
    def setDirection(self, fromBranch, toBranch):
        global throttle
        self.indent()
        self.myprint1 ("in setDirection ")
        if toBranch != self.spur_branch:
            # set loco to forward
            self.myprint("Set Loco Forward")
            if sensors.getSensor("runRealTrainDistributionInglenookSensor").getKnownState() == ACTIVE:
                throttle.setIsForward(True)
            direction = "to_siding"
        else:
            # set loco to reverse
            self.myprint("Set Loco backward")
            if sensors.getSensor("runRealTrainDistributionInglenookSensor").getKnownState() == ACTIVE:
                throttle.setIsForward(False)
            direction = "to_spur"
        self.myprint1 ("end setDirection ", direction)
        self.dedent()
        return direction
    @print_name()
    def changeDirection(self):
        #global throttle
        self.indent()
        self.myprint ("in changeDirection ")
        #global throttle
        if throttle.getIsForward():
            if sensors.getSensor("runRealTrainDistributionInglenookSensor").getKnownState() == ACTIVE:
                throttle.setIsForward(False)
            self.myprint("Changed direction, reverse")
            direction = "forwards"
        else:
            if sensors.getSensor("runRealTrainDistributionInglenookSensor").getKnownState() == ACTIVE:
                throttle.setIsForward(True)
            self.myprint("Changed direction, forward")
            direction = "reverse"
        self.dedent()
        return direction

    @print_name()
    def waitChangeSensorActive(self, sensor):
        # self.indent()
        self.myprint("in waitChangeSensorActive" + " sensor " + self.sensorName(sensor))
        self.sensors_to_watch = [self.stop_thread_sensor, sensor]

        self.waitSensorActive(self.sensors_to_watch)
        sensor_changed = [sensor for sensor in self.button_sensors_to_watch if sensor.getKnownState() == ACTIVE][0]
        if sensor_changed == self.stop_thread_sensor:
            self.stop_thread = True
            # break
    @print_name()
    def waitChangeSensorInactive(self, sensor):
        # self.indent()
        self.myprint("in waitChangeSensorInactive" + " sensor " + self.sensorName(sensor))
        self.sensors_to_watch = [self.stop_thread_sensor, sensor]
        #waitChangeSensor(sensor,self.sensorOff)
        # while 1:
            #self.waitChange(self.sensors_to_watch)
        self.waitSensorInactive(self.sensors_to_watch)
        sensor_changed = [sensor for sensor in self.button_sensors_to_watch if sensor.getKnownState() == INACTIVE][0]
        if sensor_changed == self.stop_thread_sensor:
            self.stop_thread = True
        # break
            # got_state = sensor.getKnownState()
            # if got_state == INACTIVE:
            #     self.myprint("got_state inactive")
            #     # self.dedent()
            #     break

    def wait_sensor(self, sensorName, sensorState):
        sensor = sensors.getSensor(sensorName)
        if sensor is None:
            self.displayMessage('Sensor {} not found'.format(sensorName))
            return
        if sensorState == 'active':
            #if self.logLevel > 1: print ("wait_sensor active: sensorName {} sensorState {}",format(sensorName, sensorState))
            self.waitSensorActive(sensor)
        elif sensorState == 'inactive':
            self.waitSensorInactive(sensor)
        else:
            self.displayMessage('Sensor state, {}, is not valid'.format(sensorState))

    def mysound(self):
        self.myprint("bell")
        if sensors.getSensor("bellInglenookSensor").getKnownState() == ACTIVE:
            snd = jmri.jmrit.Sound("resources/sounds/Bell.wav")
            snd.play()
        self.myprint("bell end")

    # @print_name()
    def update_displays(self, pegs):
        #print "self.positions",  self.positions
        # position = next(self.positions)
        # print("!!!!!!!!!!!!!!!!! position", self.position)
        InglenookMaster().display_trucks_on_insert(self.pegs, self.screen)
        InglenookMaster().display_trucks_on_panel(self.pegs)

    def set_delay_if_not_simulation(self, msec):
        if sensors.getSensor("runRealTrainDistributionInglenookSensor").getKnownState() == ACTIVE:
            # self.waitMsec(msec)
            pass

    def getBranchNo(self, truckNo):
        for branchno in range(1,5):
            if self.truckInSiding(truckNo, branchno):
                return branchno
        return 99

    def get_branch_from_sensor(self, sensor):
        # sensor_name = sensor.getUserName().split("_")[-1]
        sensor_name = sensor.getComment().split("_")[1]    #either siding1 2 or 3 or headshunt
        self.myprint3("sensor_name", sensor_name)
        if sensor_name == "siding1" or  sensor_name == "siding2" or sensor_name == "siding3":
            return int(sensor_name[-1])   #last char of string
        elif sensor_name == "headshunt":
            return 4
        else:
            return 100
    def truckInSiding(self, truckNo, branchNo):
        return self.pegs[branchNo - 1].count(truckNo)>0

    # @print_name()
    # def countTrucksActive_wait1(self, sensor, direction, count):
    #     # going towards sidings, the number of trucks to pick up is 0
    #     global gbl_simulate_sensor_wait_time
    #     self.indent()
    #     simulate = sensors.getSensor("simulateInglenookSensor")
    #     if simulate.getKnownState() == ACTIVE:
    #         midPeg = self.setMidBranch(sensor)-1
    #         self.dialogs.displayMessage("countTrucksActive_wait1: engine: "+ str(count))
    #         #ensure the mimic panel updates
    #         self.myprint1("pegs", self.pegs)
    #         self.myprint1( "sensor.getUserName()", sensor.getUserName())
    #         if self.setBranch(sensor)==self.spur_branch:
    #             if direction == "forwards":
    #                 # we pop from spur  and push to mid to the left
    #                 self.myprint1("1 forwards we pop from spur and push to mid")
    #                 self.dialogs.displayMessage("1 we pop from spur and push to mid")
    #                 #self.myprint1("we pop from spur to the laft and push to deque 4")
    #                 self.pegs[midPeg].appendleft(self.pegs[self.spurPeg].pop())
    #             else:
    #                 # we pop from mid and push to spur
    #                 self.myprint1("2 we pop from mid and push to spur")
    #                 self.dialogs.displayMessage("2 we pop from mid and push to spur")
    #                 self.myprint1("we pop from smid to the laft and push to spur")
    #                 self.pegs[self.spurPeg].append(self.pegs[midPeg].popleft())
    #
    #         else:    #siding sensor
    #             sidingPeg = self.setBranch(sensor)-1       # the pegs start from 0
    #             midPeg = self.setMidBranch(sensor)-1
    #             # self.myprint1("# we pop from mid_branch and push to siding")
    #             if direction == "forwards":
    #                 self.myprint1("3 we pop from mid and push to siding (maybe we should not do this)")
    #                 self.dialogs.displayMessage("3 we pop from mid and push to siding (maybe we should not do this)")
    #                 # self.pegs[sidingPeg].append(self.pegs[self.midPeg].pop())    #comment out for now
    #                 # we just move the first truck to the coupling position
    #             else:
    #                 # we pop from mid and push to siding
    #                 self.myprint1("4 we pop from siding and push to mid")
    #                 self.dialogs.displayMessage("4 we pop from siding and push to mid")
    #                 self.myprint1("we pop from mid to the laft and push to spur")
    #                 self.pegs[midPeg].append(self.pegs[sidingPeg].pop())
    #
    #         self.update_displays(self.pegs)
    #         self.waitMsec(gbl_simulate_sensor_wait_time)    # make sure can see the update
    #     else:
    #         if self.setBranch(sensor)!=self.spur_branch:   # We don't count at the spur branch (though we could)
    #             self.myprint("actually waiting for sensor")
    #             self.waitChangeSensorActive(sensor)
    #     self.myprint("waited1")
    #     self.dedent()
    #
    #     # @alternativeaction("alt_action_countTrucksActive2","sensor_stored")
    #     # @variableTimeout("timeout_stored")
    # @print_name()
    # def countTrucksActive_wait2(self, sensor, direction, count):
    #     # going towards sidings
    #     global gbl_simulate_sensor_wait_time
    #     self.indent()
    #     simulate = sensors.getSensor("simulateInglenookSensor")
    #     if simulate.getKnownState() == ACTIVE:
    #         self.dialogs.displayMessage("countTrucksActive_wait2: truck count active: "+ str(count))
    #         #ensure the mimic panel updates
    #         self.myprint1("pegs", self.pegs)
    #         spur = 3
    #         mid = 4
    #         self.myprint1( "sensor.getUserName()", sensor.getUserName())
    #         if self.setBranch(sensor)==self.spur_branch:
    #             # we pop from stack 3 to the laft and push to deque 4
    #             self.myprint1("# we pop from mid to the laft and push to spur")
    #             self.dialogs.displayMessage("# we pop from mid to the laft and push to spur")
    #             self.pegs[spur].append(self.pegs[mid].popleft())
    #         else:
    #             self.dialogs.displayMessage("counting truck: active towards siding: sensor " + str(sensor.getUserName()))
    #             # we pop from deque 1 2 or 3 and push to mid deque
    #             self.myprint1("# we pop from deque 1 2 or 3 and push to spur")
    #             self.dialogs.displayMessage("# we pop from siding and push to mid")
    #             branch = self.setBranch(sensor)-1       # the pegs start from 0
    #             self.myprint1("sensor", sensor.getUserName(), "branch", branch)
    #             self.pegs[mid].append(self.pegs[branch].pop())
    #             self.myprint1("pegs after", self.pegs)
    #         self.update_displays(self.pegs)
    #         self.waitMsec(gbl_simulate_sensor_wait_time)    # make sure can see the update
    #     else:
    #         self.waitChangeSensorActive(sensor)
    #     self.myprint("waited2")
    #     self.dedent()

    @print_name()
    def simulate1(self):
        if (sensors.getSensor("simulateInglenookSensor").getKnownState() == ACTIVE or \
            sensors.getSensor("simulateErrorsInglenookSensor").getKnownState() == ACTIVE or \
            sensors.getSensor("simulateDistributionInglenookSensor").getKnownState() == ACTIVE)     :
            return True
        else:
            return False

    @print_name()
    def really_doit_countTrucksInactive(self, sensor):
        do_it = (sensors.getSensor("runRealTrainDistributionInglenookSensor").getKnownState() == ACTIVE)
        if do_it:
            self.waitChangeSensorInactive(sensor)
            self.waitMsec(1000)


    @print_name()
    def really_doit_countTrucksActive(self, sensor):
        do_it = (sensors.getSensor("runRealTrainDistributionInglenookSensor").getKnownState() == ACTIVE)
        if do_it:
            self.waitChangeSensorActive(sensor)
            self.waitMsec(1000)

    @print_name()
    def simulate_countTrucksInactive(self, sidingBranch, sensor, direction, count, pegs):  #pegs just passed so they get printed out
        self.indent()
        simulate = self.simulate1()
        if simulate:
            #ensure the mimic panel updates
            self.myprint("pegs", self.pegs)
            spur = 3
            self.myprint1( "sensor.getUserName()", sensor.getUserName())
            my_branch = self.get_branch_from_sensor(sensor)
            self.dialogs.displayMessage("self.get_branch_from_sensor(sensor) " + str(my_branch) + " self.spur_branch " + str(self.spur_branch))
            if self.get_branch_from_sensor(sensor) == self.spur_branch:
                if direction == "to_spur":
                    # we pop from spur and push to  mid
                    midPeg = self.setMidBranch(sidingBranch) - 1
                    self.dialogs.displayMessage("pop from spur and push to  mid ")
                    self.myprint2("we pop from mid and push to spur")
                    self.myprint1("self.pegs before",self.pegs)
                    if pegs[self.spurPeg] == 0:
                        #error
                        self.myprint2("error: self.pegs before",self.pegs)
                        exit()
                    else:
                        self.pegs[spur].append(self.pegs[midPeg].popleft())
                else:
                    # we pop from mid from the left and push to  spur
                    # move_engine = True
                    midPeg = self.setMidBranch(sidingBranch) - 1
                    self.dialogs.displayMessage("pop from mid from the left and push to  spur ")
                    self.myprint2("we pop from spur and push to mid")
                    self.myprint1("self.pegs before",self.pegs)
                    self.pegs[midPeg].appendleft(self.pegs[spur].pop())
                self.myprint2("self.pegs after",self.pegs)
            else:
                if direction == "to_spur":
                    #we pop from branch and push to mid
                    # move_engine = False
                    midPeg = self.setMidBranch(sidingBranch) - 1
                    # print "midPeg" , midPeg
                    branchPeg = self.setBranch(sensor)-1       # the pegs start from 0
                    self.myprint1("pegs before", self.pegs)
                    self.dialogs.displayMessage("we pop from branch and push to mid")
                    self.myprint2("we pop from branch and push to mid")
                    self.pegs[midPeg].append(self.pegs[branchPeg].pop())
                    self.myprint1("pegs after", self.pegs)
                else:
                    # we pop from mid and push to stack 1 2 or 3
                    # move_engine = False
                    branchPeg = self.setBranch(sensor)-1       # the pegs start from 0
                    midPeg = self.setMidBranch(sidingBranch) - 1
                    self.dialogs.displayMessage("we pop from mid deque and push to branch")
                    self.myprint2("# we pop from mid and push to branch")
                    self.myprint1("self.pegs",self.pegs)
                    self.pegs[branchPeg].append(self.pegs[midPeg].pop())
                    self.myprint1("pegs after", self.pegs)
            self.update_displays(self.pegs)
            # self.waitMsec(gbl_simulate_sensor_wait_time)    # make sure can see the update
            if self.stop_thread_sensor.getKnownState() == ACTIVE:
                self.stop_thread == True
        self.dedent()

    @print_name()
    def simulate_countTrucksActive(self, sidingBranch, sensor, direction, count, pegs):  #pegs just passed so they get printed out
        self.indent()
        # self.myprint2("simulate_countTrucksActive a")
        simulate = self.simulate1()
        # self.myprint2("simulate_countTrucksActive a")
        if simulate:
            self.myprint2("simulate_countTrucksActive a")
            #ensure the mimic panel updates
            self.myprint("pegs", self.pegs)
            spur = 3
            self.myprint2( "sensor.getUserName()", sensor.getUserName())
            my_branch = self.get_branch_from_sensor(sensor)
            self.dialogs.displayMessage("self.get_branch_from_sensor(sensor) " + str(my_branch) + " self.spur_branch " + str(self.spur_branch))
            if self.get_branch_from_sensor(sensor) == self.spur_branch:
                if direction == "to_spur":
                    # we pop from spur and push to  mid
                    midPeg = self.setMidBranch(sidingBranch) - 1
                    self.dialogs.displayMessage("pop from spur and push to  mid ")
                    self.myprint2("we pop from mid and push to spur")
                    self.myprint1("self.pegs before",self.pegs)
                    if pegs[self.spurPeg] == 0:
                        #error
                        self.myprint2("error: self.pegs before",self.pegs)
                        exit()
                    else:
                        self.pegs[spur].append(self.pegs[midPeg].popleft())
                else:
                    # we pop from mid from the left and push to  spur
                    # move_engine = True
                    midPeg = self.setMidBranch(sidingBranch) - 1
                    self.dialogs.displayMessage("pop from mid from the left and push to  spur ")
                    self.myprint2("we pop from spur and push to mid")
                    self.myprint1("self.pegs before",self.pegs)
                    self.pegs[midPeg].appendleft(self.pegs[spur].pop())
                self.myprint2("self.pegs after",self.pegs)
            else:
                if direction == "to_spur":
                    #we pop from branch and push to mid
                    # move_engine = False
                    midPeg = self.setMidBranch(sidingBranch) - 1
                    # print "midPeg" , midPeg
                    branchPeg = self.setBranch(sensor)-1       # the pegs start from 0
                    self.myprint1("pegs before", self.pegs)
                    self.dialogs.displayMessage("we pop from branch and push to mid")
                    self.myprint2("we pop from branch and push to mid")
                    self.pegs[midPeg].append(self.pegs[branchPeg].pop())
                    self.myprint1("pegs after", self.pegs)
                else:
                    # we pop from mid and push to stack 1 2 or 3
                    # move_engine = False
                    branchPeg = self.setBranch(sensor)-1       # the pegs start from 0
                    midPeg = self.setMidBranch(sidingBranch) - 1
                    self.dialogs.displayMessage("we pop from mid deque and push to branch")
                    self.myprint2("# we pop from mid and push to branch")
                    self.myprint1("self.pegs",self.pegs)
                    self.pegs[branchPeg].append(self.pegs[midPeg].pop())
                    self.myprint1("pegs after", self.pegs)
            self.update_displays(self.pegs)
            # self.waitMsec(gbl_simulate_sensor_wait_time)    # make sure can see the update
        self.dedent()

        # # @print_name()
        # def is_there_a_truck(self):
        #     pass
        #
        # # @print_name()
        # def count_at_spur(self):
        #     direction = self.setDirection(sidingBranch, self.spur_branch)
        #     sensor = self.setSensor(self.spur_branch)
        #     self.countTrucksInactive(self.noTrucksOnTrain, sensor, direction, sidingBranch)  #counting all trucks on train
        #     self.setSpeed(self.stop)


    # 1) check for truck  (is_there_a_truck)
    #     stop_flag = False  # only checked when stop_sensor True
    #     stop_sensor = false
    #     if check for truck count = 1
    #         stop_thread_sensor True
    #         self.recover_flag = True
    #     if check_for_truck timed out
    #         self.recover_flag = False
    @print_name(True)                                                               # run first,  checks after function last
    @alternativeaction("alt_function_truck_at_siding_error_if_true", "sidingBranch", "noTrucksToMove")      # this is run 2nd, but stop flag is checked after timeout
    @variableTimeout("time_to_countInactive_one_truck")  # uses self.time_to_count_one_truck
    # @timeout(2000)
    def is_there_a_truck_at_siding_error_if_true(self, sidingBranch, noTrucksToMove, thread_name ):

        # Checks whether a truck is detected at the siding sensor when the trucks are disconnected and the train moves out of the siding
        # The trucks that are disconnected should be left in the siding. If the disconnection does not take place
        # the trucks will be pulled past the sensor, and an error will occur
        # if not there will be no error and the routine will time out

        # sets rectify flag if counts a truck. The trucks should have been disconnected
        # the routine should time out if there is a success

        # for simulating the time taken by the routine should be more than time_to_countInactive_one_truck for a success
        #                an alternative action should be called and the reset flag set there
        # for simulating the time taken by the routine should be less than the time_to_countInactive_one_truck for an error
        #                no alternative action should be called and the reset flag set there


        self.indent()
        from java.util import Date

        threading_local.thread_name = thread_name

        self.myprint4("thread_name", thread_name, "threading_local.thread_name", threading_local.thread_name)

        start = Date().getTime()
        # print ("setting direction")

        direction = self.setDirection(sidingBranch, self.spur_branch)
        self.myprint3 ("setting sensor", "time taken", Date().getTime() - start)
        sensor = self.setSensor(sidingBranch)

        self.myprint3("set sensor",  "time taken", Date().getTime() - start)

        noTrucksToCount = 1
        # if we are simulating an error, there will be one truck counted here i.e. simulate == True
        # and the routine will not time out
        self.myprint3("checking sensors is_there_a_truck_at_siding_error_if_true")
        if sensors.getSensor("simulateErrorsInglenookSensor").getState() == ACTIVE or \
            sensors.getSensor("simulateDistributionInglenookSensor").getState() == ACTIVE:
            # print ("*****************************simulating with errors")
            # a_long_time = 10000  # enough to make it time out
            # self.myprint3("waiting a short time", a_long_time, "time will be", Date().getTime() - start + a_short_time)
            # self.waitMsec(a_long_time)
            if self.index < 2:
                self.myprint3 ("simulating with errors")
                simulateOneTruck = True
                direction = self.setDirection(sidingBranch, self.spur_branch)
                self.display_pegs(self.pegs)
                self.countTrucksInactive(noTrucksToCount, sensor, direction, sidingBranch, simulateOneTruck)  #counting
                self.myprint3("********************* one truck went from siding to spur")
                self.myprint3("time taken a", Date().getTime() - start)
                a_long_time = 10000  # enough to make it time out
                self.myprint3("waiting a LONG time", a_long_time, "time will be", Date().getTime() - start + a_long_time)
                self.waitMsec(a_long_time)
            else:
                # print ("simulating with errors but success this time")
                simulateOneTruck = False
                # the routine must not time out.
                a_short_time = 100  # small enough to make it not time out
                self.waitMsec(int(self.time_to_countInactive_one_truck))
                # print ("time taken", Date().getTime() - start)
                # print ("should have timed out")
            #     # self.waitMsec(a_short_time)
            #     # print ("time taken", Date().getTime() - start)
            #     print ("should have timed out")
        elif sensors.getSensor("simulateInglenookSensor").getState() == ACTIVE:
            self.myprint3 ("++++++++++++++++++++++++++++++++++ simulating without errors, the alt function should be called")
            self.myprint3 ("should time out", "time_to_countInactive_one_truck", self.time_to_countInactive_one_truck)
            self.myprint3("time taken", Date().getTime() - start)
            simulateOneTruck = False
            # the routine needs to not time out
            a_long_time = str(int(self.time_to_countInactive_one_truck) * 10) # small enough to make it not time out  (much less than time_to_countInactive_one_truck)
            self.myprint3("waiting a long time", a_long_time, "time will be", Date().getTime() - start + int(a_long_time))
            self.waitMsec(a_long_time)
            # self.myprint3 ("time taken", Date().getTime() - start)
            # self.myprint3 ("should have timed out", "time_to_countInactive_one_truck", self.time_to_countInactive_one_truck)
            # self.waitMsec(a_short_time)
            # self.myprint3 ("time taken", Date().getTime() - start)
            # self.myprint3 ("should have timed out")
            # the alt_function will be called
        elif sensors.getSensor("runRealTrainDistributionInglenookSensor").getState() == ACTIVE:
            self.myprint3 ("running real train")
            simulateOneTruck = True
            direction = self.setDirection(sidingBranch, self.spur_branch)
            self.display_pegs(self.pegs)
            self.countTrucksInactive(noTrucksToCount, sensor, direction, sidingBranch, simulateOneTruck)  #counting#

        # truck counted
        self.rectify_flag_t1 = True
        self.myprint3("********************** set rectify_flag", self.rectify_flag_t1)
        self.stop_thread_sensor.setKnownState(ACTIVE)
        self.myprint3("set sensor",  "time taken", Date().getTime() - start)
        self.myprint3("is_there_a_truck_at_siding_error_if_true end")
        self.dedent()

    @print_name(True)                                                               # run first,  checks after function last
    @alternativeaction("count_at_siding__is_there_a_truck_error_if_none_alt_function", "sidingBranch", "noTrucksToCount", "simulate")      # this is run 2nd, but stop flag is checked after timeout
    @variableTimeout("time_to_countInactive_one_truck")  # uses self.time_to_count_one_truck
    # @timeout(2000)
    def count_at_siding__is_there_a_truck_error_if_none(self, sidingBranch, noTrucksToMove, time_to_countInactive_one_truck, simulate, called_from_for_diagnostics):

        from java.util import Date
        global place_trucks_near_disconnect_siding

        start = Date().getTime()
        self.myprint3 ("setting direction")

        direction = self.setDirection(sidingBranch, self.spur_branch)
        self.myprint3 ("setting sensor", "time taken", Date().getTime() - start)
        sensor = self.setSensor(sidingBranch)

        self.myprint3("set sensor",  "time taken", Date().getTime() - start)

        noTrucksToCount = noTrucksToMove
        #if we are simulating an error, there will be no truck counted here i.e. simulate == True
        # and the routine will not time out
        self.myprint3("checking sensors is_there_a_truck1")
        # self.dialogs.displayMessage1("in count_at_siding__is_there_a_truck_error_if_none"  + " self.index2 " +str(self.index2))
        if sensors.getSensor("simulateInglenookSensor").getState() == ACTIVE:
            self.myprint3 ("simulating simulateInglenookSensor")
            direction = self.setPointsAndDirection(sidingBranch, self.spur_branch)
            sensor = self.setSensor(sidingBranch)
            self.countTrucksActive(noTrucksToCount, sensor, direction, sidingBranch)  # counts from 0
            self.set_delay_if_not_simulation(2000)
            self.myprint3 ("time taken a", Date().getTime() - start)
        elif sensors.getSensor("simulateErrorsInglenookSensor").getState() == ACTIVE or \
                sensors.getSensor("simulateDistributionInglenookSensor").getState() == ACTIVE:
            if self.index2 < 2:
                midPeg = self.setMidBranch(sidingBranch) - 1
                self.dialogs.displayMessage1("added 9")
                self.myprint3 ("simulating with errors")
                simulateOneTruck = True
                # the routine needs to time out
                a_short_time = 3000  # enough to make it time out
                self.waitMsec(int(self.time_to_countInactive_one_truck))
                self.myprint3 ("time taken", Date().getTime() - start)
                self.myprint3 ("should have timed out")
                self.waitMsec(a_short_time)
                self.myprint3 ("time taken", Date().getTime() - start)
                self.myprint3 ("should have timed out")
                # now have to do recovery
            else:
                self.myprint3 ("simulating with errors but success this time")
                direction = self.setPointsAndDirection(sidingBranch, self.spur_branch)
                sensor = self.setSensor(sidingBranch)
                self.countTrucksActive(noTrucksToCount, sensor, direction, sidingBranch)  # counts from 0
                # self.set_delay_if_not_simulation(2000)
                self.myprint3 ("time taken aaaa", Date().getTime() - start)
        elif sensors.getSensor("runRealTrainDistributionInglenookSensor").getState() == ACTIVE:
            self.myprint3 ("simulating with errors but success this time")
            direction = self.setPointsAndDirection(sidingBranch, self.spur_branch)
            sensor = self.setSensor(sidingBranch)
            self.countTrucksActive(noTrucksToCount, sensor, direction, sidingBranch)  # counts from 0
            self.set_delay_if_not_simulation(2000)
            self.myprint3 ("time taken a", Date().getTime() - start)
        # truck counted
        self.rectify_flag2 = False
        self.myprint3("********************** set rectify_flag2 False", self.rectify_flag2)
        self.stop_thread_sensor.setKnownState(ACTIVE)
        self.myprint3("set sensor",  "time taken", Date().getTime() - start)
        self.myprint3("count_at_siding__is_there_a_truck_error_if_none end")

    @print_name()
    def count_at_spur(self, sidingBranch, noTrucksToMove, thread_name):

        threading_local.thread_name = thread_name
        # print "threading_local.thread_name", threading_local.thread_name
        # if stop_thread_sensor is set to inactive when counting, the routine stops   # check out countTrucksInactive to see how this works
        direction = self.setDirection(sidingBranch, self.spur_branch)
        sensor = self.setSensor(self.spur_branch)
        self.countTrucksInactive(self.noTrucksOnTrain, sensor, direction, sidingBranch)  #counting all trucks on train
        self.setSpeed(self.stop)

    @print_name()
    def count_at_siding(self, noTrucksToCount, sensor, direction, sidingBranch):
        operation = "PICKUP"
        direction = self.setPointsAndDirection(sidingBranch, self.spur_branch)
        sensor = self.setSensor(sidingBranch)
        self.countTrucksActive(noTrucksToCount, sensor, direction, sidingBranch)  # counts from 0     $$$$$$$$$$$$$changed$$$$$$$$$$$$$$
        self.set_delay_if_not_simulation(2000)

    def set_time_to_countInactive_one_truck(self):
        if sensors.getSensor("simulateErrorsInglenookSensor").getState() == ACTIVE or \
           sensors.getSensor("simulateDistributionInglenookSensor").getState() == ACTIVE:
            time_to_countInactive_one_truck = "8000"   # msec
        elif sensors.getSensor("simulateInglenookSensor").getState() == ACTIVE:
            # time_to_countInactive_one_truck = "100"
            time_to_countInactive_one_truck = "4000"
        elif sensors.getSensor("runRealTrainDistributionInglenookSensor").getState() == ACTIVE:
            time_to_countInactive_one_truck = "5000"
        else:
            time_to_countInactive_one_truck = "5000"
        return time_to_countInactive_one_truck
    @print_name()
    def display_pegs(self, pegs):    #this is just to display the pegs using @print_name
        pass

    @print_name(True)
    def rectify_trucks_back_to_mid(self, sidingBranch):
        global repeat

        threading_local.thread_name = "rectify_mid"     #make sure we now offset the printing correctly

        self.myprint2("hi")
        self.myprint2("in rectify_trucks_back_to_mid: a")
        direction = self.setDirection(self.spur_branch, sidingBranch)
        sensor = self.setSensor(self.spur_branch)
        noTrucksToCount = self.no_trucks_to_rectify
        self.myprint2("self.no_trucks_to_rectify", self.no_trucks_to_rectify)
        self.display_pegs(self.pegs)
        self.countTrucksInactive(noTrucksToCount, sensor, direction, sidingBranch)  #counting
        self.display_pegs(self.pegs)
        self.myprint2("in rectify_trucks_back_to_mid: ******************** one truck goes from mid to siding")
        self.couple1(sidingBranch)
        self.myprint2("in rectify_trucks_back_to_mid: end")

    @print_name(True)
    def rectify_trucks_back_to_siding(self, sidingBranch):

        threading_local.thread_name = "rectify_sid"     #make sure we now offset the printing corecty

        self.myprint2("in rectify_trucks_back_to_siding: a")
        direction = self.setDirection(self.spur_branch, sidingBranch)
        sensor = self.setSensor(sidingBranch)
        noTrucksToCount = 1
        self.myprint2("in rectify_trucks_back_to_siding: b")
        self.display_pegs(self.pegs)
        self.countTrucksInactive(noTrucksToCount, sensor, direction, sidingBranch)  #counting
        self.display_pegs(self.pegs)
        self.myprint2("in rectify matters: ******************** one truck goes from mid to siding")
        self.couple1(sidingBranch)
        self.myprint2("in rectify_trucks_back_to_siding: end")

    def rectify_connect_up_again(self, sidingBranch):
        self.myprint2("in rectify_connect_up_again")
        # we need to reverse direction and connect up again
        direction = self.setDirection(self.spur_branch, sidingBranch)
        sensor = self.setSensor(sidingBranch)
        # might need to move a bit ectra here
        timeCouple = 450   #need to increase this every time repeat
        self.couple1(sidingBranch)
        # remove the spacer truck (9) so the engine is coupled
        midPeg = self.setMidBranch(sidingBranch) - 1
        self.pegs[midPeg].pop()
        self.update_displays(self.pegs)


    @print_name(True)
    def alt_function_truck_at_siding_error_if_true(self, sidingBranch, noTrucksToMove):

        # There has been no truck detected in the time allocated time_to_countInactive_one_truck, so everything OK
        # We do not have to rectify anything , hence the rectify flag is set to false

        self.myprint3 ("in alternative action setting stop thread sensor")
        print ("in alternative action setting stop thread sensor")
        self.dialogs.displayMessage1("in alt_function")
        # (a0) kill other count_at_spur thread
        self.myprint3 ("in alternative action setting stop thread sensor INACTIVE")
        self.stop_thread_sensor.setKnownState(INACTIVE)    # check out countTrucksInactive to see how this works
        self.rectify_flag_t1 = False
        print "self.rectify_flag_t1", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", self.rectify_flag_t1

    @print_name(True)
    def count_at_siding__is_there_a_truck_error_if_none_alt_function(self, sidingBranch, noTrucksToMove, simulate):
        self.myprint2 ("in alternative action setting stop thread sensor")
        self.dialogs.displayMessage1("in alt_function2")
        if simulate:
            # make the engine go away from the siding sensor without the rest of the trucks
            midPeg = self.setMidBranch(sidingBranch) - 1
            self.pegs[midPeg].append(9)
            self.update_displays(self.pegs)
        # (a0) kill other count_at_spur thread
        # self.stop_thread_sensor.setKnownState(INACTIVE)    # check out countTrucksInactive to see how this works

    def set_turnout_short(self, direction):

        direction_to_1  = "Closed"

        if direction == "to_branch_1":
            if direction_to_1 == "Closed":
                self.turnout_short.setState(CLOSED)
            else:
                self.turnout_short.setState(THROWN)
        elif direction == "to_branch_2":
            if direction_to_1 == "Closed":
                self.turnout_short.setState(THROWN)
            else:
                self.turnout_short.setState(CLOSED)

    def set_turnout_long(self, direction):

        direction_to_long  = "Closed"

        if direction == "to_branch_long":
            if direction_to_long == "Closed":
                self.turnout_long.setState(CLOSED)
            else:
                self.turnout_long.setState(THROWN)
        elif direction == "to_branches_short":
            if direction_to_long == "Closed":
                self.turnout_long.setState(THROWN)
            else:
                self.turnout_long.setState(CLOSED)

    def set_throttle_direction(self, direction):

        global throttle

        engine_facing_sidings = True

        if direction == "to_sidings":
            if engine_facing_sidings:
                throttle.setIsForward(True)
            else:
                throttle.setIsForward(False)


    @print_name(print_details)
    def setPointsAndDirection(self, fromBranch, toBranch):
        # one of fromBranch or toBranch must be spur_branch
        self.indent()
        if self.spur_branch not in [fromBranch, toBranch]:
            self.myprint1("spur_branch ", self.spur_branch , " must be one of ", fromBranch, toBranch)
            cresh_here  # crash_here does not exist so crash
        self.myprint (">>in setPointsAndDirection ")
        self.setPoints(fromBranch,toBranch)
        direction = self.setDirection(fromBranch, toBranch)
        self.myprint ("end setPointsAndDirection ")
        self.dedent()
        return direction

    @print_name()
    def setBranch(self, sensor):
        self.indent()
        self.myprint ("in setBranch ")
        self.myprint("setting branch")
        branch = 99
        if sensor == self.sensor1:
            branch = 1
        if sensor == self.sensor2:
            branch = 2
        if sensor == self.sensor3:
            branch = 3
        if sensor == self.sensor4:
            branch = 4
        self.myprint("end setting branch")
        self.dedent()
        return branch

    @print_name()
    def setMidBranch(self, sidingBranch):
        self.indent()
        if type(sidingBranch) != int:
            crashhere
        self.myprint ("in setBranch ")
        self.myprint("setting branch")
        midBranch = sidingBranch + 4
        self.dedent()
        # print ("setMidBranch: branch", sidingBranch, "modBranch", midBranch)
        return midBranch

    @print_name(print_details)
    def setSensor(self, branch):
        self.indent()
        self.myprint ("in setSensor ")
        self.myprint("setting sensor")
        if branch == 1:
            sensor = self.sensor1
        if branch == 2:
            sensor = self.sensor2
        if branch == 3:
            sensor = self.sensor3
        if branch == 4:
            sensor = self.sensor4
        # self.myprint2("end setting sensor", "branch", branch, "sensor", sensor)
        self.dialogs.displayMessage("end setting sensor: branch " + str(branch) + " sensor " + str(sensor))
        self.dedent()
        return sensor

    @print_name()
    def couple1(self, sidingBranch, timeCouple = 350):   #we use self.couple for a speed, so use couple1

        self.indent()
        self.myprint("in couple")

        self.setDirection(self.spur_branch, sidingBranch)
        # timeCouple = 350
        self.mysound()
        self.setSpeedSetDelay(self.couple, timeCouple)
        self.mysound()
        self.setSpeedSetDelay(self.stop,1000)
        self.mysound()
        #self.setPointsAndDirection(toBranch, fromBranch)
        #timeReturn = 10
        #self.setSpeedSetDelay(self.slow, timeReturn)
        #self.setSpeedSetDelay(self.stop,1000)
        self.myprint("finished couple part 2 waiting 2 secs")
        #self.myprint("finished couple part 3")

        self.myprint("finished couple")
        self.dedent()
    @print_name()
    def uncouple1(self, sidingBranch, operation):     #we use self.uncouple as a speed, so use uncouple1
        self.indent()
        sensor = self.setSensor(sidingBranch)
        self.setSpeed(self.stop)
        if operation == "PICKUP":
            self.myprint("in uncouple 1")
            self.myprint("in pickup")

            # #whiz forward
            # self.setPointsAndDirection(fromBranch, toBranch)
            # self.setSpeed(self.uncouple)
            # #self.set_delay_if_not_simulation(500)
            # #count twice 'cos in active
            # #waitChangeActive(sensor)    # sets speed 0
            # noTrucksToCount = 1  # starts from 0 ( we are in a truck so that is 0
            # self.countTrucksActive(noTrucksToCount, sensor)
            # self.setSpeed(stop)
            self.mysound()
            self.set_delay_if_not_simulation(1000)


            #whiz back
            self.myprint("in whizback")

            direction = self.setDirection(self.spur_branch, sidingBranch)
            self.setSpeedSetDelay(self.uncouple,50)
            #self.set_delay_if_not_simulation(1000)
            noTrucksToCount = 1
            self.myprint("countTrucksInactive1", sensor)
            simulate = False
            self.countTrucksActive(noTrucksToCount, sensor, direction, sidingBranch, simulate)       # change to active so only a little whiz
            #waitChangeInactive(sensor)  # sets speed 0
            self.myprint("countTrucksInctive returned")
            self.setSpeed(self.stop)
            self.set_delay_if_not_simulation(1000)

            #whiz forward again
            self.myprint("in forward again")
            direction = self.setDirection(sidingBranch, self.spur_branch)
            self.setSpeedSetDelay(self.fast, 100)
            #self.set_delay_if_not_simulation(100) # need to be times because has dropped off truck
            #waitChangeActive(sensor)    # sets speed 0
            # noTrucksToCount = 1
            # self.countTrucksInactive(noTrucksToCount, sensor, direction, sidingBranch, simulate)    # change to active
            # self.setSpeedSetDelay(self.stop,100)
            self.myprint("end whiz forward")
            self.myprint("in uncouple 1a")

        if operation == "DROPOFF":
            self.myprint("in uncouple 2")
            #whiz back
            self.mysound()
            self.set_delay_if_not_simulation(1000)


            #whiz back
            self.myprint("in whizback")

            # self.setPointsAndDirection(toBranch, fromBranch)
            # self.setSpeedSetDelay(self.uncouple,50)
            # #self.set_delay_if_not_simulation(1000)
            # noTrucksToCount = 1
            # self.countTrucksInactive(noTrucksToCount, sensor)
            # #waitChangeInactive(sensor)  # sets speed 0
            # self.myprint("countTrucksActive returned")
            # self.setSpeed(self.stop)
            # self.set_delay_if_not_simulation(1000)

            #whiz forward again
            self.myprint("in forward again")
            direction = self.setPointsAndDirection(sidingBranch, self.spur_branch)
            self.setSpeedSetDelay(self.fast, 100)
            #self.set_delay_if_not_simulation(100) # need to be times because has dropped off truck
            #waitChangeActive(sensor)    # sets speed 0
            # noTrucksToCount = 1
            # self.countTrucksActive(noTrucksToCount, sensor)
            self.setSpeedSetDelay(self.stop,100)
            self.myprint("end whiz forward")
            self.myprint("in drop off")
            direction = self.setPointsAndDirection(self.spur_branch, sidingBranch)
            self.setSpeedSetDelay(self.fast,100)
            #waitChangeInactive(sensor)  # sets speed 0
            self.setSpeed(self.stop)
            self.myprint("end in dropoff")
            self.myprint2("in uncouple 2a")
        self.dedent()
        self.dialogs.displayMessage("end uncouple1 branch ")
        self.myprint2("in uncouple3")
        logging = "noprint"

    #@print_name()
    def swapRouteSameDirectionTravelling(self, fromBranch, toBranch):
        self.indent()
        self.myprint ("in swapRouteSameDirectionTravelling ")
        self.setPointsAndDirection(fromBranch, toBranch)
        self.dedent()

    #@print_name()
    def swapRouteOppDirectionTravelling(self, fromBranch, toBranch):
        self.indent()
        self.myprint ("in swapRouteOppDirectionTravelling ")
        self.setPointsAndDirection(fromBranch, toBranch)
        self.dedent()


    #@print_name()
    def noTrucksOnBranches(self, pegs):
        noTrucksList = [len(x) for x in pegs]
        return noTrucksList

    #@print_name()
    def noTrucksOnBranch(self, pegs, branch):
        NoTrucks = len(pegs[branch - 1])
        return NoTrucks

    #@print_name()
    def moveDistance(self, distance):
        self.indent()
        self.myprint("moving " , distance)
        self.setSpeed(self.vslow)
        if distance == self.smallDistance:
            self.set_delay_if_not_simulation(1000)
        else:
            self.set_delay_if_not_simulation(1000)
        self.setSpeed(self.stop)
        self.set_delay_if_not_simulation(500)
        self.dedent()

    #@print_name()
    def sensorName(self, sensor) :
        self.indent()
        #self.myprint ("in sensorName ")
        if sensor == self.sensor1:
            self.dedent()
            return "Sensor1"
        elif sensor == self.sensor2:
            self.dedent()
            return "Sensor2"
        elif sensor == self.sensor3:
            self.dedent()
            return "Sensor3"
        elif sensor == self.sensor4:
            self.dedent()
            return "Sensor4"
        else:
            self.dedent()
            return "Invalid"

    # Define routine to map status numbers to text
    #@print_name()
    def stateName(self, state) :
        self.indent()
        self.myprint ("in stateName ")
        if (state == ACTIVE) :
            self.dedent()
            return "ACTIVE"
        if (state == INACTIVE) :
            self.dedent()
            return "INACTIVE"
        if (state == INCONSISTENT) :
            self.dedent()
            return "INCONSISTENT"
        if (state == UNKNOWN) :
            self.dedent()
            return "UNKNOWN"
        self.dedent()
        return "(invalid)"

    def move_to_initial_position(self):

        self.no_trucks = self.get_no_trucks()
        # assume trucks have been backed up to siding_long
        # note position
        positions_of_trucks = self.set_positions_of_trucks()

        msg = "positions of trucks set"
        yield ["display_message", msg]
        # print "**************************************a"
        # need to distribute them
        [no_trucks_short, no_trucks_long, no_trucks_total] = self.get_no_trucks()
        [turnout_short, turnout_long, turnout_main] = self.get_sidings()
        [turnout_short_direction, turnout_long_direction, turnout_main_direction] = self.get_turnout_directions()

        # print [no_trucks_short, no_trucks_long, no_trucks_total]
        # put no_trucks_long on siding_long

        no_trucks_to_move = no_trucks_long
        destBranch = 1      # siding_long
        fromBranch = 4      # sput

        msg = "moving from " + str(fromBranch) + " to " + str("destBranch")
        yield ["display_message", msg]
        # print "**************************************b"
        # for p in self.moveTrucksCreatingYieldStatements(no_trucks_to_move, fromBranch, destBranch): yield p

        # put rest of trucks on siding 2

        no_trucks_to_move = no_trucks_total - no_trucks_long
        destBranch = 2      # sput
        fromBranch = 1      # siding_long

        msg = "moving from " + str(fromBranch) + " to " + str("destBranch")
        yield ["display_message", msg]
        # print "**************************************c"

        for p in self.moveTrucksCreatingYieldStatements(no_trucks_to_move, fromBranch, destBranch): yield p
        # print "**************************************d"
        # put rest on siding_short

        no_trucks_to_move = 0
        destBranch = 4      # sput
        fromBranch = 2     # siding_long

        msg = "moving from " + str(fromBranch) + " to " + str("destBranch")
        yield ["display_message", msg]
        # print "**************************************e"
        for p in self.moveTrucksCreatingYieldStatements(no_trucks_to_move, fromBranch, destBranch): yield p
        # print "**************************************f"

    # @print_name()
    # def generate_first_instructions(self):
    #     self.indent()
    #     # the move trucks instruction is shown commented out, so we can see what the yield does
    #     # moveTrucks(self, noTrucksOnTrain, noTruckstoMove, fromBranch, destBranch):
    #
    #     # we move from branch 4 to branch 3 depositing all 5 trucks
    #     self.dedent()
    #     pass


    # Procedure
    #
    #     trucks on train yyzz (zz = x_old)
    #     depositing zz  (x_old)
    #     trucks on siding www
    #     picking up xx
    #         yyzz*www
    #     move to left zz then to right xx
    #     connect -zz + xx
    #     trucks on train = yyzz - zz + xx
    #
    # on siding   move x to dest
    #
    # 0) move 0
    #     b) move to siding
    #         move x = 0
    #         trucks on train y = 0
    #         x_old = 0
    #         y_old = 0
    #
    # 1) move x [init from dest]
    #     a) move to spur
    #         move 	x = 0
    #         connect -x_old + x
    #         trucks y = y_old - x_old + x
    #     b) move to 'from' siding     (start here)
    #         move 	x_old = x  (= 0 first)
    #         trucks 	y_old = y  (= 0 first)
    #
    # 2) move to dest:  x trucks
    #     a) move to spur
    #         connect - x_old + x
    #         move 	x
    #         trucks 	y = y_old - x_old + x
    #
    #     b) move to dest siding
    #         move 	x_old = x
    #         trucks	y_old = y


    # DROPOFF
    # we do two threads
    # stop_thread_sensor = False
    # 1) check for truck  (is_there_a_truck_
    #     stop_flag = False  # only checked when stop_sensor True
    #     stop_sensor = false
    #     if check for truck count = 1
    #         stop_thread_sensor True
    #         rectify_flag = True
    #     if check_for_truck timed out
    #         rectify_flag = False
    #
    # 2) move to spur  (count_at_spur)
    #     check for stop_thread_sensor True while checkingh sensors
    #     self.stop_thread_flag set true in simulate
    #     self.stop_thread_flag is set if waiting for sensor (this is just the stop_thread_sensor flag
    #
    #     updates self.number_of_trucks_to_move_back
    #     if stop_thread_flag set True:
    #         stops prematurely to recover
    #
    # wait for above two threads to complete
    #
    # start below two threads if self.recover_flag set
    #
    # 3) recover_truck_to_siding if previous two have finished
    #     moves back  1 truck  (simulation)
    #
    # 3) recover_trucks_to_mid if previous two have finished
    #     moves back  self.number_of_trucks_to_move_back to mid
    #
    #
    # 4) alt_function
    #     if check_for_truck times out
    #         sets stop_sensor True
    #         sets stop_flag False

    @print_name(True)
    def move_to_spur_operations(self, sidingBranch, noTrucksToMove, noTrucksToMove_old):
        amountToMove = noTrucksToMove - noTrucksToMove_old     #

        self.time_to_countInactive_one_truck = self.set_time_to_countInactive_one_truck()    # need different times for simulation and real life 100

        # move to correct position and uncouple
        operation = self.moveToDisconnectPosition(self.noTrucksOnTrain, amountToMove, sidingBranch)
        self.myprint2("operation", operation)
        self.noTrucksOnTrain = self.noTrucksOnTrain + amountToMove
        # operation is "PICKUP" or "DROPOFF"
        self.uncouple1(sidingBranch, operation)

        if operation == "DROPOFF" or \
                operation == "PICKUP":     #error does not uncouple
            # print "in operation", operation
            repeat = True
            self.index = 1
            while repeat:
                self.rectify_flag_t1 = True
                # print "in repeat 1 " , "iteration", self.index , "starts from 1"
                self.dialogs.displayMessage1("In operation " + str(operation) + " in move_to_spur repeat")
                self.sidingBranch = sidingBranch                    # needed for alternate_function decorator: see is_there_a_truck
                self.noTrucksToMove = noTrucksToMove                # needed for alternate_function decorator: see is_there_a_truck
                thread_name = "truck"
                # ensure that we have disconnected successfully (check that no trucks are being pulled past the siding sensor
                # print "rectify_flag before",self.rectify_flag_t1
                t1 = Thread(target=self.is_there_a_truck_at_siding_error_if_true, args=(sidingBranch, noTrucksToMove, thread_name))   # sets rectify_flag if counts a truck
                # and sets stop_thread_sensor
                thread_name = "count"
                # ensure that the disconnected trucks are pulled past the headshunt sensor
                t2 = Thread(target=self.count_at_spur, args=(sidingBranch, noTrucksToMove, thread_name))

                t1.start()      # stop_thread_sensor and self.rectify_flag set here if trucks do not uncouple and counts a truck
                self.waitMsec(200)  #just to get the printing OK
                t2.start()      # stops prematurely if stop_thread_sensor set
                t1.join()
                # print "rectify_flag_t1 after",self.rectify_flag_t1
                self.myprint2("**************** t1 joined", "self.rectify_flag_t1", self.rectify_flag_t1)
                t2.join()
                self.myprint2("**************** t2 joined", "self.rectify_flag_t1", self.rectify_flag_t1)
                if self.rectify_flag_t1 == True:
                    t3 = Thread(target=self.rectify_trucks_back_to_siding, args=(sidingBranch,))
                    # t4 = Thread(target=self.rectify_trucks_back_to_mid, args=(sidingBranch,))
                    t3.start()   # moves trucks back to siding
                    # t4.start()   # move trucks back to mid
                    t3.join()
                    self.myprint2("**************** t3 joined")
                    # t4.join()
                    self.myprint2("**************** t4 joined")
                    repeat = True
                else:
                    self.myprint2("**************** repeat false")
                    repeat = False
                self.index += 1
                self.myprint2("******************move_to_spur_operations: repeat", repeat)
        else:
            # print "in operation PICKUP"
            repeat = True
            self.index = 1
            while repeat:
                # print "in repeat 2 " , "iteration", self.index , "starts from 1"
                self.sidingBranch = sidingBranch                    # needed for alternate_function decorator: see is_there_a_truck
                self.noTrucksToMove = noTrucksToMove                # needed for alternate_function decorator: see is_there_a_truck_at_siding_error_if_true
                t1 = Thread(target=self.is_there_a_truck_at_siding_error_if_true, args=(sidingBranch, noTrucksToMove))   #sets rectify_flag if counts a truck
                # and sets stop_thread_sensor
                t2 = Thread(target=self.count_at_spur, args=(sidingBranch, noTrucksToMove))

                t1.start()      # stop_thread_sensor and self.rectify_flag set here if trucks do not uncouple and counts a truck
                t2.start()      # stops prematurely if stop_thread_sensor set
                t1.join()
                self.myprint2("**************** t1 joined")
                t2.join()

            self.count_at_spur(sidingBranch, noTrucksToMove)

    @print_name()
    def move_to_siding_operations(self, sidingBranch, noTrucksToMove):

        # the move operation will be done in the head operation
        # store variables which will be required
        # self.noTrucksToMoveFromPreviousStep = self.noTrucksToMove

        direction = self.setPointsAndDirection(self.spur_branch, sidingBranch)
        self.set_delay_if_not_simulation(5000)

        self.myprint3("setting sensor to spur branch")
        sensor = self.setSensor(self.spur_branch)
        self.myprint3("sensor", sensor)
        self.countTrucksInactive(self.noTrucksOnTrain, sensor, direction, sidingBranch)  # leave the moving to the next movement

        self.myprint3("setting sensor to siding")
        sensor = self.setSensor(sidingBranch)     # a siding branch
        noTrucksToDetect = 0            #we are not moving trucks, we are only detecting the first one at the beginning of it.
        self.countTrucksInactive(noTrucksToDetect, sensor, direction, sidingBranch)  # leave the moving to the next movement




    @print_name(True)
    def moveToDisconnectPosition(self, noTrucksOnTrain, noTrucksToAdd, sidingBranch):

        self.indent()
        noTrucksToCount = abs(noTrucksToAdd)    #Trucks to add to train
        self.dialogs.displayMessage("moveToDisconnectPosition")
        if noTrucksToAdd >= 0:   # picking up trucks
            # operation = "PICKUP"
            # direction = self.setPointsAndDirection(sidingBranch, self.spur_branch)
            # sensor = self.setSensor(sidingBranch)
            # self.countTrucksActive(noTrucksToCount, sensor, direction, sidingBranch)  # counts from 0     $$$$$$$$$$$$$changed$$$$$$$$$$$$$$
            # self.set_delay_if_not_simulation(2000)
            operation = "PICKUP"

            # print "in operation", operation
            repeat = True
            self.index2 = 1
            while repeat:
                self.rectify_flag2 = True
                # print "in repeat 3 " , "iteration", self.index2 , "starts from 1"
                self.dialogs.displayMessage1("repeating moveToDisconnectPosition")
                self.sidingBranch = sidingBranch                    # needed for alternate_function decorator: see count_at_siding__is_there_a_truck_error_if_none
                self.noTrucksToCount = 1                             # needed for alternate_function decorator: see is_thecount_at_siding__is_there_a_truck_error_if_nonere_a_truck
                self.simulate = True

                # stage1 count 1 truck and time out if there is none (it is an error if there is none and we don't want to wait until the time for all the trucks before timing outy

                # t1 = Thread(target=self.count_at_siding__is_there_a_truck_error_if_none, args=(sidingBranch, noTrucksToCount))   #sets rectify_flag false if counts a truck
                # self.time_to_countActive_n_trucks = self.time_to_countInactive_one_truck * noTrucksToCount
                self.simulate = True

                # this sets self.rectify_flag2 if a truck is counted
                # print "self.rectify_flag2 before", self.rectify_flag2
                self.count_at_siding__is_there_a_truck_error_if_none(sidingBranch, self.noTrucksToCount, \
                                self.time_to_countInactive_one_truck, self.simulate, \
                                "moveToDisconnectPosition")    # sets rectify_flag false if counts a truck
                # print "self.rectify_flag2 after", self.rectify_flag2
                # # # and sets stop_thread_sensor
                # t2 = Thread(target=self.count_at_siding, args=(sidingBranch, noTrucksToCount))
                # #
                # t1.start()      # stop_thread_sensor and self.rectify_flag set here if trucks do not uncouple and counts a truck
                # t2.start()      # stops prematurely if stop_thread_sensor set
                # t1.join()
                
                # # self.myprint2("**************** t1 joined")
                # t2.join()
                # self.myprint2("**************** t2 joined", "self.rectify_flag", self.rectify_flag)
                #self.rectify_flag = False
                self.dialogs.displayMessage1("finished stage1 rectify_flag2" + str(self.rectify_flag2))
                if self.rectify_flag2 == True:
                    self.dialogs.displayMessage1("rectify_flag2 " + str(self.rectify_flag2))
                    self.rectify_connect_up_again(sidingBranch)
                    # t3 = Thread(target=self.rectify_connect_up_again, args=(sidingBranch,))
                    # # t4 = Thread(target=self.rectify_trucks_back_to_mid, args=(sidingBranch,))
                    # t3.start()   # moves trucks back to siding
                    # # t4.start()   # move trucks back to mid
                    # t3.join()
                    # # self.myprint2("**************** t3 joined")
                    # # t4.join()
                    # self.myprint2("**************** t4 joined")
                    self.dialogs.displayMessage1("repeating")
                    repeat = True
                else:

                    self.noTrucksToCount = noTrucksToCount - 1  # we have already counted one
                    self.dialogs.displayMessage2("don't need to rectify: counting " + str(self.noTrucksToCount) + " more trucks")
                    direction = self.setPointsAndDirection(sidingBranch, self.spur_branch)
                    sensor = self.setSensor(sidingBranch)
                    self.countTrucksActive(self.noTrucksToCount, sensor, direction, sidingBranch)  # counts from 0
                    self.dialogs.displayMessage1("done all trucks to disconnect not repeating")
                    repeat = False
                self.index2 += 1
                self.myprint2("******************move_to_spur_operations: repeat", repeat,"index2", self.index2)
                self.dialogs.displayMessage2("finished repeat = " + str(repeat) + " index2 " + str(self.index2))

        elif noTrucksToAdd < 0: # dropping off trucks
            operation = "DROPOFF"
            # print "in operation", operation
            if noTrucksToCount > noTrucksOnTrain:
                self.myprint("!!!!>>moveToDisconnectTrucks: dropping off trucks: error not enough trucks")
                crash_here   # does not exist so crashes
            self.myprint2("sidingBranch00", sidingBranch)
            direction = self.setPointsAndDirection(self.spur_branch, sidingBranch)
            self.myprint2("sidingBranch0", sidingBranch)
            sensor = self.setSensor(sidingBranch)
            self.myprint2("sidingBranch1", sidingBranch)
            self.countTrucksActive(noTrucksToCount, sensor, direction, sidingBranch)  # counts from 0
            self.myprint2("sidingBranch2", sidingBranch)
            self.set_delay_if_not_simulation(2000)
            operation = "DROPOFF"
        else:  # noTrucksToAdd == 0:
            operation = "PICKUP"
            pass
        self.myprint("end moveToDisconnectPosition ")
        self.dedent()
        return operation

    def place_trucks_near_disconnect(self, branch):
        if branch != self.spur_branch:
            self.place_trucks_near_disconnect_siding = True
        self.update_displays(self.pegs)

    def strip_0(self, pegs):
        list1 = []
        # print("*************")
        # print("strip_0 pegs: " , pegs)
        for deque in pegs:
            list = [item for item in deque if item>0]
            list1 .append(list)
        # print("strip_0 list1: " , list1)
        # print("*************")
        return list1

    @print_name()
    def countTrucksInactive(self, noTrucksToCount, sensor, direction, sidingBranch, simulate = True):
        self.indent()
        if self.get_branch_from_sensor(sensor) == self.spur_branch: count_from = -1 #count engine
        else: count_from = 0
        off_count = 99   #dummy value
        if count_from == noTrucksToCount:   #if simulate_countTrucksInactive is not being triggered
            self.update_displays(self.pegs)
        self.myprint2("***************counting the trucks********************", "count_from", count_from)
        self.no_trucks_to_rectify = 0     # required if need to put the trucks back
        for off_count in range(count_from, noTrucksToCount):
            self.myprint2("**************off_count**********************", off_count, "count_from", count_from, "noTrucksToCount", noTrucksToCount )
            # self.stop_thread may be set in either simulate_countTrucksInactive or really_doit_countTrucksInactive
            if simulate:
                self.simulate_countTrucksInactive(sidingBranch, sensor, direction, off_count, self.pegs)
                self.no_trucks_to_rectify = max([off_count, 0]) + 1
            self.really_doit_countTrucksInactive(sensor)
            self.myprint2("finished reallydoit")
            self.myprint2("stop_thread1", self.stop_thread)

            # if self.stop_thread == True:
            #     print ("stop_thread2", self.stop_thread)
            #     if simulate:
            #         self.stop_thread == False
            #         print ("******************moving the trucks back ****************stop_thread3", self.stop_thread)
            #         for off_count1 in range(off_count, count_from, -1):
            #             print ("off_count1", off_count1, "off_count", off_count,"count_from",count_from, "noTrucksToCount", noTrucksToCount )
            #             direction1 = self.swap_direction(direction)
            #             self.simulate_countTrucksInactive(sidingBranch, sensor, direction1, off_count, self.pegs)
            #     break
        self.setSpeed(self.stop)
        self.dedent()

    @print_name()
    def countTrucksActive(self, noTrucksToCount, sensor, direction, sidingBranch, simulate = True):
        self.indent()
        if self.get_branch_from_sensor(sensor) == self.spur_branch: count_from = -1
        else: count_from = 0
        self.myprint3("count_from", count_from)
        if count_from == noTrucksToCount:   #if simulate_countTrucksInactive is not being triggered
            self.update_displays(self.pegs)
        for on_count in range(count_from, noTrucksToCount):
            # if (on_count - count_from) > 0 and simulate:
            if simulate:
                self.simulate_countTrucksActive(sidingBranch, sensor, direction, on_count, self.pegs)
            self.really_doit_countTrucksActive(sensor)
        self.really_doit_countTrucksActive(sensor)          # need an extra count because we are counting the front of the truck
        self.setSpeed(self.stop)
        self.dedent()

    # @print_name()
    # def setPointsAndDirection(self, fromBranch, toBranch):
    #     # one of fromBranch or toBranch must be spur_branch
    #     self.indent()
    #     if self.spur_branch not in [fromBranch, toBranch]:
    #         self.myprint1("spur_branch ", self.spur_branch , " must be one of ", fromBranch, toBranch)
    #         cresh_here  # crash_here does not exist so crash
    #     self.myprint (">>in setPointsAndDirection ")
    #     self.setPoints(fromBranch,toBranch)
    #     direction = self.setDirection(fromBranch, toBranch)
    #     self.myprint ("end setPointsAndDirection ")
    #     self.dedent()
    #     return direction

    # @print_name()
    # def setBranch(self, sensor):
    #     self.indent()
    #     self.myprint ("in setBranch ")
    #     self.myprint("setting branch")
    #     branch = 99
    #     if sensor == self.sensor1:
    #         branch = 1
    #     if sensor == self.sensor2:
    #         branch = 2
    #     if sensor == self.sensor3:
    #         branch = 3
    #     if sensor == self.sensor4:
    #         branch = 4
    #     self.myprint("end setting branch")
    #     self.dedent()
    #     return branch

    # @print_name()
    # def setMidBranch(self, sidingBranch):
    #     self.indent()
    #     if type(sidingBranch) != int:
    #         crashhere
    #     self.myprint ("in setBranch ")
    #     self.myprint("setting branch")
    #     midBranch = sidingBranch + 4
    #     self.dedent()
    #     # print ("setMidBranch: branch", sidingBranch, "modBranch", midBranch)
    #     return midBranch

    # @print_name()
    # def setSensor(self, branch):
    #     self.indent()
    #     self.myprint ("in setSensor ")
    #     self.myprint("setting sensor")
    #     if branch == 1:
    #         sensor = self.sensor1
    #     if branch == 2:
    #         sensor = self.sensor2
    #     if branch == 3:
    #         sensor = self.sensor3
    #     if branch == 4:
    #         sensor = self.sensor4
    #     # self.myprint2("end setting sensor", "branch", branch, "sensor", sensor)
    #     self.dialogs.displayMessage("end setting sensor: branch " + str(branch) + " sensor " + str(sensor))
    #     self.dedent()
    #     return sensor

    # @print_name()
    # def couple1(self, sidingBranch, timeCouple = 350):   #we use self.couple for a speed, so use couple1
    #
    #     self.indent()
    #     self.myprint("in couple")
    #
    #     self.setDirection(self.spur_branch, sidingBranch)
    #     # timeCouple = 350
    #     self.mysound()
    #     self.setSpeedSetDelay(self.couple, timeCouple)
    #     self.mysound()
    #     self.setSpeedSetDelay(self.stop,1000)
    #     self.mysound()
    #     #self.setPointsAndDirection(toBranch, fromBranch)
    #     #timeReturn = 10
    #     #self.setSpeedSetDelay(self.slow, timeReturn)
    #     #self.setSpeedSetDelay(self.stop,1000)
    #     self.myprint("finished couple part 2 waiting 2 secs")
    #     #self.myprint("finished couple part 3")
    #
    #     self.myprint("finished couple")
    #     self.dedent()
    # @print_name()
    # def uncouple1(self, sidingBranch, operation):     #we use self.uncouple as a speed, so use uncouple1
    #     self.indent()
    #     sensor = self.setSensor(sidingBranch)
    #     self.setSpeed(self.stop)
    #     if operation == "PICKUP":
    #         self.myprint("in uncouple 1")
    #         self.myprint("in pickup")
    #
    #         # #whiz forward
    #         # self.setPointsAndDirection(fromBranch, toBranch)
    #         # self.setSpeed(self.uncouple)
    #         # #self.set_delay_if_not_simulation(500)
    #         # #count twice 'cos in active
    #         # #waitChangeActive(sensor)    # sets speed 0
    #         # noTrucksToCount = 1  # starts from 0 ( we are in a truck so that is 0
    #         # self.countTrucksActive(noTrucksToCount, sensor)
    #         # self.setSpeed(stop)
    #         self.mysound()
    #         self.set_delay_if_not_simulation(1000)
    #
    #
    #         #whiz back
    #         self.myprint("in whizback")
    #
    #         direction = self.setDirection(self.spur_branch, sidingBranch)
    #         self.setSpeedSetDelay(self.uncouple,50)
    #         #self.set_delay_if_not_simulation(1000)
    #         noTrucksToCount = 1
    #         self.myprint("countTrucksInactive1", sensor)
    #         simulate = False
    #         self.countTrucksActive(noTrucksToCount, sensor, direction, sidingBranch, simulate)       # change to active so only a little whiz
    #         #waitChangeInactive(sensor)  # sets speed 0
    #         self.myprint("countTrucksInctive returned")
    #         self.setSpeed(self.stop)
    #         self.set_delay_if_not_simulation(1000)
    #
    #         #whiz forward again
    #         self.myprint("in forward again")
    #         direction = self.setDirection(sidingBranch, self.spur_branch)
    #         self.setSpeedSetDelay(self.fast, 100)
    #         #self.set_delay_if_not_simulation(100) # need to be times because has dropped off truck
    #         #waitChangeActive(sensor)    # sets speed 0
    #         # noTrucksToCount = 1
    #         # self.countTrucksInactive(noTrucksToCount, sensor, direction, sidingBranch, simulate)    # change to active
    #         # self.setSpeedSetDelay(self.stop,100)
    #         self.myprint("end whiz forward")
    #         self.myprint("in uncouple 1a")
    #
    #     if operation == "DROPOFF":
    #         self.myprint("in uncouple 2")
    #         #whiz back
    #         self.mysound()
    #         self.set_delay_if_not_simulation(1000)
    #
    #
    #         #whiz back
    #         self.myprint("in whizback")
    #
    #         # self.setPointsAndDirection(toBranch, fromBranch)
    #         # self.setSpeedSetDelay(self.uncouple,50)
    #         # #self.set_delay_if_not_simulation(1000)
    #         # noTrucksToCount = 1
    #         # self.countTrucksInactive(noTrucksToCount, sensor)
    #         # #waitChangeInactive(sensor)  # sets speed 0
    #         # self.myprint("countTrucksActive returned")
    #         # self.setSpeed(self.stop)
    #         # self.set_delay_if_not_simulation(1000)
    #
    #         #whiz forward again
    #         self.myprint("in forward again")
    #         direction = self.setPointsAndDirection(sidingBranch, self.spur_branch)
    #         self.setSpeedSetDelay(self.fast, 100)
    #         #self.set_delay_if_not_simulation(100) # need to be times because has dropped off truck
    #         #waitChangeActive(sensor)    # sets speed 0
    #         # noTrucksToCount = 1
    #         # self.countTrucksActive(noTrucksToCount, sensor)
    #         self.setSpeedSetDelay(self.stop,100)
    #         self.myprint("end whiz forward")
    #         self.myprint("in drop off")
    #         direction = self.setPointsAndDirection(self.spur_branch, sidingBranch)
    #         self.setSpeedSetDelay(self.fast,100)
    #         #waitChangeInactive(sensor)  # sets speed 0
    #         self.setSpeed(self.stop)
    #         self.myprint("end in dropoff")
    #         self.myprint2("in uncouple 2a")
    #     self.dedent()
    #     self.dialogs.displayMessage("end uncouple1 branch ")
    #     self.myprint2("in uncouple3")
    #     logging = "noprint"

    # #@print_name()
    # def swapRouteSameDirectionTravelling(self, fromBranch, toBranch):
    #     self.indent()
    #     self.myprint ("in swapRouteSameDirectionTravelling ")
    #     self.setPointsAndDirection(fromBranch, toBranch)
    #     self.dedent()
    #
    # #@print_name()
    # def swapRouteOppDirectionTravelling(self, fromBranch, toBranch):
    #     self.indent()
    #     self.myprint ("in swapRouteOppDirectionTravelling ")
    #     self.setPointsAndDirection(fromBranch, toBranch)
    #     self.dedent()


    # #@print_name()
    # def noTrucksOnBranches(self, pegs):
    #     noTrucksList = [len(x) for x in pegs]
    #     return noTrucksList
    #
    # #@print_name()
    # def noTrucksOnBranch(self, pegs, branch):
    #     NoTrucks = len(pegs[branch - 1])
    #     return NoTrucks

    # #@print_name()
    # def moveDistance(self, distance):
    #     self.indent()
    #     self.myprint("moving " , distance)
    #     self.setSpeed(self.vslow)
    #     if distance == self.smallDistance:
    #         self.set_delay_if_not_simulation(1000)
    #     else:
    #         self.set_delay_if_not_simulation(1000)
    #     self.setSpeed(self.stop)
    #     self.set_delay_if_not_simulation(500)
    #     self.dedent()

    # #@print_name()
    # def sensorName(self, sensor) :
    #     self.indent()
    #     #self.myprint ("in sensorName ")
    #     if sensor == self.sensor1:
    #         self.dedent()
    #         return "Sensor1"
    #     elif sensor == self.sensor2:
    #         self.dedent()
    #         return "Sensor2"
    #     elif sensor == self.sensor3:
    #         self.dedent()
    #         return "Sensor3"
    #     elif sensor == self.sensor4:
    #         self.dedent()
    #         return "Sensor4"
    #     else:
    #         self.dedent()
    #         return "Invalid"

    # Define routine to map status numbers to text
    #@print_name()
    # def stateName(self, state) :
    #     self.indent()
    #     self.myprint ("in stateName ")
    #     if (state == ACTIVE) :
    #         self.dedent()
    #         return "ACTIVE"
    #     if (state == INACTIVE) :
    #         self.dedent()
    #         return "INACTIVE"
    #     if (state == INCONSISTENT) :
    #         self.dedent()
    #         return "INCONSISTENT"
    #     if (state == UNKNOWN) :
    #         self.dedent()
    #         return "UNKNOWN"
    #     self.dedent()
    #     return "(invalid)"

    def storeSensorFrom(self, sensor):
        self.sensor_from_stored = sensor
    #self.sensor_from_name = "sensor_from_stored" #this is done at declaration time

    def storeSensorTo(self, sensor):
        self.sensor_to_stored = sensor
        #self.sensor_to_name = "sensor_to_stored" #this is done at declaration time

    def storeSensor(self, sensor):
        self.sensor_stored = sensor
        #self.sensor_name = "sensor_stored"    #this is done at declaration time

    def storeFunction(self, function):
        self.function_stored = function
        #self.function_name = "function_stored"    #this is done at declaration time

    def storeCount(self, count):
        self.count_stored = count
        #self.count_name = "count_stored"    #this is done at declaration time

    def storeTimeout(self, timeout):
        self.timeout_stored = timeout
        #self.timeout

    def myprint5(self, *args):
        # tn = threading_local.thread_name
        # print "tn", tn
        if True:
            self.myprint00(*args)    #prefix with <#

    def myprint4(self, *args):
        # tn = threading_local.thread_name
        # print "tn", tn
        if False:
            self.myprint00(*args)    #prefix with <#
    def myprint3(self, *args):
        if False:
            self.myprint0(*args)
    def myprint2(self, *args):
        if True:
            self.myprint0(*args)
    def myprint1(self, *args):
        if False:
            self.myprint0(*args)

    def myprint(self, *args):
        if False:
            self.myprint0(*args)

    # def myprint0(self, *args):
    #
    #     # indenta = glb.indenta    # glb.indenta set up in decorator print_name
    #     indenta = 0
    #     print(" " * self.indentno),
    #     print(" " * indenta),
    #     print("<"),
    #     for arg in args:
    #         print (arg),
    #     print("")
    #
    # def myprint00(self, *args):
    #
    #     # indenta = glb.indenta    # glb.indenta set up in decorator print_name
    #     indenta = 0
    #     print(" " * self.indentno),
    #     print(" " * indenta),
    #     print("<"),
    #     for arg in args:
    #         print (arg),
    #     print("")

    def myprint00(self, *args):
        try:
            tn = threading_local.thread_name
        except:
            tn = ""
        if tn == "truck": indenta = 10
        elif tn == "count": indenta = 20
        elif tn == "rectify_mid": indenta = 30
        elif tn == "rectify_sid": indenta = 40
        else: indenta = 0
        # indenta = glb.indenta    # glb.indenta set up in decorator print_name
        # print "tn", tn, "indenta", indenta
        print(" " * self.indentno),
        print(" " * indenta),
        print("<#"),
        print tn,
        for arg in args:
            print (arg),
        print("")

    def myprint0(self, *args):
        try:
            tn = threading_local.thread_name
        except:
            tn = ""
        if tn == "truck": indenta = 10
        elif tn == "count": indenta = 20
        elif tn == "rectify_mid": indenta = 30
        elif tn == "rectify_sid": indenta = 40
        else: indenta = 0
        # indenta = glb.indenta    # glb.indenta set up in decorator print_name
        # print "tn", tn, "indenta", indenta
        print(" " * self.indentno),
        print(" " * indenta),
        print("<"),
        print tn,
        for arg in args:
            print (arg),
        print("")

    def set_indent(self, function_name):
        # print "in set_indent"
        try:
            tn = threading_local.thread_name
        except:
            tn = ""
        if tn == "truck": indenta = 10
        elif tn == "count": indenta = 20
        elif tn == "rectify_mid": indenta = 30
        elif tn == "rectify_sid": indenta = 40
        elif function_name == "is_there_a_truck_at_siding_error_if_true": indenta = 10
        elif function_name == "count_at_spur": indenta = 20
        else: indenta = 0
        # print "finished set_indent"
        return indenta

    def set_entry_prompt(self, function_name):
        try:
            tn = threading_local.thread_name
        except:
            tn = ""

        if tn == "truck": prompt = ">>thread truck: "
        elif tn == "count": prompt = ">>thread count: "
        elif tn == "rectify_mid": prompt = ">>thread recmid: "
        elif tn == "rectify_sid": prompt = ">>thread recsid: "
        elif function_name == "is_there_a_truck_at_siding_error_if_true": indenta = 10
        elif function_name == "count_at_spur": indenta = 20
        else: prompt = ">>qwerty"
        return prompt

    def set_exit_prompt(self, function_name):
        try:
            tn = threading_local.thread_name
        except:
            tn = ""

        if tn == "truck": prompt = "<<thread truck: "
        elif tn == "count": prompt = "<<thread count: "
        elif tn == "rectify_mid": prompt = "<<thread recmid: "
        elif tn == "rectify_sid": prompt = "<<thread recsid: "
        elif function_name == "is_there_a_truck_at_siding_error_if_true": indenta = 10
        elif function_name == "count_at_spur": indenta = 20
        else: prompt = "<<qwerty"
        return prompt

    # def myprint1(self, *args):
    #
    #     if self.display_message_flag == None:
    #         self.display_message_flag = False
    #
    #     #if self.display_message_flag:
    #     if False:
    #         print(" " * self.indentno),
    #         for arg in args:
    #             print (arg),
    #         print("")
    #         msg = " " * self.indentno
    #         #print(msg + "!")
    #         for arg in args:
    #             msg = msg + " " + str(arg)
    #         #logging.debug(msg)
    #     #     print "display_message_flag myprint1", self.display_message_flag
    #     # else:
    #     #     print "display_message_flag myprint1", self.display_message_flag


    # # use external "nircmd" command to "speak" some text  (I prefer this voice to eSpeak)
    # def speak(self,msg) :
    # #uncomment next line for speech (Jenkins doesn't like this command)
    # print("about to speak")
    # java.lang.Runtime.getRuntime().exec('Z:\\ConfigProfiles\\jython\\sound2\\nircmd speak text "' + msg +'"')
    # return


    def indent(self):

        # self.setprompt()

        self.indentno = self.indentno + 2

    def dedent(self):
        self.indentno = self.indentno - 2

    def alt_action_countTrucksInactive(self,sensor):
        self.indent()
        self.myprint ("in alt_action_countTrucksActive1 ")
        #speak("in alt_action_countTrucksActive1")
        self.myprint ("end alt_action_countTrucksActive1 ")
        self.dedent()

    def alt_action_countTrucksActive2(self, fromSensor):
        global glb_count
        #self.indent()
        self.myprint ("in alt_action_countTrucksActive2 ")


        self.setSpeed(self.stop)

        self.myprint("WAITING")
        self.waitMsec(10000)

        sp = Speak()

        sp.speak("in alt_action_countTrucksActive2")
        self.waitMsec(5000)

        #change direction of travel
        self.myprint ("sensor:", fromSensor)

        mySensorName = self.sensorName(fromSensor)
        sp.speak("at sensor " + mySensorName)

        #move back to sensorFrom
        self.myprint("alt_action_countTrucksActive2 w")
        fromBranch = None
        self.myprint("alt_action_countTrucksActive2 w1")
        fromBranch = self.setBranch(fromSensor)
        self.myprint("alt_action_countTrucksActive2 x")

        self.myprint("No trucks to return glb_count" , glb_count)
        noTrucksToReturn = glb_count
        self.returnToBranch(self.noTrucksOnTrain, noTrucksToReturn, fromBranch)

        self.myprint("glb_count after returnToBranch" , glb_count)


        self.myprint("alt_action_countTrucksActive2 y")

        self.setSpeed(self.stop)
        self.moveDistance(self.smallDistance)
        self.couple1(fromBranch)
        self.changeDirection()
        self.moveDistance(self.smallDistance)
        self.myprint("alt_action_countTrucksActive2 z")

        sensor = self.setSensor(4)
        self.myprint("noTrucksToCountAgain glb_count" , glb_count)
        noTrucksToCountAgain = glb_count
        self.myprint("noTrucksToCountAgain " , noTrucksToCountAgain)
        self.countTrucksAgain(noTrucksToCountAgain, fromSensor)

        self.myprint("WAITING")
        speak("We have recounted the trucks successfully")
        self.waitMsec(10000)
        self.dedent()

    def returnToBranch(self, noTrucksOnTrain, noTrucksToMove, destBranch):
        self.indent()
        # move the train to destbranch without any coupling or decoupling
        # we have already checked that the branch we are in is not destBranch
        self.myprint(">>in returnToBranch")
        self.myprint("noTrucksToMove " + str(noTrucksToMove) + " destBranch " + str(destBranch))



        if destBranch != 4:
            #announce that are moving trucks
            #speak = ("moving to branch " + str(destBranch))

            self.myprint("destBranch != 4:"+ str(destBranch))
            direction = self.setPointsAndDirection(4,destBranch)
            self.waitMsec(5000)
            noToCount = noTrucksToMove
            sensor = self.setSensor(destBranch)
            self.myprint("returnToBranch 0")
            #self.countTrucksActive(noTrucksToMove, sensor)

            #self.setSpeed(self.slow)
            self.countTrucksActive(noToCount, sensor, direction, withRecovery = False)  # leave the moving to the next movement
            self.myprint("returnToBranch 1")

            #self.myprint("about to couple")
            #self.couple1(destBranch)
            self.setSpeed(self.stop)
            self.myprint("returnToBranch 2")
        else:
            #speak = ("moving to head")
            self.myprint("moving to branch 4")
            #the points will have been set as we are moving back to branch 4
            anyBranch = 1  # choose any branch, the direction is the same
            direction = self.setDirection(anyBranch,4)
            #self.setSpeed(self.slow)
            # going towards head count number of times becomes inactive

            sensor = self.setSensor(destBranch)
            self.myprint ("noTrucksOnTrain before = ", self.noTrucksOnTrain)
            self.myprint ("noTrucksToMove before = ", noTrucksToMove)
            self.noTrucksOnTrain += noTrucksToMove
            self.myprint ("noTrucksOnTrain after = ", self.noTrucksOnTrain)
            extra = 1 # for engine count
            #speak("counting"+str(self.noTrucksOnTrain)+"trucks and engine")
            self.countTrucksActive(self.noTrucksOnTrain + extra, sensor, direction, withRecovery = False) #counting all trucks on train
            self.setSpeed(self.stop)

        self.myprint("end returnToBranch: " + "noTrucksToMove " + str(noTrucksToMove) + " destBranch " + str(destBranch))
        self.dedent()

    def countTrucksAgain(self, noTrucksToCount, sensor):
        # the number of trucks to count is the number already counted plus 1 (including the failed one)
        self.indent()
        self.myprint("In countTrucksAgain")
        self.setSpeed(self.stop)
        self.myprint("Calling countTrucksActive")
        self.countTrucksActive(noTrucksToCount, sensor, direction, withRecovery = False)
        self.myprint("counted the trucks successfully")
        self.setSpeed(self.stop)

    def get_turnout_str(self):
        turnout_str = ["to_long_siding", "to_short_sidings", "to_main"]
        return turnout_str

    def get_turnout(self, turnout_str):
        # print "get_to: qwerty", 'IMIS:the_turnout_' + turnout_str
        turnout = memories.getMemory('IMIS:the_turnout_' + turnout_str)
        if turnout != None:
            # print "$$$$$$$$$$$$$$$$", turnout, 'IMIS:the_turnout_' +turnout_str
            # print "value", turnout.getValue()
            return turnout.getValue()
        else:
            return None


    def get_turnout_directions(self):

        [turnout_short_dir, turnout_long_dir, turnout_main_dir] = self.get_turnout_dir_str()

        turnout_short_direction = self.get_turnout_direction(turnout_short_dir)
        turnout_long_direction = self.get_turnout_direction(turnout_long_dir)
        turnout_main_direction = self.get_turnout_direction(turnout_main_dir)

        return [turnout_short_direction, turnout_long_direction, turnout_main_direction]

    def get_turnout_direction(self, turnout_str):
        # print "********************************turnout_str", 'IMIS:turnout_dir_' + turnout_str
        turnout_dir = memories.getMemory('IMIS:turnout_dir_' + turnout_str)
        if turnout_dir != None:
            # print "$$$$$$$$$$$$$$$$", turnout_dir, 'IMIS:turnout_dir_' + turnout_str
            return turnout_dir.getValue()
        else:
            return None

    def get_turnout_dir_str(self):

        turnout_dir_str = ["to_long", "to_2", "to_main"]
        return turnout_dir_str

    def get_engine(self):
        engine = memories.getMemory('IMIS:engine')
        if engine != None:
            # print "$$$$$$$$$$$$$$$$", engine, 'IMIS:engine'
            return engine.getValue()
        else:
            return None

    def get_dcc_address(self):
        engine = self.get_engine()
        # print "engine ", str(engine)

        if engine != None:
            r = jmri.jmrit.roster.Roster.getDefault()

            for roster_entry in jmri.jmrit.roster.Roster.getAllEntries(r):
                # print "roster_entry.getId", roster_entry.getId()
                if str(roster_entry.getId()) == str(engine):
                    return roster_entry.getDccAddress()
                # print roster_entry.getId()
        else:
            return None

    # def setprompt(self):
    #     # global prompt, prompt1
    #     # global indenta
    #     function_names_in_stack = [x[3] for x in inspect.stack()]
    #     # print "a", function_names_in_stack
    #     # print function_name
    #     # function_names_in_stack.append (function_name)
    #     is_there_a_truck_in_hierarchy = function_names_in_stack.count("is_there_a_truck")
    #     count_at_spur_in_hierarchy = function_names_in_stack.count("count_at_spur")
    #     rectify_mid_in_hierarchy = function_names_in_stack.count("rectify_trucks_back_to_mid")
    #     rectify_sid_in_hierarchy = function_names_in_stack.count("rectify_trucks_back_to_siding")
    #
    #     # indent 10 if is_there_a_tryck is in the hierarchy, 20 if count_at_spur in hierasrchy etc. Only one should appear at a time
    #     self.indenta = 10 * is_there_a_truck_in_hierarchy + 20 * count_at_spur_in_hierarchy + \
    #               10 * rectify_mid_in_hierarchy + 20 * rectify_sid_in_hierarchy
    #
    #     # if is_there_a_truck_in_hierarchy:
    #     if rectify_mid_in_hierarchy > 0:
    #         self.prompt = ">>thread recmid: "
    #         self.prompt1 = "<<thread recmid: "
    #     elif rectify_sid_in_hierarchy > 0:
    #         self.prompt = ">>thread recsid: "
    #         self.prompt1 = "<<thread recsid: "
    #     elif is_there_a_truck_in_hierarchy > 0:
    #         self.prompt = ">>thread truck: "
    #         self.prompt1 = "<<thread truck: "
    #     elif count_at_spur_in_hierarchy > 0:
    #         self.prompt = ">>thread count: "
    #         self.prompt1 = "<<thread count: "
    #     else:
    #         self.prompt = ">>>>>>>calling: "
    #         self.prompt1 = "<<<<<<<called:  "
