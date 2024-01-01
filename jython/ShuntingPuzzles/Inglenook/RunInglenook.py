###############################################################################
#
# class OptionDialog
# Some Swing dialogs
#

# class OffActionMaster *
# allows actions when buttons are turned off
#
# class ResetButtonMaster *
# if a button is turned on, this class turns off all the others.
# allows only one station button to be active at a time
#
# class MoveTrain
# Calls dispatcher to move train from one station to another
# given engine and start and end positions
#
# class InglenookMaster *
#
#
# class RunInglenookMaster
# starts the classes marked with * above in threads so they can do their work
#
#
###############################################################################
import java
import jmri
import re
from javax.swing import JOptionPane
import os
import imp
import copy
import org

from javax.swing import JOptionPane, JFrame, JLabel, JButton, JTextField, JFileChooser, JMenu, JMenuItem, JMenuBar,JComboBox,JDialog,JList

import sys

# # include the graphcs library
# my_path_to_jars = jmri.util.FileUtil.getExternalFilename('scripts:DispatcherSystem/jars/jgrapht.jar')
# sys.path.append(my_path_to_jars) # add the jar to your path
# from org.jgrapht.alg import DijkstraShortestPath
# from org.jgrapht.graph import DefaultWeightedEdge
# from org.jgrapht.graph import DirectedWeightedMultigraph

#allow import of pyj2D
my_path_to_pyj2d = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/jars')
sys.path.append(my_path_to_pyj2d)  # add my_path_to_pyj2d to your path

# my_path_to_pyj2d = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/pyj2d2/pyj2d.jar')
# sys.path.append(my_path_to_pyj2d)  # add my_path_to_pyj2d to your path
import pyj2d as pygame

#allow import of inglenook and other classes in py files in directory Inglenook
inglenook = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/Inglenook')
sys.path.append(inglenook)  # add my_path_to_pyj2d to your path
import inglenook



#############################################################################################
#from inglenookMaster import RunInglenook
InglenookMaster1 = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/Inglenook/inglenookMaster.py')
execfile(InglenookMaster1)

MoveTrain = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/Inglenook/move_train.py')
exec(open (MoveTrain).read())

#import inglenook

#exec(open (InglenookMaster).read())

#
# Set some global variables
#

logLevel = 0          # for debugging
trains = {}           # dictionary of trains shared over classes
instanceList=[]       # instance list of threads shared over classes
g = None              # graph shared over classes

time_to_stop_in_station = 10000   # time to stop in station in stopping mode(msec)

#############################################################################################
# the file was split up to avoid errors
# so now include the split files

# FileMoveTrain has to go before CreateScheduler
# FileMoveTrain = jmri.util.FileUtil.getExternalFilename('program:jython/DispatcherSystem/MoveTrain.py')
# execfile(FileMoveTrain)
#
# CreateScheduler = jmri.util.FileUtil.getExternalFilename('program:jython/DispatcherSystem/Scheduler.py')
# execfile(CreateScheduler)
#
# LogixNG_functions = jmri.util.FileUtil.getExternalFilename('program:jython/DispatcherSystem/Simulation.py')
# execfile(LogixNG_functions)

#LogixNG_functions = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntinPuzzles/Inglenook/logicNGScripts/getSidingSensor.py')
#execfile(LogixNG_functions)

#############################################################################################

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

class modifiableJComboBox:

    def __init__(self,list, msg):
        #list = self.get_all_roster_entries()
        jcb = JComboBox(list)
        jcb.setEditable(True)
        JOptionPane.showMessageDialog( None, jcb, msg, JOptionPane.QUESTION_MESSAGE)
        self.ans = str(jcb.getSelectedItem())

    def return_val(self):
        return self.ans



