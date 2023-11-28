import java
import jmri
import java
import jmri
from timeout import alternativeaction, variableTimeout, print_name, timeout

# @print_name()
# def countTrucksInactive(self, noTrucksToCount, sensor, direction, sidingBranch, simulate = True):
#     self.indent()
#     if self.get_branch_from_sensor(sensor) == self.spur_branch: count_from = -1 #count engine
#     else: count_from = 0
#     off_count = 99   #dummy value
#     if count_from == noTrucksToCount:   #if simulate_countTrucksInactive is not being triggered
#         self.update_displays(self.pegs)
#     self.myprint2("***************counting the trucks********************")
#     self.no_trucks_to_rectify = 0     # required if need to put the trucks back
#     for off_count in range(count_from, noTrucksToCount):
#         self.myprint2("**************off_count**********************", off_count, "count_from", count_from, "noTrucksToCount", noTrucksToCount )
#         # self.top_thread may be set in either simulate_countTrucksInactive or really_doit_countTrucksInactive
#         if simulate:
#             self.simulate_countTrucksInactive(sidingBranch, sensor, direction, off_count, self.pegs)
#             self.no_trucks_to_rectify = max([off_count, 0]) + 1
#         self.really_doit_countTrucksInactive(sensor)
#         self.myprint2("finished reallydoit")
#         self.myprint2("stop_thread1", self.stop_thread)
#
#         # if self.stop_thread == True:
#         #     print ("stop_thread2", self.stop_thread)
#         #     if simulate:
#         #         self.stop_thread == False
#         #         print ("******************moving the trucks back ****************stop_thread3", self.stop_thread)
#         #         for off_count1 in range(off_count, count_from, -1):
#         #             print ("off_count1", off_count1, "off_count", off_count,"count_from",count_from, "noTrucksToCount", noTrucksToCount )
#         #             direction1 = self.swap_direction(direction)
#         #             self.simulate_countTrucksInactive(sidingBranch, sensor, direction1, off_count, self.pegs)
#         #     break
#     self.setSpeed(self.stop)
#     self.dedent()
#
# @print_name()
# def countTrucksActive(self, noTrucksToCount, sensor, direction, sidingBranch, simulate = True):
#     self.indent()
#     if self.get_branch_from_sensor(sensor) == self.spur_branch: count_from = -1
#     else: count_from = 0
#     if count_from == noTrucksToCount:   #if simulate_countTrucksInactive is not being triggered
#         self.update_displays(self.pegs)
#     for on_count in range(count_from, noTrucksToCount):
#         # if (on_count - count_from) > 0 and simulate:
#         if simulate:
#             self.simulate_countTrucksActive(sidingBranch, sensor, direction, on_count, self.pegs)
#         self.really_doit_countTrucksActive(sensor)
#     self.really_doit_countTrucksActive(sensor)          # need an extra count because we are counting the front of the truck
#     self.setSpeed(self.stop)
#     self.dedent()


