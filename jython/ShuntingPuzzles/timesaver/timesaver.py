import random
import sys
import traceback


logValue = 3
loggingInstructions = "print"

import logging
logging.basicConfig(filename='Z:\\ConfigProfiles\\jython\\timesaver\\example.log',filemode='w',level=logging.DEBUG)
logging.debug('******************************')
logging.info('So should this')
logging.warning('And this, too')

class TimeSaver:

    pegs = [[],[],[],[],[],[]]
    pegs0 = pegs[0]
    pegs1 = pegs[1]
    pegs2 = pegs[2]
    pegs3 = pegs[3]
    pegs4 = pegs[4]
    pegs5 = pegs[5]
    
    rpegs = [[],[],[],[],[],[]]
    rpegs0 = rpegs[0]
    rpegs1 = rpegs[1]
    rpegs2 = rpegs[2]
    rpegs3 = rpegs[3]
    rpegs4 = rpegs[4]
    rpegs5 = rpegs[5]

    positions =[]
    
    indentno = 2
    
    #@staticmethod
    def  pp(self, *args):       
    
        #pretty print
        
        
        #print ("logging")
        if loggingInstructions == "print":
            print(" " * self.indentno),
            for arg in args:  
                print (arg), 
            print("")
        msg = " " * self.indentno
        #print(msg + "!")
        for arg in args: 
            msg = msg + " " + str(arg)
        logging.debug(msg)
        
    def mysound(self):
        #self. pp(("bell")
        snd = jmri.jmrit.Sound("resources/sounds/Bell.wav")
        snd.play()
        #self. pp(("bell end")
        
    def get_function_name(self):
        return traceback.extract_stack(None, 3)[0][2]              

    
    def indent(self):
        self.indentno = self.indentno + 2
        x = self.get_function_name()
        self.pp("entering " , x )
        
    def dedent(self):
        self.pp("exiting " , self.get_function_name())
        self.indentno = self.indentno - 2
        
    def __init__(self, pegs, rpegs):
        self.indent()
        self.pegs = pegs
        self.rpegs = rpegs
        #print("in init")
        self.dedent()
        
    # def __init__(self, pegs, rpegs):
        # print("in init")
        #pegs is what we have, rpegs is what we require
        # self.indent()
        # self.pp("in __init__")
        # self.pegs = pegs
        # self.rpegs = rpegs
        # self.dedent()

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

    #def getFreeBranch(self, NoOfTrucksRequired):

    def solvePuzzle(self):
        
        #self.pegs  is the position now
        #self.rpegs is the position required
        
        #  ---branch1------/---------------branch2----
        #                 /
        #                /--branch3--\
        #               /             \
        #   --branch4--/--/-branch5----\---branch5---
        #                /
        #   --branch6---/
        

        self.indent()
        self.clearCentre()
        
        self.moveToPosition()
        
            
            
        # if not rbranchempty(0):
            # solvepuzzle(
        
        
        #find the branch that contains the
        self.dedent()        
        
    def clearCentre(self):
        self.indent()
        #clear the centre (branches 2,3,4,5) and put in 6, and then in 1 if 6 is full
        # we assume for now that there is only one in 5
        # if not branchempty(5):
            # xmove(5,6)
        # pass
        pass
        self.dedent()
    
    def moveToPosition(self):
        self.indent()
        a = self.pegs_in_position()
        while not a:
            # # # from_pos = 
            # # # to_peg =
            # # # move_peg(from_pos,to_pos)
            pass
            
        self.dedent()
        
    def pegs_in_position(self):
        self.indent
        self.dedent
        return True;
        # for i in [1,2,7]
            # if not rpegs[i] == pegs[i]  #check whteher all items in branch are in place
                # for pegs in rpegs[i]    
                    # print ("pegs_in_position", pegs)
        
        # #determine from positionn
        
        
        
        # for branch in range(0,5):
            # for truck in range(count
            
                    
            

    def solvePuzzleold(self):
        destSiding = 1
        for requiredPosition in range(5,0,-1):
            for p in self.moveTruckToDesiredPosition(requiredPosition, destSiding):
                #l = list(p)
                #print ("in solve puzzle" , list([p]))
                yield p
        # p = self.moveTruckToDesiredPosition(4, destSiding)
        # yield p
        # p = self.moveTruckToDesiredPosition(3, destSiding)
        # self.moveTruckToDesiredPosition(2, destSiding)
        # self.moveTruckToDesiredPosition(1, destSiding)


    def getFreeBranch(self, NoOfTrucksRequired):
        #finds a free branch, if not creates one
        print("getFreeBranch" )
        if (3 - self.noOfTrucksInBranch(2)) >= NoOfTrucksRequired :
            yield 2
            print("getFreeBranch",2)
            return
        elif ((3 - self.noOfTrucksInBranch(3)) >= NoOfTrucksRequired) :
            yield 3
            print("getFreeBranch",3)
            return

        else:
            if self.noOfTrucksInBranch(2) < self.noOfTrucksInBranch(3) :
                noTrucksToMove = 3 - self.noOfTrucksInBranch(2) - NoOfTrucksRequired
                refPos = 3 - noTrucksToMove
                for p in self.moveTrucks( noTrucksToMove,2, 3): yield p
                yield 2
                print("getFreeBranch",2)
                return
            else:
                noTrucksToMove = NoOfTrucksRequired - self.noOfTrucksInBranch(3)
                refPos = 3 - noTrucksToMove
                for p in self.moveTrucks( noTrucksToMove,3, 3): yield p
                yield 3
                print("getFreeBranch",3)
                return


    # def yieldgetFreeBranch(self, NoOfTrucksRequired):
    #     #finds a free branch, if not creates one
    #     if (3 - self.noOfTrucksInBranch(2)) >= NoOfTrucksRequired :
    #         return
    #     elif ((3 - self.noOfTrucksInBranch(3)) >= NoOfTrucksRequired) :
    #         return
    #
    #     else:
    #         if self.noOfTrucksInBranch(2) < self.noOfTrucksInBranch(3) :
    #             noTrucksToMove = 3 - self.noOfTrucksInBranch(2) - NoOfTrucksRequired
    #             refPos = 3 - noTrucksToMove
    #             for p in self.moveTrucks( noTrucksToMove,2, 3): yield p
    #             return
    #         else:
    #             noTrucksToMove = NoOfTrucksRequired - self.noOfTrucksInBranch(3)
    #             refPos = 3 - noTrucksToMove
    #             for p in self.moveTrucks( noTrucksToMove,3, 3): yield p
    #             return

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
            return 5
        else:
            return 3

    def noSpacesinBranch(self, Branch) :
        return self.capacityOfBranch(Branch) - self.noOfTrucksInBranch(Branch)


    def getOtherBranch(self,fromBranch, destBranch):

        return 6 - fromBranch - destBranch  # as sum of 1 + 2 + 3 = 6, the formula follows

    def noOfTrucksToLeftFromEnd(self,branchNo, posfromend) :
        # counts from 0
        noOfTrucksToLeft = self.noOfTrucksInBranch(branchNo) - posfromend - 1
        return noOfTrucksToLeft

    def insertTruck(self, from_branch, destination_branch, refPos) :

        # for this to work there must be no more than 2 trucks to move from the dest branch

        # move trucks from toBranch to head
        no_trucks_to_move = self.noOfTrucksToLeftFromEnd(destination_branch, refPos) + 1

        if no_trucks_to_move == 0:
            for p in self.moveTrucks(1, from_branch, destination_branch): yield p
            return
        if no_trucks_to_move > 2:
            # move the excess trucks to another branch
            noTrucks1 = no_trucks_to_move - 2

            other_branch = self.getOtherBranch(from_branch, destination_branch)
            if self.noSpacesinBranch(other_branch == 0):
                for p in self.insertTruck(destination_branch, from_branch, 0): yield p
                no_trucks_to_move -= 1
            else:
                if self.noSpacesinBranch(other_branch < noTrucks1):
                    self.moveTrucks(self.noOfTrucksInBranch(from_branch), from_branch, other_branch)
                    # move trucks on from branch to other branch
                    temp = from_branch
                    from_branch = other_branch
                    other_branch = temp
                for p in self.moveTrucks(noTrucks1, destination_branch, other_branch): yield p

        for p in self.moveTrucks(min(no_trucks_to_move, 2), destination_branch, 4): yield p

        # move truck from fromBranch to head
        no_trucks_to_move = 1
        for p in self.moveTrucks(no_trucks_to_move, from_branch, 4): yield p

        # move trucks from head to toBranch \
        no_trucks_to_move1 = min(self.noOfTrucksInBranch(4),
                              self.capacityOfBranch(destination_branch) - self.noOfTrucksInBranch(destination_branch))
        for p in self.moveTrucks( no_trucks_to_move1, 4, destination_branch): yield p

        # there may be sometrucks left on branch 4. move them

        no_trucks_to_move2 = self.noOfTrucksInBranch(4)
        if (no_trucks_to_move2 != 0):
            freeBranch = 0
            for p in self.getFreeBranch(no_trucks_to_move2):
                i = 0
                if i == 0:
                    freeBranch = p
                else:
                    yield p

            for p in self.moveTrucks( no_trucks_to_move2, 4, freeBranch): yield p

    # def init_position_branch(self):
    #     # there are 14 positions in shunting pussle
    #     self.positions = [i for i in range(1, 8)] + [0 for i in range(8, 14)]
    #     branch1 = [1 for i in range(1, 6)]
    #     branch2 = [2 for i in range(1, 4)]
    #     branch3 = [3 for i in range(1, 4)]
    #     branchh = [4 for i in range(1, 4)]
    #     self.branches = branch1 +branch2 + branch3 + branchh
    #     # shuffle positions
    #     random.shuffle(self.positions)
    #     # create dict_from_lists
    #     self.position_branch_dict = self.dict_from_lists(self.positions, self.branches)

    mainLine = 4

    def moveTrucks(self, noTrucks, fromBranch,  destBranch):

        print(self.pegs)

        print ("move_trucks_one_by_one", noTrucks, fromBranch,  destBranch)

        yield ["move_trucks_one_by_one", noTrucks, fromBranch, destBranch, self.pegs]

        # fromBranch = 1
        # destBranch = 2
        # noTrucks = 3
        # take from fromBranch, put on 4
        if fromBranch != self.mainLine:
            for i in range(0, noTrucks):
                # print("self.pegs[fromBranch]",self.pegs[fromBranch-1])
                # print("self.pegs[mainline]",self.pegs[self.mainLine-1])
                # print ("self.pegs",self.pegs)
                self.pegs[self.mainLine-1].append(self.pegs[fromBranch-1].pop())
                yield self.pegs
        if destBranch != 4:
            for i in range(0, noTrucks):
                self.pegs[destBranch-1].append(self.pegs[self.mainLine-1].pop())
                yield self.pegs
        print (self.pegs)
        print("leave moveTrucksOneByOne", noTrucks, fromBranch, destBranch)

    def moveTrucksOneByOne(self, noTrucks, fromBranch, destBranch):

        print("moveTrucks", noTrucks, fromBranch, destBranch)
        print(self.pegs)

        yield ["move_trucks", noTrucks, fromBranch, destBranch, self.pegs]

        for i in range(0, noTrucks):
            if fromBranch != self.mainLine:
                self.pegs[self.mainLine-1].append(self.pegs[fromBranch-1].pop())
                yield self.pegs
            if destBranch != 4:
                self.pegs[destBranch-1].append(self.pegs[self.mainLine-1].pop())
                yield self.pegs

        print(self.pegs)
        print("leave moveTrucks", noTrucks, fromBranch, destBranch)
        


    def solvePuzzle1(self):
        yield self.pegs
        self.pegs[3].append(self.pegs[0].pop())
        yield self.pegs
        self.pegs[3].append(self.pegs[2].pop())
        yield self.pegs
        nopegs2 = self.pegs[2].count
        # print (pegs1)
        pegs1e = len(self.pegs[1])
        #print(pegs1e)
        for i in range(0, len(self.pegs[1])):
            #print(pegs1)
            #print(pegs1e)
            self.pegs[3].append(self.pegs[1].pop())
            yield self.pegs

