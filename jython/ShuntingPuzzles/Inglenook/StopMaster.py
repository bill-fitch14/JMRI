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