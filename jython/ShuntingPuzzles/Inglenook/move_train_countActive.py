# import java
# import jmri
#
# from timeout import alternativeaction, variableTimeout, print_name, timeout

# @print_name()
# def moveToBranch_old(self, noTrucksOnTrain, noTrucksToMove, fromBranch, destBranch):
#     self.indent()
#     # move from siding to spur or vice-versa
#     if destBranch != self.spur_branch:
#         direction = self.setPointsAndDirection(self.spur_branch,destBranch)
#         self.set_delay_if_not_simulation(5000)
#
#         sensor = self.setSensor(self.spur_branch)
#         self.countTrucksInactive(noTrucksOnTrain, sensor, direction, fromBranch, destBranch)  # leave the moving to the next movement
#
#         sensor = self.setSensor(destBranch)
#         #$$$$$$$$$$$$$$$$$$$$$$$$$$ change this $$$$$$$$$$$$$$$$$$$$$$$ to noTrucksTo Move 1, countTrucksActive
#         # this should not move amy trucks in simulate, same as this
#         noTrucksToMove1 = 1          # this works for simulation but not for real
#         self.countTrucksActive(noTrucksToMove1, sensor, direction, fromBranch, destBranch)  # leave the moving to the next movement
#     else:
#         anyBranch = 1  # choose any branch, the direction is the same
#         direction = self.setDirection(anyBranch,self.spur_branch)   # don't need to set points as in siding
#         sensor = self.setSensor(destBranch)        # spur branch
#         self.countTrucksInactive(self.noTrucksOnTrain, sensor, direction, fromBranch, destBranch)  #counting all trucks on train
#         self.setSpeed(self.stop)
#     self.dedent()

