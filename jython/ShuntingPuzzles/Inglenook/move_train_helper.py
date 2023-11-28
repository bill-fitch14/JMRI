#@add_methods(h.setPointsAndDirection, h.setBranch, h.setSensor)
#@add_methods(h.couple1, h.uncouple1, h.uncouple2)
#@add_methods(h.swapRouteSameDirectionTravelling,h.swapRouteOppDirectionTravelling,h.sensorName,h.stateName)
#@add_methods(h.noTrucksOnBranches, h.noTrucksOnBranch, h.moveDistance)
import java
import jmri
from timeout import alternativeaction, variableTimeout, print_name, timeout

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
#
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
#
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
#
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
#
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
#     #whiz back
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
#
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
#
#
# #@print_name()
# def noTrucksOnBranches(self, pegs):
#     noTrucksList = [len(x) for x in pegs]
#     return noTrucksList
#
# #@print_name()
# def noTrucksOnBranch(self, pegs, branch):
#     NoTrucks = len(pegs[branch - 1])
#     return NoTrucks
#
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
#
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
#
# # Define routine to map status numbers to text
# #@print_name()
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