# Script to automatically Generate Icons on Panel for automation purposes
#
# Author: Bill Fitch, copyright 2022
# Part of the JMRI distribution

from javax.swing import JOptionPane

# IS:ISCT:nnn  Control sensors (on Inglenook Sidings panel)

# IS:ISTI:nnn  Truck Indication sensors
# IS:ISDC:nnn  Decoupling sensors

#   Procedure is:
# Remove Truck Indication Icons
# Remove Decoupling Sensors
# Add Decoupling Sensors
# Add Truck Indication Icons



class processPanels():

    logLevel = 0
    version_no = 1.2    #used to delete InglenookPanel for new versions if the number of controlsensors/icons has changed

    list_of_inglenook_sidings = []
    blockPoints = {}   # Block center points used by direct access process
    editorManager = jmri.InstanceManager.getDefault(jmri.jmrit.display.EditorManager)

    # row number, user name, label name, x offset, y offset
    i = 1
    controlSensors = []
    # note control user names and label names have to be different to DispatcherSystem Names
    # else they will be deleted when Dispatcher Runs and vice-versa
    # as a convention they all contain Inglenook so they are forced to be different
    controlSensors.append([i, 'startInglenookSensor', 'Run Inglenook System', 0, 0]); i += 1
    controlSensors.append([i, 'stopInglenookSensor', 'Stop Inglenook System', 0, 0]); i += 1
    controlSensors.append([i, 'justShowSortingInglenookSensor', 'Just Show Sorting', 10, 5]); i += 1
    controlSensors.append([i, 'simulateInglenookSensor', 'Simulate Inglenook System', 10, 5]); i += 1
    controlSensors.append([i, 'simulateErrorsInglenookSensor', 'Simulate With Errors', 10, 5]); i += 1
    controlSensors.append([i, 'simulateDistributionInglenookSensor', 'Simulate From Mainline', 10, 5]); i += 1
    controlSensors.append([i, 'runRealTrainNoDistributionInglenookSensor', 'Run Real Train From Siding', 10, 5]); i += 1
    controlSensors.append([i, 'runRealTrainDistributionInglenookSensor', 'Run Real Train from Mainline', 10, 5]); i += 1
    controlSensors.append([i, 'soundInglenookSensor', 'Enable Inglenook Announcements', 0, 5]); i += 1
    controlSensors.append([i, 'bellInglenookSensor', 'Enable Inglenook Bell', 0, 5]); i += 1
    controlSensors.append([i, 'showTrucksOnPanelInglenookSensor', 'Show Trucks On inglenook Panel', 0, 5]); i += 1
    controlSensors.append([i, 'ShowTrucksOnMimicInglenookSensor', 'Show Trucks On inglenook Mimic', 0, 5]); i += 1

    i = 1
    otherSensors = []
    otherSensors.append([i, "stopThreadSensor"])

    def __init__(self):
        self.define_DisplayProgress_global()

        if self.perform_initial_checks:
            self.show_progress(10)
            self.removeIconsAndLabels()
            self.show_progress(20)
            self.removeLogix()
            self.removeSensors()
            self.show_progress(30)
            self.get_list_of_inglenook_sidings()
            self.show_progress(50)
            self.addSensors()
            self.show_progress(60)
            self.addLogix()    #allows the system to start up
            # self.addLogixNG()
            self.show_progress(70)
            self.addIcons()
            self.setVersionNo()
            self.end_show_progress()
            msg = 'The JMRI tables and panels have been updated to support the Inglenook Siding System\nA store is recommended.'
            JOptionPane.showMessageDialog(None, msg, 'Message', JOptionPane.WARNING_MESSAGE)

    def setVersionNo(self):
        memory = memories.provideMemory('IS:ISMEM:' + "versionNo")
        if memory is not None:
            memory.setValue(self.version_no)

    def define_DisplayProgress_global(self):
        global dpg
        dpg = DisplayProgress()

    def show_progress(self, progress):
        global dpg
        dpg.Update("creating icons: " + str(progress)+ "% complete")

    def end_show_progress(self):
        global dpg
        dpg.killLabel()

    # **************************************************
    # perform initial checks
    # **************************************************

    @property
    def perform_initial_checks(self):

        sensors_OK = False
        block_sensors_OK = False
        stops_OK = False
        lengths_OK = False



        #JOptionPane.showMessageDialog(None, "Performing some preliminary checks to ensure the trains run correctly\nAll errors will need to be fixed for Dispatcher to run correctly\nSome errors will cause the panel to be set up incorrectly in this stage", 'Checks', JOptionPane.WARNING_MESSAGE)

        # check all blocks have sensors
        if self.check_all_stop_sensors_are_set_up() == False:
            self.msg = self.msg + "\n***********************\n Do you wish to continue\n***********************"
            myAnswer = JOptionPane.showConfirmDialog(None, self.msg)
            if myAnswer == JOptionPane.YES_OPTION:
                #JOptionPane.showMessageDialog(None, 'OK continuing', "As you wish", JOptionPane.WARNING_MESSAGE)
                pass
            elif myAnswer == JOptionPane.NO_OPTION:
                msg = 'Stopping'
                JOptionPane.showMessageDialog(None, 'Stopping', "Fix Error" , JOptionPane.WARNING_MESSAGE)
                return False
            elif myAnswer == JOptionPane.CANCEL_OPTION:
                msg = 'Stopping'
                JOptionPane.showMessageDialog(None, 'Stopping', "Have a cup of Tea", JOptionPane.WARNING_MESSAGE)
                return False
            elif myAnswer == JOptionPane.CLOSED_OPTION:
                if self.logLevel > 0: print( "You closed the window. How rude!")
        else:
            sensors_OK = True


        if self.check_truck_indicators_are_set_up() == False:
            self.msg1 = self.msg1 + "\n***********************\n Do you wish to continue\n***********************"
            myAnswer = JOptionPane.showConfirmDialog(None, self.msg1)
            if self.logLevel > 0: print(1)
            if myAnswer == JOptionPane.YES_OPTION:
                #JOptionPane.showMessageDialog(None, 'OK continuing', "As you wish", JOptionPane.WARNING_MESSAGE)
                pass
            elif myAnswer == JOptionPane.NO_OPTION:
                msg = 'Stopping'
                JOptionPane.showMessageDialog(None, 'Stopping', "You need a cup of Tea" , JOptionPane.WARNING_MESSAGE)
                return False
            elif myAnswer == JOptionPane.CANCEL_OPTION:
                msg = 'Stopping'
                JOptionPane.showMessageDialog(None, 'Stopping', "Have a cup of Tea", JOptionPane.WARNING_MESSAGE)
                return False
            elif myAnswer == JOptionPane.CLOSED_OPTION:
                if self.logLevel > 0: print ("You closed the window. How rude!")
        else:

            if self.logLevel > 0: print(2)
            block_sensors_OK  = True

        msg =  ""
        some_checks_OK = False
        if sensors_OK:
            msg = msg + "all_stop_sensors_are_set_up\n"
            some_checks_OK = True
        if block_sensors_OK:
            msg = msg + "all truck_indicators_are_set_up\n"
            some_checks_OK = True
        if some_checks_OK:
            msg = "Performed some preliminary checks to ensure the trains run correctly\n\nAll Checks OK"
            reply = Query().customQuestionMessage2(msg, "Checks", "Continue", "Look in more detail")
            if Query().CLOSED_OPTION == True:
                return False
            # print "reply=", reply
            if reply == JOptionPane.NO_OPTION:
                if sensors_OK:
                    Message = "All blocks have sensors"
                    JOptionPane.showMessageDialog(None, Message, 'Message', JOptionPane.INFORMATION_MESSAGE)
                if block_sensors_OK:
                    Message = "no two blocks have the same sensor\nPassed check OK"
                    JOptionPane.showMessageDialog(None, Message, 'Message', JOptionPane.INFORMATION_MESSAGE)
                # if stops_OK:
                #     Message = "The following blocks have been specified as stopping points\n" + self.msg2 + "\n there are sufficient blocks set up"
                #     JOptionPane.showMessageDialog(None, Message, 'Message', JOptionPane.INFORMATION_MESSAGE)
                # if lengths_OK:
                #     Message = "All blocks have lengths\n OK to continue \nNote that trains should also be set up with a speed profile to stop correctly"
                #     JOptionPane.showMessageDialog(None, Message, 'Message', JOptionPane.INFORMATION_MESSAGE)

        return True

    def check_all_stop_sensors_are_set_up(self):
        LayoutBlockManager=jmri.InstanceManager.getDefault(jmri.jmrit.display.layoutEditor.LayoutBlockManager)
        list_of_errors = []
        success = True



        return success

    def check_truck_indicators_are_set_up(self):
        LayoutBlockManager=jmri.InstanceManager.getDefault(jmri.jmrit.display.layoutEditor.LayoutBlockManager)
        dict = {}
        success = True
        # for block in blocks.getNamedBeanSet():
        #     if LayoutBlockManager.getLayoutBlock(block) != None:    #only include blocks included in a layout panel
        #         if block.getUserName() != None:                     #all layout blocks have usernames, should not need this check
        #             block_name = block.getUserName()
        #         else:
        #             block_name = block.getSystemName()
        #         sensor = block.getSensor()
        #         if sensor != None:
        #             if sensor.getUserName() != None:
        #                 sensor_name = sensor.getUserName()
        #             else:
        #                 sensor_name = sensor.getSystemName()
        #             dict[block_name] = sensor_name
        #
        # list_of_errors = self.get_duplicate_values_in_dict(dict)
        # if self.logLevel > 0: print list_of_errors
        # if list_of_errors == []:
        #     success = True
        # else:
        #     success = False
        # self.msg1 = ""
        # for message in list_of_errors:
        #     self.msg1 = self.msg1 +"\n" + message

        return success


    def get_duplicate_values_in_dict(self, dict):

        # finding duplicate values
        # from dictionary
        # using a naive approach
        rev_dict = {}

        for key, value in dict.items():
            rev_dict.setdefault(value, set()).add(key)

        result = ["blocks " +', '.join(values) + " have the same sensor " + str( key) for key, values in rev_dict.items()
                                      if len(values) > 1]
        return result

    def check_sufficient_number_of_blocks(self):
        LayoutBlockManager=jmri.InstanceManager.getDefault(jmri.jmrit.display.layoutEditor.LayoutBlockManager)
        list_of_stops = []
        list_of_blocks = []
        for block in blocks.getNamedBeanSet():
            if LayoutBlockManager.getLayoutBlock(block) != None:    #only include blocks included in a layout panel
                if block.getUserName() != None:                     #all layout blocks have usernames, should not need this check
                    block_name = block.getUserName()
                else:
                    block_name = block.getSystemName()
                comment = str(block.getComment())
                if comment !=None:
                    if "stop" in comment.lower():
                        list_of_stops.append("block " + block_name + " has a stop")
                        if self.logLevel > 0: print list_of_stops
                    else:
                        list_of_blocks.append("block " + block_name + " has no stop")
                        if self.logLevel > 0: print list_of_blocks
                else:
                    list_of_blocks.append("block " + block_name + " has no stop")
        #countthe number of blocks in dictionary
        no_stops = len(list_of_stops)
        if self.logLevel > 0: print "no_stops", no_stops
        no_blocks = len(list_of_blocks)
        if self.logLevel > 0: print "no blocks", no_blocks
        if no_stops < 2:
            success = False
        else:
            success = True
        self.msg2 = " - "
        self.msg2 = self.msg2 + '\n - '.join(list_of_stops)
        if self.logLevel > 0: print self.msg2
        self.msg3 = ""
        self.msg3 = '\n - '.join(list_of_blocks)
        if self.logLevel > 0: print self.msg3
        if no_stops == 0:
            self.msg2 = " - there are no stops"
        return success

    def check_all_blocks_have_lengths(self):
        LayoutBlockManager=jmri.InstanceManager.getDefault(jmri.jmrit.display.layoutEditor.LayoutBlockManager)
        list_of_errors = []
        success = True
        for block in blocks.getNamedBeanSet():
            if LayoutBlockManager.getLayoutBlock(block) != None:     #only include blocks included in a layout panel
                if block.getLengthMm() < 0.01:
                    if block.getUserName() != None:                 #all layout blocks have usernames, should not need this check
                        msg = "block {} does not have a length".format(block.getUserName())
                    else:
                        msg = "block {} does not have a length".format(block.getSystemName())
                        msg = msg + "\nblock {} does not have a username".format(block.getSystemName())
                    list_of_errors.append(msg)
                    success = False
        self.msg5 = " - "
        self.msg5 = self.msg5 + '\n - '.join(list_of_errors)

        return success

    # **************************************************
    # remove icons and labels from panels
    # **************************************************
    def removeIconsAndLabels(self):
        i = 1
        for panel in self.editorManager.getAll(jmri.jmrit.display.layoutEditor.LayoutEditor):
            if panel.getTitle() == 'Inglenook System':
                print i, "panel:" , panel.getTitle()
        print "end"
        i = 1
        for panel in self.editorManager.getAll(jmri.jmrit.display.layoutEditor.LayoutEditor):
            print i, "panel:" , panel.getTitle()
            if panel.getTitle() == 'Inglenook System':
                if self.version_number_changed():
                    print "removing panel, version number changed"
                    self.editorManager.remove(panel)
                    # panel.deletePanel()
                    panel.dispose()
                    msg = "should have removed panel"
                    Query().displayMessage(msg,"")
                # Skip the Dispatcher System control panel if it exists
                continue

            # self.removeBlockContentIcons(panel)
            self.removeLabels(panel)
            self.removeSensorIcons(panel)


    def removeBlockContentIcons(self, panel):
        deleteList = []     # Prevent concurrent modification
        icons = panel.getBlockContentsLabelList()
        for icon in icons:
            blk = icon.getBlock()
            if blk is not None:
                deleteList.append(icon)

        for item in deleteList:
            panel.removeFromContents(item)

    def removeLabels(self, panel):
        labelText = []
        for control in self.controlSensors:
            labelText.append(control[2])

        deleteList = []     # Prevent concurrent modification
        for label in panel.getLabelImageList():
            if label.isText():
                if label.getText() in labelText:
                    deleteList.append(label)

        for item in deleteList:
            panel.removeFromContents(item)

    def removeSensorIcons(self, panel):
        # blockSensors = []
        # for block in blocks.getNamedBeanSet():
        #     sensor = block.getSensor()
        #     if sensor is not None:
        #         blockSensors.append(sensor)

        deleteList = []     # Prevent concurrent modification
        icons = panel.getSensorList()
        for icon in icons:
            sensor = icon.getSensor()
            if sensor is not None:
                name = sensor.getDisplayName()
                if 'TruckIcon' in name:
                    # dispatcher system sensors
                    deleteList.append(icon)
                # else:
                #     # block sensors
                #     if sensor in blockSensors:
                #         deleteList.append(icon)
                comment = sensor.getComment()
                if comment is not None:
                    if '#IS_siding' in comment or '#IS_headshunt' in comment:
                        deleteList.append(icon)

        for item in deleteList:
            panel.removeFromContents(item)

    # **************************************************
    # remove Logix
    # **************************************************
    def removeLogix(self):
        logixManager = jmri.InstanceManager.getDefault(jmri.LogixManager)
        logix = logixManager.getLogix('Run Inglenook')
        cdlManager = jmri.InstanceManager.getDefault(jmri.ConditionalManager)
        cdl = cdlManager.getConditional(logix, 'Run Inglenook')
        if logix is not None:
            logixManager.deleteLogix(logix)

        if cdl is not None:
            cdlManager.deleteConditional(cdl)

    # **************************************************
    # remove sensors
    # **************************************************
    def removeSensors(self):
        controlName = []
        # if self.editorManager.get("Inglenook System") is None:
        if self.version_number_changed():
            # OK to delete control sensors
            for control in self.controlSensors:
                controlName.append(control[1])

            for other in self.otherSensors:
                controlName.append(other[1])

        deleteList = []     # Prevent concurrent modification
        for sensor in sensors.getNamedBeanSet():
            userName = sensor.getUserName()
            comment = sensor.getComment()
            if userName is not None:
                if 'TruckIndication' in userName or 'Decoupling' in userName:
                    deleteList.append(sensor)
                elif userName in controlName:
                    deleteList.append(sensor)
            # if comment is not None:
            #     if '#IS_siding' in comment or '#IS_spur' in comment:
            #         deleteList.append(sensor)

        for item in deleteList:
            if self.logLevel > 0: print 'remove sensor {}'.format(item.getDisplayName())

            sensors.deleteBean(item, 'DoDelete')

    def version_number_changed(self):
        memory = memories.getMemory('IMIS:ISMEM:' + "versionNo")
        print "memory", memory, type(memory)
        if memory is None:
            print "version_no changed", "memory:", "version", self.version_no
            return True
        elif memory.getValue() != self.version_no:
            print "version_no changed", "memory:", memory.getValue(), "version", self.version_no
            return True
        else:
            print "version_no not changed", "memory:", memory.getValue(), "version", self.version_no
            return False

    # ***********************************************************
    # gets the list of stopping points (stations, sidings etc.)
    # ***********************************************************
    # def get_list_of_stopping_points(self):
    #     for block in blocks.getNamedBeanSet():
    #         comment = block.getComment()
    #         if comment != None:
    #             if "stop" in comment.lower():
    #                 self.list_of_stopping_points.append(block.getUserName())

    def get_list_of_inglenook_sidings(self):
        for block in blocks.getNamedBeanSet():
            comment = block.getComment()
            if comment != None:
                if "#IS_block_" in comment:
                    blockname = block.getUserName()
                    if "#IS_block_siding1#" in comment:
                        self.add_truck_blocks(blockname, 6, "1")
                    elif "#IS_block_siding2#" in comment:
                        self.add_truck_blocks(blockname, 6, "2")
                    elif "#IS_block_siding3#" in comment:
                        self.add_truck_blocks(blockname, 8, "3")
                    # elif "#IS_block_mid#" in comment:
                    #     self.add_truck_blocks(blockname, 3, "mid")
                    elif "#IS_block_headshunt#" in comment:
                        self.add_truck_blocks(blockname, 4, "headshunt")
                    else:
                        pass
                    #self.list_of_inglenook_sidings.append(block.getUserName())
        if self.list_of_inglenook_sidings == None:
            if self.logLevel > 0: print "sidings have not been set up (None)"
            return

        if len(self.list_of_inglenook_sidings) == 0:
            if self.logLevel > 0: print "sidings have not been set up"
            return
            #need a messagebox here
        if self.logLevel > 0: print "sidings have been set up", self.list_of_inglenook_sidings

    def add_truck_blocks(self, block_name, number_blocks, siding_name):

        self.list_of_inglenook_sidings.append([block_name, number_blocks, siding_name] )

    # **************************************************
    # add sensors
    # **************************************************
    def addSensors(self):
        # Create the control sensors
        for control in self.controlSensors:
            sensor = sensors.provideSensor('IS:ISCT:' + str(control[0]))
            if sensor is not None:
                sensor.setUserName(control[1])

        for other in self.otherSensors:
            sensor = sensors.provideSensor('IS:ISOS:' + str(other[0]))
            if sensor is not None:
                sensor.setUserName(other[1])

        # Create the truck sensors
        siding_index = 0
        block_index = 0
        for stop in self.list_of_inglenook_sidings:
            siding_index += 1
            [block_name, number_blocks, siding_name] = stop
            block = blocks.getBlock(block_name)
            if block is not None:
                for i in range(number_blocks):
                    block_index += 1
                    sensor_name = siding_name + "_" + str(i)
                    ingsiding = sensors.provideSensor('IS:ISTI:' + str(block_index))  #truck indication sensor
                    if ingsiding is not None:
                        ingsiding.setUserName('TruckIndication_' + sensor_name)
                    # if i == 1:    # only need 1 decoupling sensor per siding
                    #     inproc = sensors.provideSensor('IS:ISDS:' + str(siding_index))   #decoupling sensor
                    #     if inproc is not None:
                    #          inproc.setUserName('Decoupling_' + str(siding_name))

    # **************************************************
    # generate SML
    # **************************************************
    def generateSML(self):
        layoutblocks.enableAdvancedRouting(True)
        smlManager = jmri.InstanceManager.getDefault(jmri.SignalMastLogicManager)
        smlManager.automaticallyDiscoverSignallingPairs()

    # **************************************************
    # generate sections
    # **************************************************
    def generateSections(self):
        smlManager = jmri.InstanceManager.getDefault(jmri.SignalMastLogicManager)
        smlManager.generateSection()
        sections.generateBlockSections()

    # **************************************************
    # add Logix
    # **************************************************
    def addLogix(self):
        lgxManager = jmri.InstanceManager.getDefault(jmri.LogixManager)
        cdlManager = jmri.InstanceManager.getDefault(jmri.ConditionalManager)
        lgx = lgxManager.createNewLogix('IX:ISLX:1', 'Run Inglenook')
        cdl = cdlManager.createNewConditional('IX:ISLX:1C2', 'Run Inglenook')
        if cdl is not None:
            if self.logLevel > 0: print "cnd is not none"
            cdl.setUserName('Run Inglenook')
            vars = []
            vars.append(jmri.ConditionalVariable(False, jmri.Conditional.Operator.AND, jmri.Conditional.Type.SENSOR_ACTIVE, 'startInglenookSensor', True))
            cdl.setStateVariables(vars)
            actions = []
            actions.append(jmri.implementation.DefaultConditionalAction(1, jmri.Conditional.Action.RUN_SCRIPT, '', -1, 'program:jython/ShuntingPuzzles/Inglenook/RunInglenook.py'))
            cdl.setAction(actions)

        lgx.addConditional('IX:ISLX:1C2', 0)
        lgx.activateLogix()

    def addLogixNG(self):
        lgxNGManager = jmri.InstanceManager.getDefault(jmri.jmrit.logixng.LogixNG_Manager)
        cdlNGManager = jmri.InstanceManager.getDefault(jmri.jmrit.logixng.ConditionalNG_Manager)
        lgx = lgxNGManager.createLogixNG('IQ$IS:01', 'Set Inglenook Sensors')
        cdl = cdlNGManager.createConditionalNG(lgx,'IQC$IS:01', 'Set Inglenook Sensors')


    # **************************************************
    # add Icons
    # **************************************************
    def addIcons(self):
        if self.logLevel > 0: print "in addIcons"
        self.addControlIconsAndLabels(panel)
        if self.logLevel > 0: print "added control icons"
        # self.getSidingBlockCenterPoints(panel)
        # print "added SidingBlockCenterPoints"
        self.direction = self.checkOrientationOfPuzzle(panel)
        if self.logLevel > 0: print "added checkOrientationOfPuzzle", self.direction
        if self.direction != None:
            if self.logLevel > 0: print "***************direction", self.direction
            self.addTruckIcons(panel)
        else:
            print "error"

    def checkOrientationOfPuzzle(self, panel):
        LayoutBlockManager=jmri.InstanceManager.getDefault(jmri.jmrit.display.layoutEditor.LayoutBlockManager)
        for block in blocks.getNamedBeanSet():
            if LayoutBlockManager.getLayoutBlock(block) != None:    #only include blocks included in a layout panel
                if block.getComment() != None:
                    if "#IS_block_siding1" in block.getComment():  # check the first siding which has a buffer
                        layoutblock = LayoutBlockManager.getLayoutBlock(block)
                        no_neighbours = layoutblock.getNumberOfNeighbours()
                        if no_neighbours == 1:  #there should only be one neighbour at ingsiding1
                            neighbor = layoutblock.getNeighbourAtIndex(0)
                            if self.logLevel > 0: print neighbor.getDisplayName()
                            direction =layoutblock.getNeighbourDirection(neighbor)
                            if self.logLevel > 0: print direction
                            return "direction", direction
                        else:
                            print "Error"
                            return None
        return None

    # def getSidingBlockCenterPoints(self, panel):
    #     self.blockPoints.clear()
    #     for tsv in panel.getTrackSegmentViews():
    #         blk = tsv.getBlockName()
    #
    #         pt1 = panel.getCoords(tsv.getConnect1(), tsv.getType1())
    #         pt2 = panel.getCoords(tsv.getConnect2(), tsv.getType2())
    #
    #         mid = jmri.util.MathUtil.midPoint(pt1, pt2)
    #
    #         self.updateCoords(blk, mid)
    #
    #     for tov in panel.getLayoutTurnoutAndSlipViews():
    #         blkA = tov.getBlockName()
    #         blkB = tov.getBlockBName()
    #         blkC = tov.getBlockCName()
    #         blkD = tov.getBlockDName()
    #
    #         xyA = tov.getCoordsA()
    #         xyB = tov.getCoordsB()
    #         xyC = tov.getCoordsC()
    #         xyD = tov.getCoordsD()
    #
    #         self.updateCoords(blkA, xyA)
    #         self.updateCoords(blkB, xyB)
    #         self.updateCoords(blkC, xyC)
    #         self.updateCoords(blkD, xyD)
    #
    #     for lxv in panel.getLevelXingViews():
    #         blkAC = lxv.getBlockNameAC()
    #         blkBD = lxv.getBlockNameBD()
    #
    #         # A level crossing has 4 points but only two blocks.  To prevent both points being in the
    #         # middle, use the A and D points.
    #         xyA = lxv.getCoordsA()
    #         xyD = lxv.getCoordsD()
    #
    #         self.updateCoords(blkAC, xyA)
    #         self.updateCoords(blkBD, xyD)

    def updateCoords(self, blk, xy):
        if blk is not None:
            if blk in self.blockPoints:
                self.blockPoints[blk] = jmri.util.MathUtil.midPoint(self.blockPoints[blk], xy)
            else:
                self.blockPoints[blk] = xy

    # **************************************************
    # stop icons
    # **************************************************
    def addTruckIcons(self, panel):
        if self.direction == 64:      #self,direction is direction of siding 1
            direction = "east"
        else:
            direction = "west"  # 128
        if self.logLevel > 0: print "direction", direction
        for [blockName, number_blocks, siding_name] in self.list_of_inglenook_sidings:
            if self.logLevel > 0: print [blockName, number_blocks, siding_name]
            if blockName in self.blockPoints.keys():
                x = self.blockPoints[blockName].getX()
                y = self.blockPoints[blockName].getY()
                if self.logLevel > 0: print "adding truck icons"
                #Truck Icons
                for i in range(number_blocks):
                    sensor_name = siding_name + "_" + str(i)
                    direction1 = direction
                    if siding_name == "spur":
                        if direction == "east":
                            direction1 = "west"
                        else:
                            direction1 = "east"
                    spacing = 40
                    if direction1 == "west":
                        beginning = (-spacing * number_blocks)/2
                        offset = spacing * i
                    else:
                        beginning = (spacing * number_blocks)/2 - spacing
                        offset = -spacing * i
                    offset = beginning + offset
                    if self.logLevel > 0: print "sensor_name", 'TruckIndication_' + sensor_name
                    mtSensor = sensors.getSensor('TruckIndication_' + sensor_name )
                    if mtSensor is not None:
                        if self.logLevel > 0: print "add", mtSensor.getUserName(), x, y
                        if siding_name.isdigit():
                            textno = str(i)
                        else:
                            textno = str(i)
                        self.addMarkerIcon(panel, mtSensor, blockName, x+offset, y-30, textno)

                    # mpSensor = sensors.getSensor('Decoupling_' + siding_name)
                    sensor_name = "siding"+ siding_name if siding_name != "spur" else "spur"
                    siding = "#IS_"+sensor_name+"_sensor#"
                    if self.logLevel > 0: print "*****************siding", siding, "siding_name", siding_name
                    mpSensor = self.get_decoupling_sensor(siding)
                    if mpSensor is not None:
                        if i == number_blocks-4:
                            # print "add", mpSensor.getUserName(), x, y
                            if self.logLevel > 0: print "direction1", direction1
                            if direction1 == "west":
                                # if siding_name != 'sensor_spur':
                                self.addSmallIcon(panel, mpSensor.getDisplayName(), x + offset  + 0.8*spacing , y-18)
                                # else:
                                #     self.addSmallIcon(panel, mpSensor.getDisplayName(), x + offset  + spacing/4 , y-18)
                            else:
                                # self.addSmallIcon(panel, mpSensor.getDisplayName(), x + offset/2 , y-20)
                                # self.addSmallIcon(panel, mpSensor.getDisplayName(), x , y-20)
                                self.addSmallIcon(panel, mpSensor.getDisplayName(), x + offset - 0.2*spacing , y-18)

    def get_decoupling_sensor(self, sensor_comment):
        for sensor in sensors.getNamedBeanSet():
            comment = sensor.getComment()
            if comment != None:
                if sensor_comment in comment:
                    return sensor
        return None

    # **************************************************
    # occupancy sensor icons and block content labels
    # **************************************************
    def addOccupancyIconsAndLabels(self, panel):
        for blockName in self.blockPoints.keys():
            x = self.blockPoints[blockName].getX() - 10
            y = self.blockPoints[blockName].getY() + 10
            block = blocks.getBlock(blockName)
            if block is not None:
                sensor = block.getSensor()
                if sensor is not None:
                    self.addSmallIcon(panel, sensor.getDisplayName(), x, y)

                    y = int(y) - 40 if int(y) > 45 else 5
                    self.addBlockContentLabel(panel, block, x, y)

    # **************************************************
    # control sensor icons and label
    # **************************************************
    def addControlIconsAndLabels(self, panel):
        # if self.editorManager.get("Inglenook System") is not None:
        #     return
        if not self.version_number_changed():
            if self.logLevel > 0: print "not adding control Icons and labels"
            return

        if self.logLevel > 0: print "adding control Icons and labels"
        # Create the Dispatcher System control panel
        panel = jmri.jmrit.display.layoutEditor.LayoutEditor("Inglenook System")
        self.editorManager.add(panel)

        for control in self.controlSensors:
            sensor = sensors.getSensor('IS:ISCT:' + str(control[0]))
            if sensor is not None:
                x = 20 + control[3]
                y = (control[0] * 20) + 20 + control[4]
                self.addMediumIcon(panel, sensor, x, y)

                x += 20
                self.addTextLabel(panel, control[2], x, y)

        panel.setSize(300, 400)
        panel.setAllEditable(False)
        panel.setVisible(True)

    # **************************************************
    # small icon
    # **************************************************
    def addSmallIcon(self, panel, sensorName, x, y):
        icn = jmri.jmrit.display.SensorIcon(panel)
        icn.setIcon("SensorStateActive", jmri.jmrit.catalog.NamedIcon("resources/icons/smallschematics/tracksegments/circuit-occupied.gif", "active"));
        icn.setIcon("SensorStateInactive", jmri.jmrit.catalog.NamedIcon("resources/icons/smallschematics/tracksegments/circuit-empty.gif", "inactive"));
        icn.setIcon("BeanStateInconsistent", jmri.jmrit.catalog.NamedIcon("resources/icons/smallschematics/tracksegments/circuit-error.gif", "incons"));
        icn.setIcon("BeanStateUnknown", jmri.jmrit.catalog.NamedIcon("resources/icons/smallschematics/tracksegments/circuit-error.gif", "unknown"));

        # Assign the sensor and set the location
        icn.setSensor(sensorName)
        icn.setLocation(int(x), int(y))

        # Add the icon to the layout editor panel
        panel.putSensor(icn)

    # **************************************************
    # medium icon
    # **************************************************
    def addMediumIcon(self, panel, sensor, x, y):
        icn = jmri.jmrit.display.SensorIcon(panel)
        icn.setIcon("SensorStateActive", jmri.jmrit.catalog.NamedIcon("resources/icons/mediumschematics/LEDs/AMBERLED.gif", "active"));
        icn.setIcon("SensorStateInactive", jmri.jmrit.catalog.NamedIcon("resources/icons/mediumschematics/LEDs/GRAYLED.gif", "inactive"));
        icn.setIcon("BeanStateInconsistent", jmri.jmrit.catalog.NamedIcon("resources/icons/mediumschematics/LEDs/REDLED.gif", "incons"));
        icn.setIcon("BeanStateUnknown", jmri.jmrit.catalog.NamedIcon("resources/icons/mediumschematics/LEDs/REDLED.gif", "unknown"));

        # Assign the sensor and set the location
        icn.setSensor(sensor.getDisplayName())
        icn.setLocation(int(x), int(y))

        # Add the icon to the layout editor panel
        panel.putSensor(icn)

    # **************************************************
    # marker icon
    # **************************************************
    def addMarkerIcon(self, panel, sensor, blockName, x, y, No):
        if self.logLevel > 0: print "addmarkericon"
        icn = jmri.jmrit.display.SensorIcon(panel)
        truck_icon = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/icons/truck6.gif')
        engine_icon = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/icons/engine1.gif')
        null_icon = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/icons/null.gif')
        if No == "1":
            truck_icon = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/icons/truckred.gif')
        # icn.setIcon("SensorStateActive", jmri.jmrit.catalog.NamedIcon("resources/icons/markers/loco-green.gif", "active"))
        icn.setIcon("SensorStateInactive", jmri.jmrit.catalog.NamedIcon("resources/icons/throttles/RoundRedCircle20.png", "inactive"))
        # icn.setIcon("SensorStateInactive", jmri.jmrit.catalog.NamedIcon(null_icon, "inactive"))
        # icn.setIcon("BeanStateInconsistent", jmri.jmrit.catalog.NamedIcon("resources/icons/markers/loco-yellow.gif", "incons"));
        # icn.setIcon("BeanStateUnknown", jmri.jmrit.catalog.NamedIcon("resources/icons/markers/loco-gray.gif", "unknown"))
        icn.setIcon("SensorStateActive", jmri.jmrit.catalog.NamedIcon(truck_icon, "active"))
        icn.setIcon("SensorStateInactive", jmri.jmrit.catalog.NamedIcon(null_icon, "inactive"))
        icn.setIcon("BeanStateInconsistent", jmri.jmrit.catalog.NamedIcon(engine_icon, "inconsistent"))
        icn.setIcon("BeanStateUnknown", jmri.jmrit.catalog.NamedIcon(null_icon, "unknown"))
        if No == "1":
            truck_icon = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/icons/truckred.gif')

        #icn.setText(blockName[:9])
        icn.setText(No)
        icn.setActiveText(No)
        icn.setInactiveText(No)
        icn.setInconsistentText(No)
        icn.setUnknownText(No)
        if self.logLevel > 0: print "text", icn.getText()
        icn.setTextActive(Color.WHITE)
        icn.setTextInActive(Color.YELLOW)
        icn.setTextInconsistent(Color.WHITE)
        # t = java.awt.Color()
        # transparent = Color(#FF000000)
        transparent = Color.WHITE
        alpha = 0
        transparent = Color(
            transparent.getRed(),
            transparent.getGreen(),
            transparent.getBlue(),
            alpha);
        icn.setTextInconsistent(Color.WHITE)  #should be transparent
        #icn.setTextInconsistent(Color.YELLOW)
        icn.setTextUnknown(Color.WHITE)

        # Assign the sensor and set the location
        icn.setSensor(sensor.getDisplayName())
        icn.setLocation(int(x), int(y))

        # Add the icon to the layout editor panel
        if self.logLevel > 0: print "putting sensor"
        panel.putSensor(icn)

    # **************************************************
    # text label
    # **************************************************
    def addTextLabel(self, panel, text, x, y):
        label = jmri.jmrit.display.PositionableLabel(text, panel)
        label.setLocation(int(x), int(y))
        label.setSize(label.getPreferredSize().width, label.getPreferredSize().height);
        label.setDisplayLevel(4)
        panel.putItem(label)

    # **************************************************
    # block content label
    # **************************************************
    def addBlockContentLabel(self, panel, block, x, y):
        label = jmri.jmrit.display.BlockContentsIcon(block.getDisplayName(), panel)
        label.setBlock(block.getDisplayName())
        label.setLocation(int(x), int(y))
        panel.putItem(label)

class DisplayProgress:
    def __init__(self):
        #labels don't seem to work. This is the only thing I could get to work. Improvements welcome
        self.frame1 = JFrame('Hello, World!', defaultCloseOperation=JFrame.DISPOSE_ON_CLOSE, size=(500, 50), locationRelativeTo=None)

        self.frame1.setVisible(True)

    def Update(self,msg):
        self.frame1.setTitle(msg)

    def killLabel(self):
        self.frame1.setVisible(False)
        self.frame1 = None


class Query:

    CLOSED_OPTION = False
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

    def displayMessage(self, msg, title = "", display = True):
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