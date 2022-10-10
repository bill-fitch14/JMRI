import jarray
import jmri
import java.beans
#import jmri.jmrit.automat.AbstractAutomaton as aa
import sys, os
#sys.path.append('Z:\\Shunting puzzle\\Python\\an inglenook puzzle')
my_path_to_classes = jmri.util.FileUtil.getExternalFilename('program:jython/ShuntingPuzzles/Inglenook')
sys.path.append(my_path_to_classes) # add the classes to your path

class Move_train(jmri.jmrit.automat.AbstractAutomaton) :

    def __init__(self):
    
        #speeds
        self.stop = 0
        self.slow = 3
        self.medium = 5
        self.fast = 7
        
        self.initialmove = True
        print("Inside init(self)xx1")
        try:
            list = sensors.getSystemNameList()
            print list
        except:
            print("!!  sensors not connected")

        try:
            print ("trying to set up sensors")
            # self.sensor1 = sensors.provideSensor("MS+N259E7;-N259E7")
            # print ("This is an success message! s1 set up")
            # self.sensor2 = sensors.provideSensor("MS+N259E6;-N259E6")
            # print ("This is an success message! s2 set up")
            # self.sensor3 = sensors.provideSensor("MS+N259E5;-N259E5")
            # print ("This is an success message! s3 set up")
            # self.sensor4 = sensors.provideSensor("MS+N259E8;-N259E8")
            # print ("This is an success message! s4 set up")
            for s in sensors:
                if s.getUserName() == "InglenookSensor1" : self.sensor1 = s
                if s.getUserName() == "InglenookSensor2" : self.sensor2 = s
                if s.getUserName() == "InglenookSensor3" : self.sensor3 = s
                if s.getUserName() == "InglenookSensor4" : self.sensor4 = s
            if self.sensor1 != None and self.sensor2 != None and self.sensor3 != None and self.sensor4 != None:
                print ("This is an success message! Stopping sensors s1-s4 set up")
            else
                print ("this is a failure message! Stopping sensors s1-s4 not set up)
        except:
            print ("this is a failure message! Stopping sensors s1-s4 not set up)
         
         # get loco address. For long address change "False" to "True"
        try:
            self.throttle = self.getThrottle(3, False)  # short address 3
            print("throttle set up")
        except:
            print("throttle not set up")
        
        print ("finished init")
        print(self.__dict__)

        # self.sensor1 = DebounceSensor()  # create one of these
        # self.sensor1.init('+N259E5','-N256E5', 0.5, 3) # invoke this for the sensor pair

        # self.sensor2 = DebounceSensor()  # create one of these
        # self.sensor2.init('NS775', 'ISNS775', 0.5, 3)  # invoke this for the sensor pair

        # self.sensor3 = DebounceSensor()  # create one of these
        # self.sensor3.init('NS775', 'ISNS775', 0.5, 3)  # invoke this for the sensor pair

        # self.sensor4 = DebounceSensor()  # create one of these
        # self.sensor4.init('NS775', 'ISNS775', 0.5, 3)  # invoke this for the sensor pair

        

    def decide_what_to_do(self, instructions):
        print("inside what to do")
        print instructions
        if instructions[0] == "moveTrucksOneByOne":
            #self.moveTrucksOneByOne(instructions[1],instructions[2],instructions[3],instructions[4])
            pass
        elif instructions[0] == "move_trucks":
            print(" about to moveTrucks",instructions[1], instructions[2], instructions[3], instructions[4])
            self.moveTrucks(instructions[1], instructions[2], instructions[3], instructions[4])
            pass
        else:
            pass
            


    def noTrucksOnStack(self, pegs, branch_no):
        noTrucks = len(pegs[branch_no - 1])
        return noTrucks


    def disconnect(Branch):
        self.throttle.setSpeedSetting(0)
        self.pause(1) # pause for 1 sec
        #magnets so dont need to do anything else
        
    def moveTrucksOneByOne(self, noTrucks, fromBranch, destBranch, pegs):
        for i in range[0:noTrucks]:
            if fromBranch != 4:
                tmp = self.mypop(fromBranch)
                self.mypush(4, temp);
                #self.drawStacks()

            if destBranch != 4:
                temp = self.mypop(4)
                self.mypush(destBranch, temp)
                #self.drawStacks()

    def moveEngineToBranch(self,fromBranch, toBranch, trucksToMove):
        print("In moveEngineToBranch")
        #set direction
        self.setDirection(fromBranch, toBranch)
        #set Speed
        self.setSpeed(self.slow)
        #set sensor
        sensor = self.setSensor(toBranch)
        
        #this is wrong
        noTrucksToCount = trucksToMove
        
        #wait for sensor to trigger
        if toBranch == 4:
            self.countTrucks(noTrucksToCount, sensor)
        else:
            self.countTrucks(0, sensor)
            
    # def moveToDisconnectTrucks(self, noTrucksInitially,
                               # noTrucksToMove, fromBranch, toBranch ):
                               
    def moveToDisconnectTrucks(self, noTrucksInitially,
                               noTrucksToMove, Branch):
        # deed todetermine the direction to pick up or remove trucks from engine at from branch
        
        noTrucksToAdd = noTrucksInitially - noTrucksToMove
        if noTrucksToAdd > 0:
            setDirection(Branch, 4)
        else:
            setDirection(4, Branch)
        noTrucksToCount = abs(noTrucksToAdd)            
            
        sensor = self.setSensor(Branch)

        self.countTrucks(noTrucksToCount, sensor)

    def swapRouteSameDirectionTravelling(self, fromBranch, toBranch):
        self.setDirection(fromBranch, toBranch)

    def swapRouteOppDirectionTravelling(self, fromBranch, toBranch):
        self.setDirection(fromBranch, toBranch)

    def setDirection(self, fromBranch, toBranch):
        if fromBranch == 4:
            # set loco to forward
            print("Set Loco Forward")
            self.throttle.setIsForward(True)
        else:
            # set loco to reverse
            print("Set Loco Forward")
            self.throttle.setIsForward(False)

    def setSensor(self, branch):
        if branch == 1:
            sensor = self.sensor1
        if branch == 2:
            sensor = self.sensor2
        if branch == 3:
            sensor = self.sensor3
        if branch == 4:
            sensor = self.sensor4
        return sensor
        
    def setSpeed(self, speed):
 
         self.throttle.setSpeedSetting(speed)    
            
    def countTrucks(self, noTrucksToCount, sensor):
        # delay so that we are on a truck then count the number of off events
        
        while 1:
            self.waitChange([sensor])
            if sensor.on_click:
                count+= 1
                if count == noTrucksToCount:
                    break
    
    def moveTrucks_old(self, noTruckstoMove, fromBranch, destBranch, pegs):
        
        noTrucksOnStack4 = self.noTrucksOnStack(pegs, 4)
        if self.initialmove :
            self.swapRouteSameDirectionTravelling(4, fromBranch)
            self.moveEngineToBranch(4, fromBranch) # move
            # and connect with existing trucks if any
            self.pause(1)
            self.connectTrucks(fromBranch)
            self.initialmove = False

        noTrucksInitially = noTrucksOnStack4
        #noTrucksToMove = noTrucks
        self.moveToDisconnectTrucks(noTrucksInitially,
                               noTrucksToMove, fromBranch)
        #move to right place todisconnect
        #move fromonelinked list to another
        # self.disconnectTrucks(noTrucksOnStack4,
                         # noTrucksToMove, fromBranch, destBranch)
        
        self.disconnect(fromBranch) # disconnect

        self.moveEngineToBranch4(fromBranch, 4, TrucksToMove)
       
        self.moveEngineToBranch(4, destBranch, TrucksToMove)
 
        #self.connectTrucksToTrain4(destBranch)
        self.swapRouteOppDirectionTravelling(4, fromBranch)
        
    def moveTrucks(self, noTrucksInitially, noTrucksToMove, fromBranch, destBranch):
        print("in movetrucks")
        print("Movetrucks",noTrucksInitially, noTrucksToMove, fromBranch, destBranch)
        if fromBranch != 4:
            self.moveToDisconnectTrucks(noTrucksInitially, noTrucksToMove, fromBranch)  
            self.disconnect(fromBranch) # disconnect
            self.moveEngineToBranch(fromBranch, destBranch, noTrucksToMove)
            self.swapDirection()
        else:
            self.moveEngineToBranch(fromBranch, destBranch, noTrucksToMove)
        return noTrucksInitially + noTrucksToMove 
        
    def moveTrucksAllAtOnce(self, noTrucksInitially, startsInBranch4, fromBranch, destBranch, noTruckstoMove):
        if startsInBranch4 :
            noTrucksOnStack4 = self.noTrucksOnStack(pegs, 4)
            self.moveTrucks(noTrucksOnStack4,4,fromBranch)
            self.initialmove = False
            noTrucksInitially = noTrucksOnStack4
        
        if fromBranch != 4:
            noTrucks = self.moveTrucks(noTrucksInitially, noTruckstoMove, fromBranch, 4)
        if destBranch != 4:       
            noTrucks = self.moveTrucks(noTrucks, noTruckstoMove, 4, destBranch)
        
        return noTrucks
            
    def moveTrucksOneByOne(self, noTrucksInitially, startsInBranch4, fromBranch, destBranch, noTrucksToMove, pegs):    
        
        if startsInBranch4 == True:
            noTrucksOnStack4 = self.noTrucksOnStack(pegs, 4)
            self.moveEngineToBranch(4, fromBranch, noTrucksOnStack4)
            connectTrucks(fromBranch)
			
		
        for i in Range(noTrucksToMove):
            noTrucksToMoveInOneGo = 1
            if fromBranch != 4:
                noTrucks = self.moveTrucks(noTrucksInitially, noTrucksToMoveInOneGo, fromBranch, 4)
            if destBranch != 4:      
                noTrucks = self.moveTrucks(noTrucks, noTrucksToMoveInOneGo, 4, destBranch)
        
        return noTrucks


    #def moveTrucksOneByOne(startBranch, fromBranch, refPos, noTrucks, destBranch) 
    def moveTrucksOneByOne_old(self, startBranch, fromBranch, destBranch, noTrucks):
        
        # engine starts in fromBranch
        # picks uptruck in fromBranch and deposits in destBranch.
        # it then returns to dest branch if another truck is to be picked up

        init = True
        for i in Range(noTrucks):
            noTrucksOnStack4 = self.noTrucksOnStack(pegs, 4)
            if fromBranch != 4:
                print("Hi")
                
            if fromBranch != 4:
                print("Hi")
                if startBranch == 4 and init == true:
                    moveEngineToBranch(4, fromBranch, 1) # move engine so engine is at stop
                    connectTrucks(fromBranch)
                init = False
                #swapRouteOppDirectionTravelling(fromBranch, 4)
                #self.swapDirection()

                noTrucksInitially = noTrucksOnStack4
                noTrucksToMove = 1 # if noTruckstomove is +ve then picking up a truck

                moveToDisconnectTrucks(noTrucksInitially,
                        noTrucksToMove, fromBranch, 4) #move engine back so can disconnect

                disconnectTrucks(noTrucksOnStack4, noTrucksToMove, fromBranch, i) 
                disconnectSignal(fromBranch)
                noOfTrucks = noTrucksInitially + noTrucksToMove
                moveEngineToBranch(fromBranch, 4, )

            if destBranch != 4:

                swapDirectionTravelling(4, destBranch)

                moveEngineToBranch(4, destBranch)
                connectTrucks(destBranch)
                # we have picked a truck up
                noTrucksInitially = noTrucksOnStack4 + 1 

                noTrucksToMove = -1  # deposit a truck

                if noTrucksToMove>0: #remove truck
                    swapRouteOppDirectionTravelling(destBranch, 4)
                    moveToDisconnectTrucks(noTrucksInitially,
                            noTrucksToMove, destBranch, 4)
                else:
                    moveToDisconnectTrucks(noTrucksInitially,
                            noTrucksToMove, 4, destBranch)	

                disconnectTrucks(noTrucksInitially,
                        noTrucksToMove, destBranch, i * 10)
                disconnectSignal(destBranch)
                if noTrucksToMove<0 : #remove truck
                    swapRouteOppDirectionTravelling(destBranch, 4)
                    swapRouteSameDirectionTravelling(destBranch, 4)  # should not do anything, but does

                pause(0) # pause for 1 sec
                if i != noTrucks - 1:
                    moveEngineToBranch(destBranch, 4)
                    #swapRouteOppDirectionTravelling(4, destBranch)
                    self.swapDirection()
                    
#print (__name__)
if __name__ == "__builtin__":
    def generate_instructions():
        #yield ["move_trucks", noTrucks, fromBranch, destBranch, self.pegs]
        # should be
        #moveTrucks(self, noTrucksInitially, noTruckstoMove, fromBranch, destBranch):
        yield ["move_trucks", 2, 1, 4, 1]
    
    t = Move_train()
    print(Move_train().__dict__)
    
    #train.init()
    print("in test1")       
    instructions = generate_instructions()
    print("in test2")   

    for position in instructions:
        if type(position[0]) is str:
            #this is a command for the train
            print("in test3")   
            t.decide_what_to_do(position)
    print("Hi")