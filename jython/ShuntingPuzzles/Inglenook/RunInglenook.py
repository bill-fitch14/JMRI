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

###############################################################################
#allow import of pyj2D
my_path_to_pyj2d = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/jars')
sys.path.append(my_path_to_pyj2d)  # add my_path_to_pyj2d to your path

# my_path_to_pyj2d = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/pyj2d2/pyj2d.jar')
# sys.path.append(my_path_to_pyj2d)  # add my_path_to_pyj2d to your path
import pyj2d as pygame

#allow import of inglenook and other classes in py files in directory Inglenook
inglenook = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/Inglenook')
sys.path.append(inglenook)  # add inglenook to your path
import inglenook

#############################################################################################
InglenookMaster1 = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/Inglenook/inglenookMaster.py')
execfile(InglenookMaster1)

MoveTrain = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/Inglenook/move_train.py')
exec(open (MoveTrain).read())

OptionDialog = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/Inglenook/OptionDialog.py')
exec(open (OptionDialog).read())

OffActionMaster = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/Inglenook/OffActionMaster.py')
exec(open (OffActionMaster).read())

StopMaster = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/Inglenook/StopMaster.py')
exec(open (StopMaster).read())

#
# Set some global variables
#

instanceList=[]       # instance list of threads shared over classes



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
        run_inglenook = InglenookMaster()                   # need this starts the system
        if run_inglenook.setup():
            print "run_inglenook_setup() returns True"
            run_inglenook.setName('Start Inglenook')
            run_inglenook.start()
            print "started StartInglenookMaster"
        else:
            print "run_inglenook_setup() returns False"

        stop_master = StopMaster()                          # need this stops the system
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
        sensors.getSensor("InglenookHelpSensor").setKnownState(INACTIVE)





if __name__ == '__builtin__':
    pass
    RunInglenookMaster()
    # NewTrainMaster checksfor the new train in siding. Needs to inform what station we are in
    #DispatchMaster checks all button sensors