@print_name()
# def moveToBranch(self, noTrucksOnTrain, noTrucksToMove, fromBranch, destBranch):
#     self.indent()
#     # move from siding to spur or vice-versa
#     if destBranch != self.spur_branch:
#         direction = self.setPointsAndDirection(fromBranch, destBranch)
#         self.set_delay_if_not_simulation(5000)
#
#         sensor = self.setSensor(fromBranch)     # spur branch
#         self.countTrucksInactive(noTrucksOnTrain, sensor, direction, fromBranch, destBranch)  # leave the moving to the next movement
#
#         sensor = self.setSensor(destBranch)     # a siding branch
#         noTrucksToMove1 = 1
#         self.countTrucksActive(noTrucksToMove1, sensor, direction, fromBranch, destBranch)  # leave the moving to the next movement
#     else:
#         direction = self.setDirection(fromBranch, destBranch)
#         sensor = self.setSensor(destBranch)     # a siding branch
#         self.countTrucksInactive(self.noTrucksOnTrain, sensor, direction, fromBranch, destBranch)  #counting all trucks on train
#         self.setSpeed(self.stop)
#     self.dedent()
# @print_name()
# def countTrucksActive_old(self, noTrucksToCount1, sensor, direction, timeout0=50, timeoutn =2, withRecovery = True):
#     #goint towards sidings
#     global glb_count
#     self.indent()
#     self.myprint1("In countTrucksActive")
#     self.myprint1("sensor", sensor)
#     self.myprint("noTrucksToCount1=" , noTrucksToCount1)
#     #for when engine needs to take corrective action after timeout
#
#     withRecovery = True    # force to show simulation
#
#     noTrucksToCount = int(noTrucksToCount1)
#     self.myprint("noTrucksToCount=" , noTrucksToCount)
#     if noTrucksToCount < 0:
#         self.myprint("quitting countTrucksActive")
#         # self.dedent()
#         # pass
#     else:
#         self.myprint(" noTruckstocount " + str(noTrucksToCount))
#         self.myprint("sensor " + self.sensorName(sensor))
#         self.myprint ("in countTrucksActive: sensor " + self.sensorName(sensor) + " noTruckstocount " + str(noTrucksToCount))
#         self.dialogs.displayMessage("entered countTrucksActive: sensor " + self.sensorName(sensor) + " noTruckstocount " + str(noTrucksToCount))
#         on_count = -1 #can count 0 to n trucks on active   The first truck is O in case we dont want to pick up one
#
#         if on_count > noTrucksToCount:
#             self.myprint("on_count > noTrucksToCount")
#         else:
#             self.myprint("on_count !> noTrucksToCount")
#         if int(on_count) == int(noTrucksToCount):
#             self.myprint ("int(on_count) == int(noTrucksToCount)")
#         else:
#             self.myprint ("int(on_count) != int(noTrucksToCount)")
#
#         self.stopflag = False
#         # self.mysound()
#         # self.waitMsec(500)
#         # self.mysound()
#         # self.waitMsec(1000)
#         #self.setSpeed(self.slow)
#
#         #self.storeSensorFrom(sensorFrom)
#         #self.storeSensorTo(sensorTo)
#         self.myprint("withRecovery",withRecovery)
#         if withRecovery == True:
#             self.storeSensor(sensor)
#         else:
#             self.myprint("x")
#
#         while self.stopflag == False:
#             on_count+=1
#             self.dialogs.displayMessage("set on_count to " + str(on_count))
#             self.myprint("on_count = ", on_count)
#             if withRecovery == True:
#                 glb_count = on_count  # no of trucks counted successfully
#             #don't uncomment these statements. It stops the program working because there is no time for the sensor to react.
#             #self.myprint("waiting for sensorActive")
#             #self.myprint("sensor = " + str(sensor))
#
#             if on_count==0:
#                 self.myprint("x")
#                 self.myprint("about to call countTrucksActive wait1")
#                 if withRecovery == True:
#                     self.storeTimeout(timeout0)
#                 if withRecovery == True:
#                     self.setSpeed(self.slow)
#                     self.countTrucksActive_wait1(sensor, direction, on_count)
#                     #self.mysound()
#                 else:
#                     self.myprint("waiting for waitChangeSensorActive with sensor" + str(self.sensorName(sensor)))
#                     speak("waiting for waitChangeSensorActive with sensor" + str(self.sensorName(sensor)))
#                     self.setSpeed(self.vslow)
#                     self.waitChangeSensorActive(sensor)
#                     self.mysound()
#             else:
#                 self.myprint("y")
#                 self.myprint("about to call countTrucksActive wait2")
#                 if withRecovery == True:
#                     self.storeTimeout(timeoutn)
#                 if withRecovery == True:
#                     self.setSpeed(self.slow)
#                     self.countTrucksActive_wait1(sensor, direction, on_count)
#                     #self.mysound()
#                 else:
#                     self.myprint("waiting for waitChangeSensorActive with sensor" + str(self.sensorName(sensor)))
#                     speak("waiting for waitChangeSensorActive with sensor" + str(self.sensorName(sensor)))
#                     self.setSpeed(self.vslow)
#                     self.waitChangeSensorActive(sensor)
#                     self.mysound()
#                 #self.waitChangeSensorActive(sensor)
#             self.myprint("z")
#             #self.waitMsec(10000)
#             #speak(str(on_count))
#             #self.mysound()
#             self.myprint("waited sensor active on_count = " + str(on_count))
#             #self.myprint("waited sensor active")
#             #self.myprint("sensor changed active " + self.sensorName(sensor) + "  noTrucksToCount =" + str(noTrucksToCount) + (" on_count = " + str(on_count)))
#             #self.myprint("xxx")
#             #fre = (on_count == noTrucksToCount)
#             #self.myprint(fre)
#             #if (on_count == noTrucksToCount):
#             #    self.myprint ("int(on_count) == int(noTrucksToCount)  " + str(on_count))
#             #else:
#             #    self.myprint ("int(on_count) != int(noTrucksToCount)  " + str(on_count))
#             #self.myprint("waited sensor active on_count = " + str(on_count))
#             #self.myprint("sensor changed active " + self.sensorName(sensor) + "noTrucksToCount " + str(noTrucksToCount) + ("on_count = " + str(on_count)))
#             if on_count == noTrucksToCount:
#                 self.myprint("on_count == noTrucksToCount")
#                 self.setSpeedSetDelay(self.stop, 500)
#                 self.myprint("Bingo on_count is " + str(on_count))
#                 self.myprint("end countTrucksActive")
#                 #self.setSpeed(self.stop)
#                 self.stopflag = True
#                 #self.dedent()
#
#             if on_count > noTrucksToCount:
#                 self.myprint("ERROR in countTrucksActive on_count > noTrucksToCount")
#                 self.setSpeed(self.stop)
#                 self.stopflag = True
#                 #self.dedent()
#
#             if on_count < noTrucksToCount:
#                 self.myprint("on_count < noTrucksToCount")
#                 #self.myprint("on_count < noTrucksToCount. on_count = " + str(on_count)+ " noTrucksToCount = " + str(noTrucksToCount))
#
#
#             self.myprint("default: on_count = "+ str(on_count)+ " noTrucksToCount= " + str(noTrucksToCount))
#
#     self.myprint1 ("end countTrucksActive: sensor " + self.sensorName(sensor) + " noTruckstocount " + str(noTrucksToCount))
#     self.dedent()
#     self.myprint1("after dedent)")