#     def getPositionInBranchFromEnd(self, truckNo) :
#
#         branchNo = self.getBranchNo(truckNo)
#
#         position = StringUtils.indexOf(
#             StringUtils.leftPad(layout[1].toString(), 14, "0"),
#             truckNo.toString());
#         int
#         noTrucksInBranch = self.noOfTrucksInBranch(branchNo)
#         switch(position)
#         {
#             case
#         13:
#         case
#         12:
#         case
#         11:
#         case
#         10:
#         case
#         9: \
#             branchNo = 1;
#         return (noTrucksInBranch - (13 - position) - 1);
#         case
#         8:
#         case
#         7:
#         case
#         6:
#         return (noTrucksInBranch - (8 - position) - 1);
#
#     case
#     5:
#     case
#     4:
#     case
#     3:
#     return (noTrucksInBranch - (5 - position) - 1);
#
#
# case
# 2:
# case
# 1:
# case
# 0:
# return (noTrucksInBranch - (2 - position) - 1);
# }
# return position;
#
# }

    def truckInSiding(self, truckNo, branchNo):
        # print (self.pegs[branchNo - 1].count(truckNo))
        # print (self.pegs[branchNo - 1])
        # print (self.pegs)
        # print( self.pegs[branchNo - 1].count(truckNo)>0)
        return self.pegs[branchNo - 1].count(truckNo)>0


    def truckAtPositionFromEnd(self, truckNo, branchNo, position):
        # print (branchNo)
        # print( self.pegs[branchNo- 1].index(truckNo))
        return position == self.pegs[branchNo - 1].index(truckNo)+1

        # _branchNo = self.getBranchNo(truckNo)
        # _position = self.getPositionInBranchFromEnd(truckNo)
        # if ((branchNo == _branchNo) and (position == _position)):
        #     return True
        # else:
        #     return False

    def moveTruckToDesiredPosition(self, truckNo, destSiding):
        print("moveTruckToDesiredPosition", truckNo, destSiding)
        if self.truckInSiding(truckNo, destSiding):
            print("truckInSiding", truckNo, destSiding)

            # a) If Truck is in top siding but not nearest buffers, move to other siding
            # if truck 5 is in position 2, move to position 3 by putting another truck at buffers
            # If truck is in position 3 or more, move trucks to other siding
            # putting in position 3 if possible

            desiredPosition = 5 - truckNo

            if not self.truckAtPositionFromEnd(truckNo, destSiding, desiredPosition):
            #if not self.pegs[destSiding].index == desiredPosition:

                # move truck5 to another branch
                refPos = desiredPosition + 1

                a1=self.truckAtPositionFromEnd(truckNo, destSiding, 1)
                a2=self.truckAtPositionFromEnd(truckNo, destSiding, 2)
                a3=self.truckAtPositionFromEnd(truckNo, destSiding, 3)
                a4=self.truckAtPositionFromEnd(truckNo, destSiding, 4)
                a5=self.truckAtPositionFromEnd(truckNo, destSiding, 5)

                if self.truckAtPositionFromEnd(truckNo, destSiding, refPos):
                    fromBranch = self.getOccupiedBranch(destSiding)
                    self.insertTruck(fromBranch, destSiding, desiredPosition + 1)
                    # Myfunctions.getPositions());

                # check the position of the truck
                freeBranch = 0
                refPos = desiredPosition + 1
                rp = 0
                if self.truckAtPositionFromEnd(truckNo, destSiding, refPos):
                    # Myfunctions.getPositions())) {
                    rp = desiredPosition + 1

                refPos = desiredPosition + 1
                if self.truckAtPositionFromEnd(truckNo, destSiding, refPos + 1):
                    # Myfunctions.getPositions())) {
                    rp = desiredPosition + 2
                if rp > 0:
                    noTrucks = self.noOfTrucksToLeftFromEnd(destSiding, rp)
                    if (noTrucks > 1):
                        # we can't have more than one truck to left of truck to position
                        noTrucks1 = self.noOfTrucksToLeftFromEnd(destSiding, rp + 1)
                        # move the surplus trucks
                        freeBranch1 = 0
                        for p in self.getFreeBranch(noTrucks1):
                            freeBranch1 = next(p)
                            yield p
                        # Myfunctions.getPositions());
                        for p in self.moveTrucks(noTrucks1, destSiding,  freeBranch1): yield p

                    noTrucks = self.noOfTrucksToLeftFromEnd(destSiding, rp)
                    if (noTrucks == 1):
                        noTrucksToMove = 2
                        freeBranch = 0
                        for p in self.getFreeBranch(noTrucksToMove):
                            i = 0
                            if i == 0:
                                freeBranch = p
                            else:
                                yield p
                        # Myfunctions.getPositions());
                        for p in self.moveTrucksOneByOne( noTrucksToMove, destSiding, freeBranch): yield p

                    noTrucks = self.noOfTrucksToLeftFromEnd(destSiding, rp)
                    if (noTrucks == 0):
                        # can just move truck
                        noTrucksToMove = 1
                        freeBranch = 0
                        for p in self.getFreeBranch(noTrucksToMove):
                            i = 0
                            if i == 0:
                                freeBranch = p
                            else:
                                yield p
                        # Myfunctions.getPositions());
                        for p in self.moveTrucks(noTrucksToMove, destSiding,  freeBranch): yield p

                refPos = desiredPosition + 3

                if (self.truckAtPositionFromEnd(truckNo, destSiding, refPos) or
                        self.truckAtPositionFromEnd(truckNo, destSiding, refPos + 1) or
                        self.truckAtPositionFromEnd(truckNo, destSiding, refPos + 2)):
                    # , Myfunctions.getPositions())) {
                    # now we have to move the trucks to another siding
                    noTrucks = self.noOfTrucksToLeftFromEnd(destSiding, 2)
                    freeBranch = 0
                    for p in self.getFreeBranch(noTrucks):
                        i = 0
                        if i==0 :
                            freeBranch = p
                        else:
                            yield p
                    # Myfunctions.getPositions());
                    for p in self.moveTrucksOneByOne(noTrucks, destSiding, freeBranch): yield p

                    if (self.truckAtPositionFromEnd(truckNo, destSiding, refPos+2)):
                        # move truck to a free branch
                        freeBranch = 0
                        for p in self.getFreeBranch(noTrucks):
                            i = 0
                            if i == 0:
                                freeBranch = p
                            else:
                                yield p
                        for p in self.moveTrucks(1, destSiding, freeBranch): yield p
                        #insert the truck in the first position
                        for p in self.insertTruck(freeBranch, destSiding, 5 - truckNo): yield p
                    else:
                        # move truck to a free branch
                        freeBranch = 0
                        for p in self.getFreeBranch(noTrucks):
                            i = 0
                            if i == 0:
                                freeBranch = p
                            else:
                                yield p
                        for p in self.moveTrucks(1, destSiding, freeBranch): yield p
                        # now move the truck from the first position on the free branch to another branch
                        for p in self.insertTruck(freeBranch, destSiding, 5 - truckNo): yield p
                #print(list([p][-1]))



        if (not self.truckInSiding(truckNo, destSiding)):

            truckSiding = self.getBranchNo(truckNo)

            # b) If Truck 5 is nearest buffer of another siding
            # Ensure siding has one spare slot
            # Move a Truck to buffer
            # Ensure siding has one spare slot
            if self.truckAtPositionFromEnd(truckNo, truckSiding, 0):
                noTrucks = self.noOfTrucksToLeftFromEnd(truckSiding, 0)
                if (noTrucks > 0):
                    # better occupied branch excluding all trucks less than
                    # current truck
                    otherBranch = self.getOtherBranch(destSiding, truckSiding)

                    if self.noOfTrucksInBranch(otherBranch) == 0:
                        self.moveTrucks(min(2, noTrucks),truckSiding,  otherBranch)
                        # if truckno > 3 then the remaining trucks and the truck
                        # to position will not be able to fit on branch 4
                        if (truckNo >= 3):
                            for p in self.moveTrucks(truckSiding, 1, otherBranch): yield p
                            truckSiding = self.getBranchNo(truckNo)
                    elif (self.noOfTrucksInBranch(otherBranch) == 1):
                        for p in self.moveTrucks(min(2, noTrucks), truckSiding,  otherBranch): yield p
                    elif (self.noOfTrucksInBranch(otherBranch) == 2):
                        for p in self.moveTrucks(1, truckSiding,  otherBranch): yield p
                        if (noTrucks == 2):
                            for p in self.moveTrucks( 1, truckSiding, destSiding): yield p
                        for p in self.moveTrucks( noTrucks, truckSiding, destSiding): yield p
                        for p in self.moveTrucks(1, truckSiding,  4): yield p
                        self.noTrucks1 = min(self.noOfTrucksToLeftFromEnd(destSiding, 5 - (truckNo + 1)), 2)
                        for p in self.moveTrucks(self.noTrucks1, 1, 4): yield p
                        for p in self.moveTrucks(4, self.noOfTrucksInBranch(4),  truckSiding): yield p

                refPos = 5 - truckNo;
                for p in self.insertTruck(truckSiding, destSiding, refPos): yield p

            elif self.truckAtPositionFromEnd(truckNo, truckSiding, 1):
                noTrucks = self.noOfTrucksToLeftFromEnd(truckSiding, 1)
                if noTrucks > 0:
                    # better occupied branch excluding all trucks less than
                    # current truck
                    other_branch = self.getOtherBranch(destSiding, truckSiding)
                    if self.noOfTrucksInBranch(other_branch) <= 2:
                        for p in self.moveTrucks(1, truckSiding, other_branch): yield p
                    else:
                        for p in self.insertTruck(other_branch, truckSiding, 1, ): yield p

                for p in self.insertTruck(truckSiding, destSiding, 5 - truckNo): yield p
            else:
                # check the position of the truck

                freeBranch = 0
                refPos = 2
                if (self.truckAtPositionFromEnd(truckNo, truckSiding, refPos)):
                    refPos1 = 5 - truckNo;  # because of the numbering
                    for p in self.insertTruck(truckSiding, destSiding, refPos1): yield p

        print("leave moveTruckToDesiredPosition", truckNo, destSiding)

if __name__ == '__main__':
    print("Hello")
    import sys;sys.path.append(r'C:\Users\bill\.p2\pool\plugins\org.python.pydev.core_7.2.1.201904261721\pysrc')
    import pydevd;pydevd.settrace()
    ts = TimeSaver()
    ts.solvePuzzle()
    
    #assert ingle.positions.count(1) == 1
    #assert ingle.branches.count(1) == 5