class StopMaster(jmri.jmrit.automat.AbstractAutomaton):

    def __init__(self):
        self.logLevel = 0
        if self.logLevel > 0: print 'Create Stop Thread'
        self.opd = OptionDialog()

    def setup(self):
        self.stop_master_sensor = sensors.getSensor("stopInglenookSensor")
        if self.stop_master_sensor is None:
            return False
        self.stop_master_sensor.setKnownState(INACTIVE)

        # self.start_scheduler = sensors.getSensor("startSchedulerSensor")
        # self.start_scheduler.setKnownState(INACTIVE)
        return True

    def handle(self):
        global timebase
        self.waitSensorActive(self.stop_master_sensor)
        #self.stop_master_sensor.setKnownState(INACTIVE)

        print "waited"
        msg = "stop or list threads"
        title = "Transits"
        opt1 = "stop"
        opt2 = "list threads"

        requested_action = self.opd.customQuestionMessage2str(msg, title, opt1, opt2)
        if self.opd.CLOSED_OPTION == True:
            self.stop_master_sensor.setKnownState(INACTIVE)
            #self.reset_start_sensor()
            return True
        if requested_action == opt1:
            #
            self.stop_all_threads()
            #self.stop_master_sensor.setKnownState(INACTIVE)
            self.reset_start_sensor()
            return False
        else:
            #self.reset_start_sensor()
            self.list_all_threads()
            #self.stop_master_sensor.setKnownState(INACTIVE)
            self.reset_start_sensor()
            return False

        #return True

    def reset_start_sensor(self):
        self.new_train_sensor = sensors.getSensor("startInglenookSensor")
        self.new_train_sensor.setKnownState(INACTIVE)

    def stop_all_threads(self):
        try:
            summary = jmri.jmrit.automat.AutomatSummary.instance()
            automatsList = java.util.concurrent.CopyOnWriteArrayList()
            for automat in summary.getAutomats():
                automatsList.add(automat)

            for automat in automatsList:
                automat.stop()
        except:
            pass
    def list_all_threads(self):
        summary = jmri.jmrit.automat.AutomatSummary.instance()
        automatsList = java.util.concurrent.CopyOnWriteArrayList()
        for automat in summary.getAutomats():
            automatsList.add(automat)

        for automat in automatsList:
            if automat.isRunning():
                print 'automatList "{}" thread running'.format(automat.getName())
            else:
                print 'automatList "{}" thread not running'.format(automat.getName())

    # def remove_listener(self):
    #     try:
    #         #stop the scheduler timebase listener
    #         if self.logLevel > 0: print "removing listener"
    #         timebase.removeMinuteChangeListener(TimeListener())
    #         return False
    #     except NameError:
    #         if self.logLevel > 0: print "Name error"
    #         return False
    #     else:
    #         return False
    #
    # def delete_active_transits(self):
    #
    #     DF = jmri.InstanceManager.getDefault(jmri.jmrit.dispatcher.DispatcherFrame)
    #     activeTrainsList = DF.getActiveTrainsList()
    #     for i in range(0, activeTrainsList.size()) :
    #         activeTrain = activeTrainsList.get(i)
    #         DF.terminateActiveTrain(activeTrain)

# End of class StopMaster

class OffActionMaster(jmri.jmrit.automat.AbstractAutomaton):

    button_sensors_to_watch = []
    def __init__(self):
        self.logLevel = 0

    def init(self):
        if self.logLevel > 0: print 'Create OffActionMaster Thread'
        self.get_run_buttons()
        self.get_route_dispatch_buttons()

        self.button_sensors_to_watch = self.run_stop_sensors
        if self.logLevel > 0: print "button to watch" , str(self.button_sensors_to_watch)
        #wait for one to go inactive
        button_sensors_to_watch_JavaList = java.util.Arrays.asList(self.button_sensors_to_watch)
        self.waitSensorState(button_sensors_to_watch_JavaList, INACTIVE)

        if self.logLevel > 0: print "button went inactive"
        sensor_that_went_inactive = [sensor for sensor in self.button_sensors_to_watch if sensor.getKnownState() == INACTIVE][0]
        if self.logLevel > 0: print "sensor_that_went_inactive" , sensor_that_went_inactive
        start_sensor = sensors.getSensor("startInglenookSensor")
        stop_sensor =  sensors.getSensor("stopInglenookSensor")
        if self.logLevel > 0: print "start_sensor" , start_sensor
        if self.logLevel > 0: print "stop_sensor" , stop_sensor
        if sensor_that_went_inactive in self.run_stop_sensors:
            if self.logLevel > 0: print "run stop sensor went inactive"

            if sensor_that_went_inactive == start_sensor:
                self.sensor_to_look_for = stop_sensor
                if self.logLevel > 0: print "start sensor went inactive"
                if self.logLevel > 0: print "setting stop sensor active"
                stop_sensor.setKnownState(ACTIVE)
                # self.waitMsec(5000)
                # if self.logLevel > 0: print "setting start sensor active"
                # start_sensor.setKnownState(ACTICE)
            elif sensor_that_went_inactive == stop_sensor:
                self.sensor_to_look_for = start_sensor
                if self.logLevel > 0: print "stop sensor went inactive"
                if self.logLevel > 0: print "setting start sensor active"
                start_sensor.setKnownState(ACTIVE)
                # self.waitMsec(5000)
                # start_sensor.setKnownState(ACTICE)
                pass#

        if self.logLevel > 0: print "finished OffActionMaster setup"

    def setup(self):
        if self.logLevel > 0: print "starting OffActionMaster setup"
        #get dictionary of buttons self.button_dict
        #self.get_route_dispatch_buttons()

        return True

    def handle(self):
        if self.logLevel > 0: print "started handle"
        #for pairs of buttons, if one goes off the other is set on
        #self.button_sensors_to_watch = self.run_sensor_to_look_for
        if self.logLevel > 0: print "button to watch" , str(self.button_sensors_to_watch)
        #wait for one to go active
        button_sensors_to_watch_JavaList = java.util.Arrays.asList(self.button_sensors_to_watch)
        self.waitSensorState(button_sensors_to_watch_JavaList, INACTIVE)
        #determine which one changed
        if self.logLevel > 0: print "sensor went inactive"
        sensor_that_went_inactive = [sensor for sensor in self.button_sensors_to_watch if sensor.getKnownState() == INACTIVE][0]

        if sensor_that_went_inactive in self.run_stop_sensors:
            if self.logLevel > 0: print "run stop sensor went inactive"
            start_sensor = sensors.getSensor("startInglenookSensor")
            stop_sensor =  sensors.getSensor("stopInglenookSensor")
            if sensor_that_went_inactive == start_sensor:
                self.sensor_to_look_for = stop_sensor
                if self.logLevel > 0: print "start sensor went inactive"
                if self.logLevel > 0: print "setting stop sensor active"
                stop_sensor.setKnownState(ACTIVE)
                # self.waitMsec(5000)
                # if self.logLevel > 0: print "setting start sensor active"
                # start_sensor.setKnownState(ACTICE)
            elif sensor_that_went_inactive == stop_sensor:
                self.sensor_to_look_for = start_sensor
                if self.logLevel > 0: print "stop sensor went inactive"
                if self.logLevel > 0: print "setting start sensor active"
                start_sensor.setKnownState(ACTIVE)

        if self.logLevel > 0: print "end handle"
        #self.waitMsec(20000)
        return False
    def get_route_dispatch_buttons(self):
        self.setup_route_or_run_dispatch_sensors = [sensors.getSensor(sensorName) for sensorName in ["setDispatchSensor","setRouteSensor","setStoppingDistanceSensor"]]
        #self.route_dispatch_states = [self.check_sensor_state(rd_sensor) for rd_sensor in self.setup_route_or_run_dispatch_sensors]
        pass

    def get_run_buttons(self):
        self.run_stop_sensors = [sensors.getSensor(sensorName) for sensorName in ["startInglenookSensor"]]

