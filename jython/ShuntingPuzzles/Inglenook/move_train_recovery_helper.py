#@add_methods(r2.storeSensorFrom, r2.storeSensorTo, r2.storeSensor, r2.storeFunction, r2.storeCount, r2.storeTimeout)
import java
import jmri
from timeout import alternativeaction, variableTimeout, print_name, timeout

# def storeSensorFrom(self, sensor):
#     self.sensor_from_stored = sensor
#     #self.sensor_from_name = "sensor_from_stored" #this is done at declaration time
#
# def storeSensorTo(self, sensor):
#     self.sensor_to_stored = sensor
#     #self.sensor_to_name = "sensor_to_stored" #this is done at declaration time
#
# def storeSensor(self, sensor):
#     self.sensor_stored = sensor
#     #self.sensor_name = "sensor_stored"    #this is done at declaration time
#
# def storeFunction(self, function):
#     self.function_stored = function
#     #self.function_name = "function_stored"    #this is done at declaration time
#
# def storeCount(self, count):
#     self.count_stored = count
#     #self.count_name = "count_stored"    #this is done at declaration time
#
# def storeTimeout(self, timeout):
#     self.timeout_stored = timeout
#     #self.timeout_name = "timeout_stored"    #this is done at declaration time