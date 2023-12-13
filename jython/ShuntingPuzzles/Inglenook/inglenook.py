import java
import jmri
import re
from javax.swing import JOptionPane, JFrame, JLabel, JButton, JTextField, JFileChooser, JMenu, JMenuItem, JMenuBar,JComboBox,JDialog,JList
import random
from collections import deque
#from timeout import alternativeaction, variableTimeout, print_name, timeout

class Inglenook():

    pegs = [deque([]),deque([]),deque([]),deque([]),deque([]),deque([]),deque([])]
    # pegs0 = pegs[0]
    # pegs1 = pegs[1]
    # pegs2 = pegs[2]
    # pegs3 = pegs[3]
    # pegs4 = pegs[4]          # we will use this later for the trucks between the siding sensors and the spur sensor

    positions =[]

    spur_branch = 4
    mid_branch = 5

    def __init__(self, pegs, size_long_siding, size_short_sidings):
        self.pegs = pegs
        self.size_long_siding = size_long_siding
        self.size_short_sidings = size_short_sidings
        # print "self.size_short_siding", self.size_short_sidings
        # print "self.size_long_siding", self.size_long_siding

    def distribute_trucks(self):

        print "distribute_trucks-inglenook"
        no_trucks = self.get_no_trucks()

        # assume trucks have been backed up to siding_long

        # note position


        # need to distribute them
        [no_trucks_short, no_trucks_long, no_trucks_total] = self.get_no_trucks()
        print "distribute_trucks2"
        # [turnout_short, turnout_long, turnout_main] = self.get_sidings()
        # [turnout_short_direction, turnout_long_direction, turnout_main_direction] = self.get_turnout_directions()


        no_trucks_to_move = no_trucks_long
        destBranch = 1      # siding_long
        fromBranch = 4      # mid

        for p in self.moveTrucksCreatingYieldStatements(no_trucks_to_move, fromBranch, destBranch): yield p
        print "distribute_trucks3"

        # put no_trucks_long on siding_long

        # no_trucks_to_move = no_trucks_long
        # destBranch = 4      # siding_long
        # fromBranch = 5      # mid
        #
        # for p in self.moveTrucksCreatingYieldStatements(no_trucks_to_move, fromBranch, destBranch): yield p
        # print "distribute_trucks3"

        msg = "moved trucks to long siding"
        yield ["display_message", msg]

        # put rest of trucks on siding 2

        no_trucks_to_move = no_trucks_short
        destBranch = 2      # sput
        fromBranch = 4      # siding_long

        for p in self.moveTrucksCreatingYieldStatements(no_trucks_to_move, fromBranch, destBranch): yield p

        msg = "moved trucks to head shunt"
        yield ["display_message", msg]

        # put rest on siding_short
        #
        # no_trucks_to_move = no_trucks_total - no_trucks_long
        # destBranch = 4      # sput
        # fromBranch = 1      # siding_long
        #
        # for p in self.moveTrucksCreatingYieldStatements(no_trucks_to_move, fromBranch, destBranch): yield p


    def solvePuzzle(self):
        destSiding = 1
        for requiredPosition in range(self.size_long_siding,0,-1):
            msg = "$$      solve puzzle    $$: self.moveTruckToDesiredPosition " + str(requiredPosition)
            yield ["display_message", msg]

            #move trucks to the required position in order 5 4 3 2 1
            for p in self.moveTruckToDesiredPosition(requiredPosition, destSiding):
                yield p
        # return engine to spur
        noTrucks = 0
        fromBranch = 1
        destBranch = self.spur_branch
        yield ["move_trucks", noTrucks, fromBranch, destBranch, self.pegs]

    def moveTruckToDesiredPosition(self, truckNo, destSiding):
        # print("moveTruckToDesiredPosition", truckNo, destSiding)
        msg = "move trucks to the required position in order 5 4 3 2 1 : NtruckNo: " + str(truckNo) + " destSiding: " + str(destSiding)
        # print  "msg", msg
        yield ["display_message", msg]

        desiredPosition = self.size_long_siding - truckNo + 1         #starts at 1

        if self.truckInSiding(truckNo, destSiding):
            # print("truckInSiding", truckNo, destSiding)
            # a) If Truck is in top siding but not nearest buffers, move to other siding
            # if truck self.size_long_siding is in position 2, move to position 3 by putting another truck at buffers
            # If truck is in position 3 or more, move trucks to other siding
            # putting in position 3 if possible

            if not self.truckAtPositionFromEnd(truckNo, destSiding, desiredPosition + 1 -1):
                msg = "mtdpa1 " + str(truckNo) + " " +  "truck" + str(truckNo) + " not in " + str(desiredPosition) + \
                      " actually at " + str(list(self.pegs[destSiding - 1]).index(truckNo)+1)
                yield ["display_message", msg]
                #if not self.pegs[destSiding].index == desiredPosition:

                #************************************************************************************

                # move truck5 to another branch
                refPos = desiredPosition + 1 - 1 + 1     #added a 1 to check for position 2

                # check if desired truck is in position 2 (if 1 is the desired position), if so put it to position 3

                # if in position 2 we may not have enough room to take the piece from position 1 directly
                # we may have to put the piece on position 3 first
                # we wont have enough space if
                #  total no of spaces in 2 short sidings - (all the trucks - (truckno + 1)) <= 0

                [no_trucks_short, no_trucks_long, no_trucks_total] = self.get_no_trucks()
                space_in_short_sidings = 2 * no_trucks_short
                trucks_apart_from_those_in_place = no_trucks_total - (truckNo - 1)
                enough_space = space_in_short_sidings - trucks_apart_from_those_in_place
                if self.truckAtPositionFromEnd(truckNo, destSiding, refPos) and \
                                (space_in_short_sidings - trucks_apart_from_those_in_place > 0):
                    msg = "truck at 2: " + "truckNo " + str(truckNo) + " desiredPosition " + str(desiredPosition) + " refPos " + str(refPos) + " destSiding " + str(destSiding)
                    yield ["display_message", msg]
                    msg = "mtdpb1 " + str(truckNo) + " " +  " truck " + str(truckNo) + " in " + str(refPos) + " inserting truck so we can deal with it at next stage"
                    yield ["display_message", msg]
                    fromBranch = self.getOccupiedBranch(destSiding)
                    #self.insertTruck(fromBranch, destSiding, desiredPosition + 1 - 1)
                    for p in self.insertTruck(fromBranch, destSiding, refPos, truckNo): yield p
                    msg = "mtdpbb1 " + str(truckNo) + " " +  "truck" + str(truckNo) + " in " + str(refPos) + "inserted truck"
                    yield ["display_message", msg]

                # check the position of the truck is at position 3 (0,1,2,3), if put mypos = that position for display purposes
                refPos = desiredPosition + 3 - 1
                mypos = refPos - 1
                if self.truckAtPositionFromEnd(truckNo, destSiding, refPos):
                    mypos = refPos
                elif self.truckAtPositionFromEnd(truckNo, destSiding, refPos + 1):
                    mypos = refPos + 1
                elif self.truckAtPositionFromEnd(truckNo, destSiding, refPos + 2):
                    mypos = refPos + 2

                msg = "desiredPosition " + str(desiredPosition) + ", refPos " + str(refPos)+ ", mypos " + str(mypos)
                yield ["display_message", msg]
                msg = "mtdph1" + str(truckNo) + " a " +  "truck is in position " + str(mypos)
                yield ["display_message", msg]

                # if the truck is at position 3 4 or 5  (only check up to the number needed) put the truck on another branch
                # then use the algorithm for 'truck on the other branch'

                # A better routine would be to move all trucks except 2 to other branches, ensuring that the desired truck is on top
                # i.e move all trucks to left of the desired truck to other branch. then all except 2 to other branch. Might need a 'split
                # routine to ensure that all trucks get to other branch

                print "fred"

                if (self.truckAtPositionFromEnd(truckNo, destSiding, refPos) or \
                        self.truckAtPositionFromEnd(truckNo, destSiding, refPos + 1) or \
                        self.truckAtPositionFromEnd(truckNo, destSiding, refPos + 2) or \
                        self.truckAtPositionFromEnd(truckNo, destSiding, refPos - 1)):
                    msg = "truck at 2 3 4 or 5: "
                    yield ["display_message", msg]
                    msg = "refPos " + str(refPos) + " mypos " +  str(mypos)
                    yield ["display_message", msg]
                    # if self.truckAtPositionFromEnd(truckNo, destSiding, refPos):
                    #     mypos = refPos
                    # elif self.truckAtPositionFromEnd(truckNo, destSiding, refPos + 1):
                    #     mypos = refPos + 1
                    # elif self.truckAtPositionFromEnd(truckNo, destSiding, refPos + 2):
                    #     mypos = refPos + 2
                    # now we have to move the trucks to another siding
                    noTrucks = self.noOfTrucksToLeftFromEnd(destSiding, mypos - 1)   #move all trucks in position 3 4 or 5
                    msg = "noTrucks = " + str(noTrucks)
                    yield ["display_message", msg]
                    if noTrucks > 0:
                        freeBranch = 0
                        for p in self.getFreeBranch(noTrucks, destSiding):
                            i = 0
                            if i==0 :
                                freeBranch = p
                            else:
                                yield p

                        msg = "mtdpi1" + str(truckNo) + " " +  "move " + str(noTrucks) + " from " + str(destSiding) + " to " + str(freeBranch) + " as truck is in position " + str(mypos)
                        yield ["display_message", msg]

                        for p in self.moveTrucksCreatingYieldStatements(noTrucks, destSiding, freeBranch): yield p
                        msg = "mtdpj1" + str(truckNo) + " " +  "b1 refPos " +str(refPos+2)
                        yield ["display_message", msg]

                    # if (self.truckAtPositionFromEnd(truckNo, destSiding, refPos+2)):     #dont need to do this check as both options the same
                    # move truck to a free branch
                    msg = "mtdpk1" + str(truckNo) + " " +  "b2"
                    yield ["display_message", msg]
                    noTrucks = 1
                    freeBranch = 0
                    for p in self.getFreeBranch(noTrucks, destSiding):
                        if type(p) == int:
                            freeBranch = p
                        else:
                            msg = "mtdpl" + str(truckNo) + " " +  "b22"
                            yield ["display_message", msg]
                            yield p
                    msg = "mtdpm" + str(truckNo) + " " +  " freeBranch " + str(freeBranch)
                    yield ["display_message", msg]
                    if (self.truckAtPositionFromEnd(truckNo, destSiding, refPos+2)):
                        msg = "mtdpm1 " + str(truckNo) + " " + "in last position" + str(refPos+2)
                        yield ["display_message", msg]
                        #move as many trucks all at once
                        noTrucks = 2
                        freeBranch = 0
                        for p in self.getFreeBranch(noTrucks, destSiding):
                            if type(p) == int:
                                freeBranch = p
                            else:
                                msg = "mtdpl" + str(truckNo) + " " +  "b22"
                                yield ["display_message", msg]
                                yield p
                        for p in self.moveTrucksCreatingYieldStatements(noTrucks, destSiding, freeBranch): yield p
                    else:
                        msg = "mtdpm2 " + str(truckNo) + " " + "not in last position" + str(refPos+2)
                        yield ["display_message", msg]
                        for p in self.moveTrucksOneByOneCreatingYieldStatements(1, destSiding, freeBranch): yield ["display_message", msg];yield p
                    sg = "b24"
                    #insert the truck in the first position
                    msg = "self.size_long_siding " + str(self.size_long_siding) + " truckNo " + str(truckNo)
                    print msg

                    for p in self.insertTruck(freeBranch, destSiding, self.size_long_siding - truckNo + 1, truckNo): yield ["display_message", msg];yield p
                    # else:
                    #     msg = "mtdpn1" + str(truckNo) + " " +  "b3"
                    #     yield ["display_message", msg]
                    #     noTrucks = 1
                    #     # move truck to a free branch
                    #     freeBranch = 0
                    #     for p in self.getFreeBranch(noTrucks, destSiding):
                    #         if type(p) == int:
                    #             freeBranch = p
                    #         else:
                    #             yield p
                    #     for p in self.moveTrucksOneByOneCreatingYieldStatements(1, destSiding, freeBranch): yield p
                    #
                    #     msg = "&&&& self.size_long_siding" + str(self.size_long_siding) + "truckNo" + str(truckNo)
                    #     print msg
                    #     # now move the truck from the first position on the free branch to another branch
                    #     for p in self.insertTruck(freeBranch, destSiding, self.size_long_siding - truckNo + 1): yield p

            print("end of truckInSiding" + str(truckNo) + " " + str(destSiding))



        if (not self.truckInSiding(truckNo, destSiding)):
            msg = "mtdp" + str(truckNo) + " " +   "truck " + str(truckNo) + " not in siding (destSiding) " + str(destSiding)
            yield ["display_message", msg]
            truckSiding = self.getBranchNo(truckNo)
            positionOfTruck = self.PositionOfTruck(truckNo, truckSiding)
            msg = "PositionOfTruck " + str(positionOfTruck) + " truckSiding " + str(truckSiding)
            yield ["display_message", msg]
            for p in self.moveTruckToTop(truckSiding, truckNo):
                if type(p) == int:
                    freeBranch = p
                else:
                    yield p
            if freeBranch == destSiding:
                #crash_here_z    #this is kept here so can test te code
                msg = "Calling mtdp again with same parameters " + " truckNo " + str(truckNo) + " destSiding " + str(destSiding)
                yield ["display_message", msg]
                for p in self.moveTruckToDesiredPosition(truckNo, destSiding): yield p   #start again with truck in destSiding

            else:
                refpos = desiredPosition
                for p in self.insertTruck(freeBranch, destSiding, refpos, truckNo): yield p

        msg = "mtdp" + str(truckNo) + " " +  "end of moveTruckToDesiredPosition " + str(truckNo) + " " + str(destSiding)
        yield ["display_message", msg]
        #print("leave moveTruckToDesiredPosition", truckNo, destSiding)

    # def moveTruckToDesiredPosition_old(self, truckNo, destSiding):
    #     # print("moveTruckToDesiredPosition", truckNo, destSiding)
    #     msg = "move trucks to the required position in order 5 4 3 2 1 : NtruckNo: " + str(truckNo) + " destSiding: " + str(destSiding)
    #     # print  "msg", msg
    #     yield ["display_message", msg]
    #
    #     desiredPosition = self.size_long_siding - truckNo + 1         #starts at 1
    #
    #     if self.truckInSiding(truckNo, destSiding):
    #         # print("truckInSiding", truckNo, destSiding)
    #         # a) If Truck is in top siding but not nearest buffers, move to other siding
    #         # if truck self.size_long_siding is in position 2, move to position 3 by putting another truck at buffers
    #         # If truck is in position 3 or more, move trucks to other siding
    #         # putting in position 3 if possible
    #
    #         if not self.truckAtPositionFromEnd(truckNo, destSiding, desiredPosition + 1 -1):
    #             msg = "mtdpa" + str(truckNo) + " " +  "truck" + str(truckNo) + " not in " + str(desiredPosition) + \
    #                   " actually at " + str(list(self.pegs[destSiding - 1]).index(truckNo)+1)
    #             yield ["display_message", msg]
    #             #if not self.pegs[destSiding].index == desiredPosition:
    #
    #             #************************************************************************************
    #
    #             # move truck5 to another branch
    #             refPos = desiredPosition + 1 - 1 + 1     #added a 1 to check for position 2
    #
    #             # a1=self.truckAtPositionFromEnd(truckNo, destSiding, 1)
    #             # a2=self.truckAtPositionFromEnd(truckNo, destSiding, 2)
    #             # a3=self.truckAtPositionFromEnd(truckNo, destSiding, 3)
    #             # a4=self.truckAtPositionFromEnd(truckNo, destSiding, 4)
    #             # a5=self.truckAtPositionFromEnd(truckNo, destSiding, 5)
    #
    #
    #
    #             # check if desired truck is in position 2 (if 1 is the desired position), if so put it to position 3
    #
    #             if self.truckAtPositionFromEnd(truckNo, destSiding, refPos):
    #                 msg = "mtdpb" + str(truckNo) + " " +  "truck" + str(truckNo) + " in " + str(refPos) + "inserting truck so we can deal with it at next stage"
    #                 yield ["display_message", msg]
    #                 fromBranch = self.getOccupiedBranch(destSiding)
    #                 #self.insertTruck(fromBranch, destSiding, desiredPosition + 1 - 1)
    #                 for p in self.insertTruck(fromBranch, destSiding, refPos): yield p
    #                 msg = "mtdpbb" + str(truckNo) + " " +  "truck" + str(truckNo) + " in " + str(refPos) + "inserted truck"
    #                 yield ["display_message", msg]
    #
    #             #************************************************************************************
    #             # crash_here_d
    #
    #             # # check the position of the truck is at position 3, if put rp = 2
    #             # freeBranch = 0
    #             # refPos = desiredPosition + 1 -1
    #             # rp = 0
    #             # if self.truckAtPositionFromEnd(truckNo, destSiding, refPos):
    #             #
    #             #     # Myfunctions.getPositions())) {
    #             #     rp = desiredPosition + 1 - 1
    #             #     msg = "mtdpc" + str(truckNo) + " " +  "truck" + str(truckNo) + " in " + str(refPos) + " storing value rp " + str(rp)
    #             #     yield ["display_message", msg]
    #             #
    #             # # check the position of the truck is at position 4, if put rp = 3
    #             # refPos = desiredPosition + 2 - 1
    #             # if self.truckAtPositionFromEnd(truckNo, destSiding, refPos + 2):
    #             #     # Myfunctions.getPositions())) {
    #             #     rp = desiredPosition + 2 - 1
    #             #     msg = "mtdpd" + str(truckNo) + " " +  "truck" +str(truckNo) + " in " + str(refPos) + "storing value rp " + str(rp)
    #             #     yield ["display_message", msg]
    #             #
    #             # if rp > 0:
    #             #     # if truck is in positions 2 or 3 move trucks to the left of that position to leave only 1 truck to the left of it
    #             #     noTrucks = self.noOfTrucksToLeftFromEnd(destSiding, rp)
    #             #     msg = "mtdp" + str(truckNo) + " " +  "a" + " noTrucks " + str(noTrucks)
    #             #     yield ["display_message", msg]
    #             #     if (noTrucks > 1):
    #             #         # we can't have more than one truck to left of truck to position
    #             #         noTrucks1 = self.noOfTrucksToLeftFromEnd(destSiding, rp + 1)
    #             #         # move the surplus trucks
    #             #         freeBranch1 = 0
    #             #         for p in self.getFreeBranch(noTrucks1):
    #             #             if type(p) == int:
    #             #                 freeBranch1 = p
    #             #             else:
    #             #                 yield p
    #             #         # Myfunctions.getPositions());
    #             #         #for p in self.moveTrucksOneByOneCreatingYieldStatements(noTrucks1, destSiding, freeBranch1): yield p
    #             #         for p in self.moveTrucksCreatingYieldStatements(noTrucks1, destSiding, freeBranch1): yield p
    #             #
    #             #     msg = "mtdpe" + str(truckNo) + " " +  str(self.pegs)
    #             #     yield ["display_message", msg]
    #             #
    #             #     # if there is 1 truck to the left of the truck we are positioning, move the two trucks to a free branch
    #             #
    #             #     noTrucks = self.noOfTrucksToLeftFromEnd(destSiding, rp)
    #             #     if (noTrucks == 1):
    #             #         noTrucksToMove = 2
    #             #         freeBranch = 0
    #             #         for p in self.getFreeBranch(noTrucksToMove):
    #             #             i = 0
    #             #             if i == 0:
    #             #                 freeBranch = p
    #             #             else:
    #             #                 yield p
    #             #         # Myfunctions.getPositions());
    #             #         for p in self.moveTrucksOneByOneCreatingYieldStatements(noTrucksToMove, destSiding, freeBranch): yield p # ensure "5" is left on the top of the stack - use one by one
    #             #
    #             #     msg = "mtdpf" + str(truckNo) + " " +  "a2"
    #             #     yield ["display_message", msg]
    #             #
    #             #     # now move the truck from the first position on the free branch to another branch
    #             #     for p in self.insertTruck(freeBranch, destSiding, self.size_long_siding - truckNo): yield p
    #             #
    #             #     # # if there are no trucks to the left of the one we are positioning, move that truck to a free branch
    #             #     #
    #             #     # noTrucks = self.noOfTrucksToLeftFromEnd(destSiding, rp)
    #             #     # if (noTrucks == 0):
    #             #     #     # can just move truck
    #             #     #     noTrucksToMove = 1
    #             #     #     freeBranch = 0
    #             #     #     for p in self.getFreeBranch(noTrucksToMove):
    #             #     #         i = 0
    #             #     #         if i == 0:
    #             #     #             freeBranch = p
    #             #     #         else:
    #             #     #             yield p
    #             #     #     # Myfunctions.getPositions());
    #             #     #     for p in self.moveTrucksCreatingYieldStatements(noTrucksToMove, destSiding, freeBranch): yield p
    #             #     #
    #             #     # msg = "mtdpg" + str(truckNo) + " " +  "a3"
    #             #     # yield ["display_message", msg]
    #
    #
    #
    #             # check the position of the truck is at position 3 (0,1,2,3), if put mypos = that position for display purposes
    #             refPos = desiredPosition + 3 - 1
    #             mypos = 99
    #             if self.truckAtPositionFromEnd(truckNo, destSiding, refPos):
    #                 mypos = refPos
    #             elif self.truckAtPositionFromEnd(truckNo, destSiding, refPos + 1):
    #                 mypos = refPos + 1
    #             elif self.truckAtPositionFromEnd(truckNo, destSiding, refPos + 2):
    #                 mypos = refPos + 2
    #             msg = "desiredPosition " + str(desiredPosition) + ", refPos " + str(refPos)+ ", mypos " + str(mypos)
    #             yield ["display_message", msg]
    #             msg = "mtdph2" + str(truckNo) + " a " +  "truck is in position " + str(mypos)
    #             yield ["display_message", msg]
    #
    #             # if the truck is at position 3 4 or 5  (only check up to the number needed) put the truck on another branch
    #             # then use the algorithm for 'truck on the other branch'
    #
    #             # A better routine would be to move all trucks except 2 to other branches, ensuring that the desired truck is on top
    #             # i.e move all trucks to left of the desired truck to other branch. then all except 2 to other branch. Might need a 'split
    #             # routine to ensure that all trucks get to other branch
    #
    #             if (self.truckAtPositionFromEnd(truckNo, destSiding, refPos) or
    #                     self.truckAtPositionFromEnd(truckNo, destSiding, refPos + 1) or
    #                     self.truckAtPositionFromEnd(truckNo, destSiding, refPos + 2)):
    #
    #                 # now we have to move the trucks to another siding
    #                 noTrucks = self.noOfTrucksToLeftFromEnd(destSiding, mypos - 1)   #move all trucks in position 3 4 or 5
    #                 if noTrucks > 0:
    #                     freeBranch = 0
    #                     for p in self.getFreeBranch(noTrucks, destSiding):
    #                         i = 0
    #                         if i==0 :
    #                             freeBranch = p
    #                         else:
    #                             yield p
    #
    #                     msg = "mtdpi2" + str(truckNo) + " " +  "move " + str(noTrucks) + " from " + str(destSiding) + " to " + str(freeBranch) + " as truck is in position " + str(mypos)
    #                     yield ["display_message", msg]
    #
    #                     for p in self.moveTrucksCreatingYieldStatements(noTrucks, destSiding, freeBranch): yield p
    #                     msg = "mtdpj2" + str(truckNo) + " " +  "b1 refPos " +str(refPos+2)
    #                     yield ["display_message", msg]
    #
    #                 if (self.truckAtPositionFromEnd(truckNo, destSiding, refPos+2)):     #dont neeed to do this check as both options the same
    #                     # move truck to a free branch
    #                     msg = "mtdpk2" + str(truckNo) + " " +  "b2"
    #                     yield ["display_message", msg]
    #                     noTrucks = 1
    #                     freeBranch = 0
    #                     for p in self.getFreeBranch(noTrucks, destSiding):
    #                         if type(p) == int:
    #                             freeBranch = p
    #                         else:
    #                             msg = "mtdpl2" + str(truckNo) + " " +  "b22"
    #                             yield ["display_message", msg]
    #                             yield p
    #                     msg = "mtdpm2" + str(truckNo) + " " +  " freeBranch " + str(freeBranch)
    #                     yield ["display_message", msg]
    #                     for p in self.moveTrucksOneByOneCreatingYieldStatements(1, destSiding, freeBranch): yield ["display_message", msg];yield p
    #                     sg = "b24"
    #                     #insert the truck in the first position
    #                     for p in self.insertTruck(freeBranch, destSiding, self.size_long_siding - truckNo + 1): yield ["display_message", msg];yield p
    #                 else:
    #                     msg = "mtdpn2" + str(truckNo) + " " +  "b3"
    #                     yield ["display_message", msg]
    #                     noTrucks = 1
    #                     # move truck to a free branch
    #                     freeBranch = 0
    #                     for p in self.getFreeBranch(noTrucks, destSiding):
    #                         if type(p) == int:
    #                             freeBranch = p
    #                         else:
    #                             yield p
    #                     for p in self.moveTrucksOneByOneCreatingYieldStatements(1, destSiding, freeBranch): yield p
    #                     # now move the truck from the first position on the free branch to another branch
    #                     for p in self.insertTruck(freeBranch, destSiding, self.size_long_siding - truckNo + 1): yield p
    #
    #                 # msg = "mtdpo" + str(truckNo) + " " +  "b3"
    #                 # yield ["display_message", msg]
    #                 # # move truck to a free branch
    #                 # freeBranch = 0
    #                 # for p in self.getFreeBranch(noTrucks):
    #                 #     i = 0
    #                 #     if i == 0:
    #                 #         freeBranch = p
    #                 #     else:
    #                 #         yield p
    #                 # for p in self.moveTrucksOneByOneCreatingYieldStatements(1, destSiding, freeBranch): yield p
    #                 # # now move the truck from the first position on the free branch to another branch
    #                 # n = self.size_long_siding - truckNo
    #                 # for p in self.insertTruck(freeBranch, destSiding, n): yield p
    #         print("end of truckInSiding" + str(truckNo) + " " + str(destSiding))
    #
    #
    #
    #     if (not self.truckInSiding(truckNo, destSiding)):
    #         msg = "mtdp" + str(truckNo) + " " +   "truck " + str(truckNo) + " not in siding (destSiding) " + str(destSiding)
    #         yield ["display_message", msg]
    #         truckSiding = self.getBranchNo(truckNo)
    #         positionOfTruck = self.PositionOfTruck(truckNo, truckSiding)
    #         msg = "PositionOfTruck " + str(positionOfTruck) + " truckSiding " + str(truckSiding)
    #         yield ["display_message", msg]
    #         for p in self.moveTruckToTop(truckSiding, truckNo):
    #             if type(p) == int:
    #                 freeBranch = p
    #                 msg = "jim"
    #                 yield ["display_message", msg]
    #                 # crash_here_t0
    #             else:
    #                 yield p
    #         if freeBranch == destSiding:
    #             crash_here_z
    #         else:
    #             refpos = desiredPosition
    #             for p in self.insertTruck(freeBranch, destSiding, refpos): yield p
    #             return
    #
    #         # crash_here_t1
    #
    #         truckSiding = freeBranch
    #         msg = "fred"
    #         # msg = "mtdp" + str(truckNo) + " " +   "truck " + str(truckNo) + " moved to top of (freebranch) " + str(freeBranch) + str(self.pegs)
    #         yield ["display_message", msg]
    #         # crash_here_t
    #
    #         # b) If Truck 5 is nearest buffer of another siding
    #         # Ensure siding has one spare slot
    #         # Move a Truck to buffer
    #         # Ensure siding has one spare slot
    #         if self.truckAtPositionFromEnd(truckNo, truckSiding, 0+1):
    #             noTrucks = self.noOfTrucksToLeftFromEnd(truckSiding, 0)
    #             if (noTrucks > 0):
    #                 # better occupied branch excluding all trucks less than
    #                 # current truck
    #                 otherBranch = self.getOtherBranch(destSiding, truckSiding)
    #                 noOfTrucksInOtherBranch = self.noOfTrucksInBranch(otherBranch)
    #                 if self.noOfTrucksInBranch(otherBranch) == 0:
    #                     msg = "otherBranch " + str(otherBranch) + " noOfTrucksInOtherBranch " + str(noOfTrucksInOtherBranch) + \
    #                           " truckSiding " + str(truckSiding) + " noTrucks " + str(noTrucks)
    #                     yield ["display_message", msg]
    #                     self.moveTrucksOneByOneCreatingYieldStatements(min(2, noTrucks), truckSiding, otherBranch)
    #                     # if noTrucks > 3 then the remaining trucks and the truck
    #                     # to position will not be able to fit on branch 4
    #                     if (noTrucks >= 3):
    #                         crash_here_h
    #                         for p in self.moveTrucksOneByOneCreatingYieldStatements(1, truckSiding, otherBranch): yield p
    #                         truckSiding = self.getBranchNo(truckNo)
    #                 elif (self.noOfTrucksInBranch(otherBranch) == 1):
    #                     msg = "otherBranch " + str(otherBranch) + " noOfTrucksInOtherBranch " + str(noOfTrucksInOtherBranch)+ \
    #                           " truckSiding " + str(truckSiding) + " noTrucks " + str(noTrucks)
    #                     yield ["display_message", msg]
    #                     for p in self.moveTrucksOneByOneCreatingYieldStatements(min(2, noTrucks), truckSiding, otherBranch): yield p
    #                 elif (self.noOfTrucksInBranch(otherBranch) == 2):
    #                     msg = "otherBranch " + str(otherBranch) + " noOfTrucksInOtherBranch " + str(noOfTrucksInOtherBranch)+ \
    #                           " truckSiding " + str(truckSiding) + " noTrucks " + str(noTrucks)
    #                     yield ["display_message", msg]
    #                     # cresh_here_f
    #                     for p in self.moveTrucksOneByOneCreatingYieldStatements( truckSiding, 1,  otherBranch): yield p
    #                     if (noTrucks == 2):
    #                         for p in self.moveTrucksOneByOneCreatingYieldStatements(1, truckSiding, destSiding): yield p
    #                     for p in self.moveTrucksOneByOneCreatingYieldStatements(noTrucks, truckSiding, destSiding): yield p
    #                     for p in self.moveTrucksOneByOneCreatingYieldStatements(1, truckSiding, 4): yield p
    #                     self.noTrucks1 = min(self.noOfTrucksToLeftFromEnd(destSiding, self.size_long_siding - (truckNo + 1)), 2)
    #                     for p in self.moveTrucksOneByOneCreatingYieldStatements(self.noTrucks1, 1, 4): yield p
    #                     for p in self.moveTrucksOneByOneCreatingYieldStatements(4, self.noOfTrucksInBranch(4), truckSiding): yield p
    #
    #             refPos = self.size_long_siding - truckNo;
    #             for p in self.insertTruck(truckSiding, destSiding, refPos): yield p
    #
    #         elif self.truckAtPositionFromEnd(truckNo, truckSiding, 1+1):
    #             crash_here_x
    #             noTrucks = self.noOfTrucksToLeftFromEnd(truckSiding, 1)
    #             if noTrucks > 0:
    #                 # better occupied branch excluding all trucks less than
    #                 # current truck
    #                 other_branch = self.getOtherBranch(destSiding, truckSiding)
    #                 if self.noOfTrucksInBranch(other_branch) <= 2:
    #                     for p in self.moveTrucksOneByOneCreatingYieldStatements(1, truckSiding, other_branch): yield p
    #                 else:
    #                     for p in self.insertTruck(other_branch, truckSiding, 1 + 1 ): yield p
    #
    #             for p in self.insertTruck(truckSiding, destSiding, self.size_long_siding - truckNo + 1): yield p
    #         else:
    #             # crash_here_y
    #
    #             # check the position of the truck
    #
    #             freeBranch = 0
    #             refPos = 2
    #             if (self.truckAtPositionFromEnd(truckNo, truckSiding, refPos+1)):
    #                 refPos1 = self.size_long_siding - truckNo  # because of the numbering
    #                 for p in self.insertTruck(truckSiding, destSiding, refPos1): yield p
    #         msg = "mtdp" + str(truckNo) + " " +   "end of truck " + str(truckNo) + " not in siding (destSiding) " + str(destSiding)
    #         yield ["display_message", msg]
    #
    #     msg = "mtdp" + str(truckNo) + " " +  "end of moveTruckToDesiredPosition " + str(truckNo) + " " + str(destSiding)
    #     yield ["display_message", msg]
    #     #print("leave moveTruckToDesiredPosition", truckNo, destSiding)

    def PositionOfTruck(self, truckNo, destSiding):
        return list(self.pegs[destSiding - 1]).index(truckNo)+1

    def truckAtPositionFromEnd(self, truckNo, branchNo, position):
        return position == list(self.pegs[branchNo - 1]).index(truckNo) + 1


    def moveTruckToTop(self, destSiding, truckNo):
        #get position of truck
        mypos = self.PositionOfTruck(truckNo, destSiding)
        # now we have to move the trucks to another siding
        noTrucks = self.noOfTrucksToLeftFromEnd(destSiding, mypos - 1)   #move all trucks in position 3 4 or 5

        msg = "PositionOfTruck " + str(mypos) + " noTrucks " + str(noTrucks)
        yield ["display_message", msg]

        #move trucks to left
        if noTrucks > 0:
            freeBranch = 0
            for p in self.getFreeBranch(noTrucks, destSiding):
                if type(p) == int:
                    freeBranch = p
                else:
                    yield p

            msg = "mtttopb" + str(truckNo) + " " +  "move " + str(noTrucks) + " from " + str(destSiding) + " to " + str(freeBranch) + " as truck is in position " + str(mypos)
            yield ["display_message", msg]

            for p in self.moveTrucksCreatingYieldStatements(noTrucks, destSiding, freeBranch): yield p

            # move the truck itself
            # move truck to free branch
            msg = "mtttopc" + str(truckNo) + " " +  "b2"
            yield ["display_message", msg]
            noTrucks = 1
            no_trucks = min(self.noOfTrucksInBranch(destSiding), self.noSpacesinBranch(freeBranch))
            if no_trucks > 0:
                for p in self.moveTrucksCreatingYieldStatements(no_trucks, destSiding, freeBranch): yield p
                finalBranch = freeBranch
                msg = "mtttope" + str(truckNo) + " " +  " freeBranch " + str(freeBranch) + str(self.pegs)
            else:
                finalBranch = destSiding
                msg = "mtttope" + str(truckNo) + " " +  " finalBrancj " + str(finalBranch) + str(self.pegs)
            yield ["display_message", msg]
            yield finalBranch
        else:
            yield destSiding

    def insertTruck(self, from_branch, destination_branch, refPos, truckNo):      # counts from 1

        msg = "  ita"+ " " +  "insertTruck: " + "from_branch " + str(from_branch) + \
              " destination_branch " + str(destination_branch) + " refPos " + str(refPos) + " " + str(self.pegs)
        yield ["display_message", msg]

        # we move trucks so there are no more than 2 trucks to move from the dest branch

        # move trucks from toBranch to head
        # no_trucks_to_move = self.noOfTrucksToLeftFromEnd(destination_branch, refPos + 1) + 1
        no_trucks_to_move = self.noOfTrucksToLeftFromEndCountFrom1(destination_branch, refPos) + 1
        msg = "  itb"+ " " +  "no_trucks_to_move: "  + str(no_trucks_to_move)
        yield ["display_message", msg]


        if no_trucks_to_move == 0:
            for p in self.moveTrucksOneByOneCreatingYieldStatements(1, from_branch, destination_branch): yield p
            return
        if no_trucks_to_move > 2:
            # move the excess trucks to another branch
            noTrucks1 = no_trucks_to_move - 2
            no_trucks_to_move = 2
            other_branch = self.getOtherBranch(from_branch, destination_branch)
            msg = "  itc"+ " " +  "other_branch: "  + str(other_branch)
            yield ["display_message", msg]
            if self.noSpacesinBranch(other_branch) == 0:
                # need to put required no trucks (noTrucks1) on the from_branch, but leave the truck we want to move on the top. i.e. insert a truck
                msg = "  itcc about to insert " + str(noTrucks1) + " truck(s) " + " destination_branch " + str(destination_branch) + \
                      " from_branch " + str(from_branch) + " refPos " + str(refPos) + str(self.pegs)
                yield ["display_message", msg]
                for i in range(noTrucks1):
                    for p in self.insertTruck(destination_branch, from_branch, 0 + 1, truckNo): yield p
                # crash_here_a
            else:
                if self.noSpacesinBranch(other_branch) < noTrucks1:
                    # crash_here_b
                    for p in self.moveTrucksCreatingYieldStatements(self.noOfTrucksInBranch(from_branch), from_branch, other_branch): yield p
                    # move trucks on from branch to other branch
                    temp = from_branch
                    from_branch = other_branch
                    other_branch = temp

                for p in self.moveTrucksCreatingYieldStatements(noTrucks1, destination_branch, other_branch): yield p
                msg = "  itd"+ " moved noTrucks1 " + str(noTrucks1) +  " to other_branch: "  + str(other_branch)
                yield ["display_message", msg]

        msg = "  ite"+ " " +  " now have only max 2 trucks on destination_branch : "  + str(destination_branch)+ " " +str(self.pegs)
        yield ["display_message", msg]
        # msg = "  itee00 "+ "truckNo " + str(truckNo) + " from_branch " + str(from_branch) + " " +str(self.pegs)
        # yield ["display_message", msg]
        # positionOfTruckFrom = self.PositionOfTruck(truckNo, from_branch)
        # msg = "  itee01 "+ "positionOfTruckFrom " + str(positionOfTruckFrom)
        # yield ["display_message", msg]
        # no_trucks_to_move_from = self.noOfTrucksToLeftFromEndCountFrom1(from_branch, positionOfTruckFrom) + 1
        # msg = "  itee02 "+ "positionOfTruckFrom " + str(positionOfTruckFrom) + " no_trucks_to_move_from " +str(no_trucks_to_move_from)
        # yield ["display_message", msg]
        # no_trucks_head = self.noOfTrucksInBranch(4)
        # msg = "  itee03 "+ "positionOfTruckFrom " + str(positionOfTruckFrom) + " no_trucks_to_move_from " +str(no_trucks_to_move_from) + " no_trucks_head " + str(no_trucks_head)
        # yield ["display_message", msg]

        # if (no_trucks_to_move + no_trucks_to_move_from + no_trucks_head)< 3:
        #     for p in self.moveTrucksCreatingYieldStatements(no_trucks_to_move, destination_branch, 4): yield p
        #     msg = "  itee1 "+ " moved no_trucks_to_move " + str(no_trucks_to_move) +  " to head: "  + str(4)
        #     yield ["display_message", msg]
        #
        #     for p in self.moveTrucksCreatingYieldStatements(no_trucks_to_move_from, from_branch, 4): yield p
        #     msg = "  itee2 "+ " moved no_trucks_to_move_from " + str(no_trucks_to_move_from) +  " to head: "  + str(4)
        #     yield ["display_message", msg]
        #
        #     for p in self.moveTrucksCreatingYieldStatements(1, 4, from_branch): yield p
        #     msg = "  itee3 "+ " moved 1 " +  " to from_branch : "  + str(from_branch)
        #     yield ["display_message", msg]
        #
        #     for p in self.moveTrucksCreatingYieldStatements(0, from_branch, 4): yield p
        #     msg = "  itee4 "+ " moved 0 " +  " to head : "  + str(4)
        #     yield ["display_message", msg]
        #
        #     for p in self.moveTrucksCreatingYieldStatements( \
        #             no_trucks_to_move + no_trucks_to_move_from + no_trucks_head - 1, 4, from_branch): yield p
        #     msg = "  itee5 "+ " moved rest " + \
        #           str(no_trucks_to_move + no_trucks_to_move_from + no_trucks_head - 1) + " to head : "  + str(4)
        #     yield ["display_message", msg]
        # else:
        for p in self.moveTrucksCreatingYieldStatements(no_trucks_to_move, destination_branch, 4): yield p

        # need a space on the destiation branch as "5" or whatever no is being positioned will be on head
        msg = "  itf"+ " " +  " now have only max 2 trucks on destination_branch : "  + str(destination_branch)
        yield ["display_message", msg]

        #move "5" to head
        # move 1 truck from fromBranch to head
        no_trucks_to_move = 1
        for p in self.moveTrucksCreatingYieldStatements(no_trucks_to_move, from_branch, 4): yield p

        msg = "  itff"+ " " +  " pegs : "  + str(self.pegs)
        yield ["display_message", msg]
        # move trucks from head to to Branch 1 (destination Branch)
        # move so we have "5xx" on head
        no_trucks_to_move1 = min(self.noOfTrucksInBranch(4)-1,     #engine
                                 self.capacityOfBranch(destination_branch) - self.noOfTrucksInBranch(destination_branch))
        msg = "  itg"+ " " +  "move " +str(no_trucks_to_move1) + " trucks from head to destination_branch " + str(destination_branch)
        yield ["display_message", msg]
        for p in self.moveTrucksCreatingYieldStatements(no_trucks_to_move1, 4, destination_branch): yield p

        # there may be sometrucks left on branch 4. move them to another branch

        no_trucks_to_move2 = self.noOfTrucksInBranch(4) - 1  # take off 1 for the engine
        if no_trucks_to_move2 > 0:
            msg = "  ith"+ " " +  "move2: move " +str(no_trucks_to_move2) + " trucks from head to toBranch" + " from_branch " + str(from_branch)
            yield ["display_message", msg]
            # freeBranch = 0
            # for p in self.getFreeBranch(no_trucks_to_move2, from_branch):
            #     if type(p) is int:
            #         freeBranch = p
            #     else:
            #         yield p

            for p in self.moveTrucksCreatingYieldStatements(no_trucks_to_move2, 4, from_branch): yield p
        msg = "  iti end " + str(self.pegs)
        yield ["display_message", msg]

    def moveTrucksCreatingYieldStatements(self, noTrucks, fromBranch, destBranch):

        msg = "    mtcys"+ " " +  "moveTrucks noTrucks: " + str(noTrucks) + " fromBranch " + str(fromBranch) + \
              " destBranch " + str(destBranch) + " " + str(self.pegs)
        yield ["display_message", msg]
        #print(self.pegs)

        # print ("move_trucks", noTrucks, fromBranch,  destBranch)

        # yield ["move_trucks", noTrucks, fromBranch, destBranch, self.pegs]

        # fromBranch = 1
        # destBranch = 2
        # noTrucks = 3
        # take from fromBranch, put on 4
        mid_branch = 5
        if fromBranch < self.spur_branch or destBranch == self.spur_branch or destBranch == mid_branch:   #if not at spur, move to spur
            for i in range(noTrucks):
                msg = "    mtcys1"+ " " +  "move Truck to spur: " + str(i)
                yield ["display_message", msg]
                # print("self.pegs[fromBranch]",self.pegs[fromBranch-1])
                # print("self.pegs[spur_branch]",self.pegs[self.spur_branch-1])
                # print ("self.pegs",self.pegs)

                if destBranch == mid_branch:
                    # print "a"
                    self.pegs[mid_branch-1].append(self.pegs[fromBranch-1].pop())
                else:
                    # print "bb"
                    # print self.pegs
                    self.pegs[self.spur_branch-1].append(self.pegs[fromBranch-1].pop())
            yield self.pegs
        msg = "    mtcys2"+ " moved to head " + str(self.pegs)
        yield ["display_message", msg]
        if destBranch != 4:    # if we want to go to a siding, go there
            for i in range(noTrucks):
                msg = "    mtcys"+ " " +  "move Truck to branch: " + str(destBranch)
                yield ["display_message", msg]
                if fromBranch == self.mid_branch:
                    print "pegs", self.pegs
                    self.pegs[destBranch-1].append(self.pegs[self.mid_branch-1].pop())   #only use for distribution
                else:
                    self.pegs[destBranch-1].append(self.pegs[self.spur_branch-1].pop())
            yield self.pegs
        #print (self.pegs)
        # print("leave moveTrucksCreatingYieldStatements", noTrucks, fromBranch, destBranch)
        msg = "    mtcys3"+ " " +  "finished moveTrucksCreatingYieldStatements " + str(self.pegs)
        yield ["display_message", msg]

    def moveTrucksOneByOneCreatingYieldStatements(self, noTrucks, fromBranch, destBranch):
        # print ("move_trucks_one_by_one", noTrucks, fromBranch,  destBranch)
        msg = "mtobo"+ " " +  "moveTrucks noTrucks: " + str(noTrucks) + " fromBranch "  + str(fromBranch) + " destBranch " + str(destBranch)
        yield ["display_message", msg]
        #print("moveTrucks", noTrucks, fromBranch, destBranch)
        #print(self.pegs)

        yield ["move_trucks_one_by_one", noTrucks, fromBranch, destBranch, self.pegs]

        for i in range(0, noTrucks):
            msg = "mtobo"+ " " +  "move Truck: " + str(i)
            yield ["display_message", msg]
            if fromBranch != self.spur_branch:
                self.pegs[self.spur_branch-1].append(self.pegs[fromBranch-1].pop())
                yield self.pegs
            if destBranch != 4:
                self.pegs[destBranch-1].append(self.pegs[self.spur_branch-1].pop())
                yield self.pegs
        # print("leave moveTrucksOneByOneCreatingYieldStatements", noTrucks, fromBranch, destBranch)

    def keys_from_dict(self, dict1):
        return list(dict1.keys())

    def values_from_dict(self, dict1):
        return list(dict1.values())

    def dict_from_lists(self, keys, values):
        return {k: v for k, v in zip(keys, values)}

    def getBranchNo(self, truckNo):
        for branchno in range(1,5):
            if self.truckInSiding(truckNo, branchno):
                return branchno
        return 99

    def noOfTrucksInBranch(self,branchNo):
        return len(self.pegs[branchNo - 1])

    def getFreeBranch(self, noTrucksRequired, currentBranch):

        freeBranch = 0
        # getthe other branches
        for i in range(1,3):
            if i != currentBranch:
                otherBranch1 = i
        otherBranch2 = self.getOtherBranch(currentBranch, otherBranch1)
        print "otherBranch1", otherBranch1
        print "otherBranch2", otherBranch2

        if self.noSpacesinBranch(otherBranch1) <= noTrucksRequired or self.noSpacesinBranch(otherBranch2) <= noTrucksRequired:
            print "a"
            print "self.noSpacesinBranch(otherBranch1)", self.noSpacesinBranch(otherBranch1), "self.noSpacesinBranch(otherBranch2)", self.noSpacesinBranch(otherBranch2)
            print "noTrucksRequired", noTrucksRequired
            #choose a shorter branch if possible
            if otherBranch1 != 1 and self.noSpacesinBranch(otherBranch1) >= noTrucksRequired:
                freeBranch = otherBranch1
            else:
                freeBranch = otherBranch2
            print "freeBranch", freeBranch
            yield freeBranch
        elif self.noSpacesinBranch(otherBranch1) + self.noSpacesinBranch(otherBranch2) >= noTrucksRequired:
            print "b"
            print "self.noSpacesinBranch(otherBranch1)", self.noSpacesinBranch(otherBranch1), "self.noSpacesinBranch(otherBranch2)", self.noSpacesinBranch(otherBranch2)
            # move the trucks between the branches so there is enough room
            if self.noSpacesinBranch(otherBranch1) > self.noSpacesinBranch(otherBranch2):
                fromBranch = otherBranch1
                toBranch = otherBranch2
            else:
                fromBranch = otherBranch2
                toBranch = otherBranch1

            print "toBranch", toBranch, "fromBranch", fromBranch

            noTrucksToMove = NoOfTrucksRequired - self.noSpacesinBranch(fromBranch)
            for p in self.moveTrucksCreatingYieldStatements(noTrucksToMove, fromBranch, toBranch): yield p
            yield fromBranch

    def getFreeBranch_old(self, NoOfTrucksRequired):
        #finds a free branch, if not creates one
        #print("getFreeBranch" )
        if (self.size_short_sidings - self.
                noOfTrucksInBranch(2)) >= NoOfTrucksRequired :
            yield 2
            #print("getFreeBranch",2)
            return
        elif ((self.size_short_sidings - self.noOfTrucksInBranch(3)) >= NoOfTrucksRequired) :
            yield 3
            #print("getFreeBranch",3)
            return

        else:
            if self.noOfTrucksInBranch(2) < self.noOfTrucksInBranch(3) :
                noTrucksToMove = self.size_short_sidings - self.noOfTrucksInBranch(2) - NoOfTrucksRequired
                refPos = self.size_short_sidings - noTrucksToMove
                for p in self.moveTrucksOneByOneCreatingYieldStatements(noTrucksToMove, 2, 3): yield p
                yield 2
                #print("getFreeBranch",2)
                return
            else:
                noTrucksToMove = NoOfTrucksRequired - self.noOfTrucksInBranch(3)
                refPos = self.size_short_sidings - noTrucksToMove
                for p in self.moveTrucksOneByOneCreatingYieldStatements(noTrucksToMove, 3, 3): yield p
                yield 3
                #print("getFreeBranch",3)
                return

    def getOccupiedBranch(self, truckSiding):
        # finds a branch (not equal to truckSiding) that has at least 1 truck
        if truckSiding == 1:
            if self.noOfTrucksInBranch(2) > 0:
                return 2
            else:
                return 3
        if truckSiding == 2:
            if self.noOfTrucksInBranch(1) > 0:
                return 1
            else:
                return 3
        if truckSiding == 3:
            if self.noOfTrucksInBranch(0) > 0:
                return 0
            else:
                return 1

    def capacityOfBranch(self, destBranch) :
        if destBranch == 1 :
            return self.get_no_trucks1("long")
        else:
            return self.get_no_trucks1("short")

    def noSpacesinBranch(self, Branch) :
        #print "self.noOfTrucksInBranch(Branch)", self.noOfTrucksInBranch(Branch), "self.capacityOfBranch(Branch)", self.capacityOfBranch(Branch);
        return self.capacityOfBranch(Branch) - self.noOfTrucksInBranch(Branch)


    def getOtherBranch(self,fromBranch, destBranch):

        return 6 - fromBranch - destBranch  # as sum of 1 + 2 + 3 = 6, the formula follows

    def noOfTrucksToLeftFromEnd(self,branchNo, posfromend) :
        # counts from 0
        noOfTrucksToLeft = self.noOfTrucksInBranch(branchNo) - posfromend - 1
        return noOfTrucksToLeft

    def noOfTrucksToLeftFromEndCountFrom1(self,branchNo, posfromend) :
        # counts from 0
        noOfTrucksToLeft = self.noOfTrucksInBranch(branchNo) - posfromend
        return noOfTrucksToLeft

    def truckInSiding(self, truckNo, branchNo):
        # print (self.pegs[branchNo - 1].count(truckNo))
        # print (self.pegs[branchNo - 1])
        # print (self.pegs)
        # print( self.pegs[branchNo - 1].count(truckNo)>0)
        return self.pegs[branchNo - 1].count(truckNo)>0

    def get_no_trucks(self):

        no_trucks_short = self.get_no_trucks1("short")
        no_trucks_long = self.get_no_trucks1("long")
        no_trucks_total = self.get_no_trucks1("total")

        return [no_trucks_short, no_trucks_long, no_trucks_total]

    def get_no_trucks1(self, no_trucks_str):
        #no_trucks is of the form short, long, total
        memories1 = jmri.InstanceManager.getDefault(jmri.MemoryManager)
        no_trucks = memories1.getMemory('IMIS:no_trucks_' + no_trucks_str)
        print "$$$$$$$$$$$$$$$$*", no_trucks, 'IMIS:no_trucks_' + no_trucks_str
        return int(no_trucks.getValue())



if __name__ == '__main__':
    ingle = Inglenook()
    ingle.init_position_branch()

    assert ingle.positions.count(1) == 1
    assert ingle.branches.count(1) == 5

