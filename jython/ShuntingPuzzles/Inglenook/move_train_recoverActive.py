import speak
import java
import jmri

# def alt_action_countTrucksActive2(self, fromSensor):
#     global glb_count
#     #self.indent()
#     self.myprint ("in alt_action_countTrucksActive2 ")
#
#
#     self.setSpeed(self.stop)
#
#     self.myprint("WAITING")
#     self.waitMsec(10000)
#
#     sp = Speak()
#
#     sp.speak("in alt_action_countTrucksActive2")
#     self.waitMsec(5000)
#
#     #change direction of travel
#     self.myprint ("sensor:", fromSensor)
#
#     mySensorName = self.sensorName(fromSensor)
#     sp.speak("at sensor " + mySensorName)
#
#     #move back to sensorFrom
#     self.myprint("alt_action_countTrucksActive2 w")
#     fromBranch = None
#     self.myprint("alt_action_countTrucksActive2 w1")
#     fromBranch = self.setBranch(fromSensor)
#     self.myprint("alt_action_countTrucksActive2 x")
#
#     self.myprint("No trucks to return glb_count" , glb_count)
#     noTrucksToReturn = glb_count
#     self.returnToBranch(self.noTrucksOnTrain, noTrucksToReturn, fromBranch)
#
#     self.myprint("glb_count after returnToBranch" , glb_count)
#
#
#     self.myprint("alt_action_countTrucksActive2 y")
#
#     self.setSpeed(self.stop)
#     self.moveDistance(self.smallDistance)
#     self.couple1(fromBranch)
#     self.changeDirection()
#     self.moveDistance(self.smallDistance)
#     self.myprint("alt_action_countTrucksActive2 z")
#
#     sensor = self.setSensor(4)
#     self.myprint("noTrucksToCountAgain glb_count" , glb_count)
#     noTrucksToCountAgain = glb_count
#     self.myprint("noTrucksToCountAgain " , noTrucksToCountAgain)
#     self.countTrucksAgain(noTrucksToCountAgain, fromSensor)
#
#     self.myprint("WAITING")
#     speak("We have recounted the trucks successfully")
#     self.waitMsec(10000)
#     self.dedent()
#
# def returnToBranch(self, noTrucksOnTrain, noTrucksToMove, destBranch):
#     self.indent()
#     # move the train to destbranch without any coupling or decoupling
#     # we have already checked that the branch we are in is not destBranch
#     self.myprint(">>in returnToBranch")
#     self.myprint("noTrucksToMove " + str(noTrucksToMove) + " destBranch " + str(destBranch))
#
#
#
#     if destBranch != 4:
#         #announce that are moving trucks
#         #speak = ("moving to branch " + str(destBranch))
#
#         self.myprint("destBranch != 4:"+ str(destBranch))
#         direction = self.setPointsAndDirection(4,destBranch)
#         self.waitMsec(5000)
#         noToCount = noTrucksToMove
#         sensor = self.setSensor(destBranch)
#         self.myprint("returnToBranch 0")
#         #self.countTrucksActive(noTrucksToMove, sensor)
#
#         #self.setSpeed(self.slow)
#         self.countTrucksActive(noToCount, sensor, direction, withRecovery = False)  # leave the moving to the next movement
#         self.myprint("returnToBranch 1")
#
#         #self.myprint("about to couple")
#         #self.couple1(destBranch)
#         self.setSpeed(self.stop)
#         self.myprint("returnToBranch 2")
#     else:
#         #speak = ("moving to head")
#         self.myprint("moving to branch 4")
#         #the points will have been set as we are moving back to branch 4
#         anyBranch = 1  # choose any branch, the direction is the same
#         direction = self.setDirection(anyBranch,4)
#         #self.setSpeed(self.slow)
#         # going towards head count number of times becomes inactive
#
#         sensor = self.setSensor(destBranch)
#         self.myprint ("noTrucksOnTrain before = ", self.noTrucksOnTrain)
#         self.myprint ("noTrucksToMove before = ", noTrucksToMove)
#         self.noTrucksOnTrain += noTrucksToMove
#         self.myprint ("noTrucksOnTrain after = ", self.noTrucksOnTrain)
#         extra = 1 # for engine count
#         #speak("counting"+str(self.noTrucksOnTrain)+"trucks and engine")
#         self.countTrucksActive(self.noTrucksOnTrain + extra, sensor, direction, withRecovery = False) #counting all trucks on train
#         self.setSpeed(self.stop)
#
#     self.myprint("end returnToBranch: " + "noTrucksToMove " + str(noTrucksToMove) + " destBranch " + str(destBranch))
#     self.dedent()
#
# def countTrucksAgain(self, noTrucksToCount, sensor):
#     # the number of trucks to count is the number already counted plus 1 (including the failed one)
#     self.indent()
#     self.myprint("In countTrucksAgain")
#     self.setSpeed(self.stop)
#     self.myprint("Calling countTrucksActive")
#     self.countTrucksActive(noTrucksToCount, sensor, direction, withRecovery = False)
#     self.myprint("counted the trucks successfully")
#     self.setSpeed(self.stop)
