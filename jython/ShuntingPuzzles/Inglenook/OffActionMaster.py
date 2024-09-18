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
            help_sensor = sensors.getSensor("InglenookHelpSensor")
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
            elif sensor_that_went_inactive == help_sensor:
                self.sensor_to_look_for = help_sensor
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
        self.run_stop_sensors = [sensors.getSensor(sensorName) for sensorName in ["startInglenookSensor", "InglenookHelpSensor"]]