class RunInglenookMaster():

    def __init__(self):
        global g
        global le
        global indentno

        indentno = 0

        #my_path_to_jars = jmri.util.FileUtil.getExternalFilename('program:jython/DispatcherSystem/jars/jgrapht.jar')
        #import sys
        #sys.path.append(my_path_to_jars) # add the jar to your path
        #CreateGraph = jmri.util.FileUtil.getExternalFilename('program:jython/DispatcherSystem/CreateGraph.py')
        #exec(open (CreateGraph).read())

        # le = LabelledEdge
        # g = StationGraph()

        # new_train_master = NewTrainMaster()      #this used to respond to the setup train button
        # instanceList.append(new_train_master)
        # if new_train_master.setup():
        #     new_train_master.setName('New Train Master')
        #     new_train_master.start()

        # Inglenook_run2 = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/inglenook/inglenook_run2.py')
        # exec(open (Inglenook_run2).read())

        # StartInglenook = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/inglenook/startInglenookSystem.py')
        # exec(open (StartInglenook).read())

        # Inglenook = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/inglenook/inglenook.py')
        # exec(open (Inglenook).read())
        print "starting InglenookMaster"
        run_inglenook = InglenookMaster()                  #need this starts the system
        if run_inglenook.setup():
            print "run_inglenook_setup() returns True"
            run_inglenook.setName('Start Inglenook')
            run_inglenook.start()
            print "started StartInglenookMaster"
        else:
            print "run_inglenook_setup() returns False"

        stop_master = StopMaster()                  #need this stops the system
        if stop_master.setup():
            stop_master.setName('Stop Master')
            stop_master.start()

        off_action_master = OffActionMaster()
        instanceList.append(off_action_master)
        if off_action_master.setup():
            off_action_master.setName('Off-Action Master')
            off_action_master.start()
        else:
            if self.logLevel > 0: print("Off-Action Master not started")

        #set default values of buttons
        sensors.getSensor("justShowSortingInglenookSensor").setKnownState(INACTIVE)
        sensors.getSensor("simulateInglenookSensor").setKnownState(INACTIVE)
        sensors.getSensor("simulateErrorsInglenookSensor").setKnownState(INACTIVE)
        sensors.getSensor("simulateDistributionInglenookSensor").setKnownState(INACTIVE)
        sensors.getSensor("runRealTrainDistributionInglenookSensor").setKnownState(INACTIVE)




if __name__ == '__builtin__':
    pass
    RunInglenookMaster()
    # NewTrainMaster checksfor the new train in siding. Needs to inform what station we are in
    #DispatchMaster checks all button sensors
