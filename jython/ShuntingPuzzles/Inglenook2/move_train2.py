import jarray
import jmri
import java.beans
#import jmri.jmrit.automat.AbstractAutomaton as aa
import sys, os
from javax.swing import JFrame, JButton, JOptionPane
from inglenook import Inglenook
# move_train import move_train
#from move_train2 import Move_train 
import doctest
import time
import pyj2d as pygame
from pyj2d.locals import *
import threading

sys.path.append('Z:\\Config Profiles\\jython\\an inglenook puzzle')

throttle = None
stop_program = False


class Move_train(jmri.jmrit.automat.AbstractAutomaton) :

    # def __init__(self,instructions):
        # self.instructions = instructions
        
    # def run_generator(self,instruction)
        # #instruction = self.instructions.next()
        # self.decide_what_to_do(instruction)
        
    tender = True
    
    def init(self):
        global throttle
        #speeds
        self.stop = 0
        self.slow = 0.1
        self.decouple = 0.2
        self.medium = 0.5
        self.couple = 0.6
        self.fast = 0.7
        
        #sensor States
        self.sensorOn = 1
        self.sensorOff = 0
        
        self.initialmove = True
        print("Inside init(self)xx")
        
        list = sensors.getSystemNameList()
        print list
        list = turnouts.getSystemNameList()
        print list
            
        try:
            print ("trying to set up sensors")
            
            #self.sensor1 = sensors.provideSensor("MS+N259E5;-N259E5")
            self.sensor1 = sensors.provideSensor("sensor1")
            print ("This is an success message! s1 set up")
            #self.sensor2 = sensors.provideSensor("MS+N259E6;-N259E6")
            self.sensor2 = sensors.provideSensor("sensor2")
            print ("This is an success message! s2 set up")
            #self.sensor = sensors.provideSensor("MS+N259E7;-N259E7")
            self.sensor3 = sensors.provideSensor("sensor3")
            print ("This is an success message! s3 set up")
            #self.sensor4 = sensors.provideSensor("MS+N259E8;-N259E8")
            self.sensor4 = sensors.provideSensor("sensor4")
            print ("This is an success message! s4 set up")
            print "in move_train2.py"
        except:
            print ("sensors not set!")
            
        try:
            print ("trying to set up points")
            self.point1 = turnouts.provideTurnout("MT+N0E10;-N0E10")
            self.point2 = turnouts.provideTurnout("MT+N0E11;-N0E11")
            print ("set up points")
        except:
            print ("points not set!")
         
        # get loco address. For long address change "False" to "True"
        try:
            print("throttle set up2")
            throttle = self.getThrottle(3, False)  # short address 3
            #throttle = self.throttle
            print("throttle set up3")
            print throttle
        except:
            print("throttle not set up")
        
        print ("finished init")
        print(self.__dict__)
        print(dir())
    
    def decide_what_to_do_first(self):
        #set up the trucks 5 in branch 3 and 3 in branch 2, and return to branch 4
        # self.noTrucksOnTrain = 0
        
        print("decide_what_to_do_first")

        self.noTrucksOnTrain = 0
        self.initialBranch = 4
        self.noTrucksToMoveFromPreviousStep = 0
        print ("self.noTrucksOnTrain:" + str(self.noTrucksOnTrain))
        print ("self.initialBranch:" + str(self.initialBranch))
        # instruction_first = [generate_first_instructions]
        # self.noTrucksOnTrain = self.decide_what_to_do(instruction_first,self.noTrucksOnTrain)
        print("end decide_what_to_do_first")
    
    def generate_first_instructions(self):
        # the move trucks instruction is shown commented out, so we can see what the yield does
        #moveTrucks(self, noTrucksOnTrain, noTruckstoMove, fromBranch, destBranch):
        
        #we move from branch 4 to branch 3 depositing all 5 trucks

        
        pass
        
    def decide_what_to_do(self, instructions):
    
        # decide_what_to_do uses the instructions and also uses two variables
        #  * noTrucksOnTrain
        #  * initialBranch
    
    
        print("decide_what_to_do")
        print instructions
        if instructions[0] == "move_trucks_one_by_one":
            #the argumants in inglenook are yield ["move_trucks_one_by_one", noTrucks, fromBranch, destBranch, self.pegs]
            #the arguments in this file are moveTrucksOneByOne(self, noTrucksOnTrain, startsInBranch4, fromBranch, destBranch, noTrucksToMove, pegs)
            print (">>decidewhattodo, move_trucks_one_by_one" )
            print ("instructions[0]:" + str(instructions[0]))
            print ("instructions[1]:" + str(instructions[1]))
            print ("instructions[2]:" + str(instructions[2]))
            print ("instructions[3]:" + str(instructions[3]))
            print ("instructions[4]:" + str(instructions[4]))
            print ("noTrucksOnTrain " + str(self.noTrucksOnTrain))
            print ("initialBranch " + str(self.initialBranch))
            
            self.moveTrucksOneByOne( instructions[1],instructions[2],instructions[3],instructions[4])
            pass
        elif instructions[0] == "move_trucks":
            print(" about to moveTrucks",instructions[1], instructions[2], instructions[3], instructions[4])
            self.moveTrucks(instructions[1], instructions[2], instructions[3])
            pass
        else:
            print("!!!!!!!!!unrecognised instruction " & instructions[0])
            pass
        print("end decide_what_to_do")
        #return noTrucksOnTrain
            
    def startFromBranch4(self, destBranch, pegs):
        
        self.noTrucksOnTrain =  self.noTrucksOnStack(pegs, 4)
        noTrucksToMove = 0
        fromBranch = 4 
        destBranch = destBranch
        self.moveEngineToBranch(noTrucksOnTrain, noTrucksToMove, fromBranch, destBranch)
        connectTrucks(fromBranch)
                
    def moveTrucksOneByOne(self, noTrucksToMove, fromBranch, destBranch,  pegs):    
        
        #self.noTrucksOnTrain and self.initialBranch are global variables that are used in this routine
        
        # moveTrucks emulates the following code in inglenook, however in addition to that code we must 
        # check whether we are at the correct branch before popping
        
        # for i in range(0, noTrucks):
            # if fromBranch != self.mainLine:
                # pop from fromBranch push to mainLine
            # if destBranch != 4:
                # pop from fromBranch push to mainLine
                
        # we do this with the following pseudocode
        # if initialbranch != fromBranch
            # move to fromBranch. We take the current number of trucks on train
            # do this in 2 steps
            # if initialbranch != mainLine
                # move from initialBranch to mainLine
            # if frombranch != mainLine
                # move from mainLine to fromBranch
        # repeat for each truck in trucksToMove
            # if frombranch != mainLine
                # take 1 truck from frombranch to mainLine 
            # if destBranch != mainLine
                # take 1 truck from mainLine to destBranch
            # deposit 1 truck at destBranch
        
        print (">>moveTrucksOneByOne " )
        print ("self.noTrucksOnTrain:" + str(self.noTrucksOnTrain))
        print ("self.initialBranch:" + str(self.initialBranch))
        print ("fromBranch:" + str(fromBranch))
        print ("destBranch:" + str(destBranch))
        print ("noTrucksToMove:" + str(noTrucksToMove))
        
        if self.initialBranch != fromBranch:
            print ("!!!!!!!!!!self.initialBranch != fromBranch:" + str(noTrucksToMove))
            # noTrucksOnStack4 = self.noTrucksOnStack(pegs, 4)
            self.moveTrucks(self.noTrucksOnTrain, self.initialBranch, fromBranch)
            #connectTrucks(fromBranch)
            print ("!!!!!!!!!!moveTrucksOneByOne: self.initialBranch != fromBranch:" + str(noTrucksToMove))
		
        print ("!!!!!!!!!!!moveTrucksOneByOne: stage2 " + str(noTrucksToMove))
        for i in Range(noTrucksToMove):
            noTrucksToMoveInOneGo = 1
            if fromBranch != 4:
                print ("!!!!!!!!!!!moveTrucksOneByOne: stage2a " + str(noTrucksToMoveInOneGo))
                self.moveTrucks(noTrucksToMoveInOneGo+1, fromBranch, 4) #need to count 2 trucks 
            if destBranch != 4: 
                print ("!!!!!!!!!!!moveTrucksOneByOne: stage2b " + str(noTrucksToMoveInOneGo))
                self.moveTrucks(noTrucksToMoveInOneGo, 4, destBranch)
        
        self.noTrucksOnTrain = noTrucks
        self.initialBranch = fromBranch       
            
    def moveTrucks(self, noTrucksToMove, fromBranch, destBranch):
    
        #self.noTrucksOnTrain and self.initialBranch are global variables that are used in this routine
        # self.noTrucksToMoveFromPreviousStep is another global ised to reduce unnecessary movement
        # we do the final move to disconnect in the next step
        
        # moveTrucks emulates the following code in inglenook, however in addition to that code we must 
        # check whether we are at the correct branch before popping
        
        # if fromBranch != self.mainLine:
            # for i in range(0, noTrucks):
                # pop from fromBranch push to mainLine
        # if destBranch != 4:
            # for i in range(0, noTrucks):
                # pop from fromBranch push to mainLine
                
        # we do this with the following pseudocode
        
        # if initialbranch != fromBranch
            # move to fromBranch. We take the current number of trucks on train
            # do this in 2 steps
            # if initialbranch != mainLine
                # move from initialBranch to mainLine
            # if frombranch != mainLine
                # move from mainLine to fromBranch
        # if frombranch != mainLine
            # take trucksToMove from frombranch to mainLine
        # if destBranch != mainLine
            # take trucksToMove from mainLine to destBranch
        # deposit trucksToMove at destBranch
            
        # note mainLine is siding 4
        
        # however we modify the above a bit by doiny the last stage of depositing in the first stage 
        # this is to avoid possible extra moves 
        # to enable this we need another variable noTrucksToMoveFromPreviousStep
        
        
        print (">>moveTrucks " )
        print ("self.noTrucksOnTrain:" + str(self.noTrucksOnTrain))
        print ("self.initialBranch:" + str(self.initialBranch))
        print ("self.noTrucksToMoveFromPreviousStep"+ str(self.noTrucksToMoveFromPreviousStep))
        print ("fromBranch:" + str(fromBranch))
        print ("destBranch:" + str(destBranch))
        print ("noTrucksToMove:" + str(noTrucksToMove))
        print("in movetrucks")
        #print("Movetrucks",str(noTrucksOnTrain), noTrucksToMove, fromBranch, destBranch)
        
        if self.initialBranch == fromBranch:
            noTrucksToMove = self.noTrucksToMoveFromPreviousStep - noTrucksToMove
            noTrucksToMoveFromPreviousStep = 0
            # now move and disconnect
        
        if self.initialBranch != fromBranch:
            print("self.initialBranch != fromBranch")
            self.moveToDisconnectPosition(self.noTrucksOnTrain, self.noTrucksToMoveFromPreviousStep, destBranch)
            self.decouple()
            noTrucksToMoveFromPreviousStep = 0
            # move to fromBranch. We take the current number of trucks on train. i.e. 0 extra trucks
            if self.initialBranch != 4:
                # move from initialBranch to mainLine
                self.moveToBranch(self.noTrucksOnTrain, 0, 4)
            if fromBranch != 4:
                self.moveToBranch(self.noTrucksOnTrain, 0, fromBranch)
            #now move and disconnect

            
            print ("!!!!!!!!!!moveTrucksOneByOne: self.initialBranch != fromBranch:" + str(noTrucksToMove))           
             
        if fromBranch != 4:
            print("in movetrucks fromBranch")
            # disconnect 
            self.moveToDisconnectPosition(self.noTrucksOnTrain, noTrucksToMove, destBranch)
            self.decouple()
            # take trucksToMove from frombranch to mainLine
            self.moveToBranch(self.noTrucksOnTrain, noTrucksToMove, 4)
            
        if destBranch != 4:
            print("in movetrucks destBranch")
            self.moveToBranch(self.noTrucksOnTrain, noTrucksToMove, destBranch)
            #self.moveToDisconnectPosition(self.noTrucksOnTrain, noTrucksToMove, destBranch)
            
        self.couple()    
        # note: we do not disconnect here because if we need to pick up in the same branch we do
        # not disconnect, hence we do the disconnect in the next move, if self.initialBranch != fromBranch
            
        # set the two global variables
        self.noTrucksOnTrain = noTrucksOnTrain + noTrucksToMoveFromPreviousStep
        self.initialBranch = fromBranch
        self.noTrucksToMoveFromPreviousStep = noTrucksToMove
        
       # we are now ready to do the final deposit in the next step

    def moveEngineToBranch(self,fromBranch, toBranch, trucksToMove):
        print("In moveEngineToBranch")
        #set direction
        self.setDirection(fromBranch, toBranch)
        self.setPoints(fromBranch, toBranch)
        self.waitMsec(2000)
        #set Speed
        self.setSpeed(self.slow)
        #set sensor
        sensor = self.setSensor(toBranch)
        
        #this is wrong
        noTrucksToCount = trucksToMove
        
        #wait for sensor to trigger
        self.countTrucksAndPosition(noTrucksToCount, sensor, "INACTIVE")
        self.setSpeed(self.stop)
        self.waitMsec(1000)
        
        #go on for a bit
        self.setSpeed(self.slow)
        self.waitMsec(500)
        self.setSpeed(self.stop)
        
        #decouple
        self.decouple()
        
    # def moveToDisconnectTrucks(self, noTrucksOnTrain,
                               # noTrucksToMove, fromBranch, toBranch ):
    def couple():
        self.setDirection(fromBranch, toBranch)
        self.setSpeed(self.couple)
        timeCouple = 500
        self.waitMsec(timeCouple)
        self.setSpeed(self.stop)
        self.setDirection(toBranch, fromBranch)
        self.setSpeed(self.slow)
        timeReturn = timeCouple * self.slow / self.couple
        self.waitMsec(timeReturn)
        self.setSpeed(self.stop)

    
    def decouple(fromBeanch, toBranch, sensor):
        self.setSpeed(self.stop)
        
        #whiz forward
        self.setDirection(fromBranch, toBranch)
        self.setSpeed(self.decouple)
        #self.waitMsec(500)
        waitChangeActive(sensor)    # sets speed 0
        self.waitMsec(100)
        
        #whiz back
        self.setDirection(toBranch, fromBranch)
        self.setSpeed(self.decouple)
        #self.waitMsec(1000)
        waitChangeInactive(sensor)  # sets speed 0
        self.waitMsec(100)
        
        #whiz forward again
        self.setDirection(fromBranch, toBranch)
        self.setSpeed(self.decouple)
        #self.waitMsec(500)
        waitChangeActive(sensor)    # sets speed 0
        self.waitMsec(100)
        
    def waitChangeSensorActive(sensor):
        #waitChangeSensor(sensor,self.sensorOn)
        while 1:
            self.waitChange([sensor])
            got_state = sensor.getKnownState()  
            if got_state == ACTIVE:
                self.setSpeed(0)
                #self.waitMsec(1000)             
                break

    def waitChangeSensorInactive(sensor):
        #waitChangeSensor(sensor,self.sensorOff)
        while 1:
            self.waitChange([sensor])
            got_state = sensor.getKnownState()  
            if got_state == INACTIVE:
                self.setSpeed(0)
                #self.waitMsec(1000)             
                break
    
    def waitChangeSensor(sensor, required_sensor_state):
        global throttle
        self.changeDirection()        
        self.setSpeed(self.slow)
        while 1:
            self.waitChange([sensor])
            got_state = sensor.getKnownState()
            print( ">> moveBackToSensor " + self.stateName(got_state) );   
            if required_sensor_state == self.sensorOn:
                print( ">> moveBackToSensor" + " sensor state on " + self.stateName(got_state) ); 
                if got_state == ACTIVE:
                    self.setSpeed(0)
                    #self.waitMsec(1000)             
                    break
                else:
                    print( ">> moveBackToSensor" + " req_sensor_state on " + self.stateName(got_state) );       
                    pass
            elif required_sensor_state == self.sensorOff:
                print( ">> moveBackToSensor" + " sensor state off" );
                if got_state == INACTIVE:
                    self.setSpeed(0)
                    #self.waitMsec(1000)
                    break
                else:
                    print( ">> moveBackToSensor" + " req_sensor_state off " + self.stateName(got_state) ); 
                    pass
            else:
                pass
        
    def moveToBranch(self, noTrucksOnTrain, noTrucksToMove, destBranch):
        # move the train to destbranch without any coupling or decoupling
        # we have already checked that the branch we are in is not destBranch
        if destBranch != 4:
            self.setDirection(4,destBranch)
            noToCount = 0
            self.countTrucksAndPosition(NoTrucksToMove, sensor, "ACTIVE") 
            self.setSpeed(self.stop)
        else:
            self.setDirection(destBranch,4)
            # going towards head count nuber of times becomes inactive
            if self.tender == True:
                extra = 2  # for engine and tender count
            else:
                extra = 1  # for engine count)
            self.countTrucksAndPosition(NoTrucksToMove, sensor, "INACTIVE") 
            self.setSpeed(self.stop)
       
    def moveToDisconnectPosition(self, noTrucksOnTrain, noTrucksToMove, destBranch):
    
        #self.moveToDisconnectPosition(self.noTrucksOnTrain, noTrucksToMoveFromPreviousStep, destBranch)
        
        # we have already moved the train to the branch and coupled the train
        # this routine moves the train to the new decoupling position
        print( "moveToDisconnectTrucks: destBranch = " )
        print( destBranch)
        
        #dest branch is never 4
        #self.setDirection(4, destBranch)
        self.setPoints(4,destBranch)
        
        sensor = self.setSensor(destBranch)
        self.setSpeed(self.slow)
        
        # need to determine the direction to pick up or remove trucks from engine at from branch
        
        noTrucksToAdd = noTrucksToMove 
        noTrucksToCount = abs(noTrucksToAdd)
        print(">>moveToDisconnectTrucks: noTrucksToAdd " + str(noTrucksToAdd) + " noTrucksToCount " + str(noTrucksToCount))
        
        #Assuming we are connected and need to pick up or drop off and return to destBranch
        if noTrucksToAdd >= 0:
            # picking up trucks
            print(">>moveToDisconnectTrucks: picking up Trucks");
            self.setDirection(destBranch,4)
            # print(">>moveToDisconnectTrucks: picking up trucks");
            self.countTrucksActive(noTrucksToCount, sensor)   # counts from 0
            self.setSpeed(self.stop)
            # #need to check that have connected
            #change direction
            print(">>moveToDisconnectTrucks: moving back to Siding 4");
            self.setDirection(4, destBranch)
            noTrucksToCount = noTrucksOnTrain + NoTrucksToMove
            sensor = self.setSensor(4)
            self.countTrucksInactive(noTrucksToCount, sensor)   # counts from 1
            self.setSpeed(self.stop)
            self.moveToDisconnectPosition2(sensor) 
            print(">>moveToDisconnectTrucks: picked up trucks");
        else:
            #dropping off trucks
            if noTrucksToCount > noTrucksOnTrain:
                print("!!!!>>moveToDisconnectTrucks: dropping off trucks: error not enough trucks")
            print(">>moveToDisconnectTrucks: dropping off " + str(noTrucksToCount) + " trucks");
            self.setDirection(4, Branch)
            self.countTrucksInactive(noTrucksToCount, sensor)   # counts from 0
            self.setSpeed(self.stop)
            #need to check that have connected
            print("DONE1");
            print(">>moveToDisconnectTrucks: dropped off trucks");
            # self.setDirection(Branch, 4)
            sensor = self.setSensor(destBranch)
            self.moveToDisconnectPosition2(sensor) 
            
    # def moveToDisconnectPosition2(self, sensor):
        # return
        # if sensor == self.sensor1:
            # self.moveBackToSensor(sensor, self.sensorOff)
        # elif sensor == self.sensor2:
            # self.moveBackToSensor(sensor, self.sensorOn)
        # elif sensor == self.sensor3:
            # self.moveBackToSensor(sensor, self.sensorOn)
            # #need to move a little more
        # else:
            # pass  # sensor 4 does not need positioning  

    # def moveBackToSensor(self, sensor, required_sensor_state):
        # global throttle
        # self.changeDirection()        
        # self.setSpeed(self.slow)
        # while 1:
            # self.waitChange([sensor])
            # got_state = sensor.getKnownState()
            # print( ">> moveBackToSensor " + self.stateName(got_state) );   
            # if required_sensor_state == self.sensorOn:
                # print( ">> moveBackToSensor" + " sensor state on " + self.stateName(got_state) ); 
                # if got_state == ACTIVE:
                    # self.setSpeed(0)
                    # #self.waitMsec(1000)             
                    # break
                # else:
                    # print( ">> moveBackToSensor" + " req_sensor_state on " + self.stateName(got_state) );       
                    # pass
            # elif required_sensor_state == self.sensorOff:
                # print( ">> moveBackToSensor" + " sensor state off" );
                # if got_state == INACTIVE:
                    # self.setSpeed(0)
                    # #self.waitMsec(1000)
                    # break
                # else:
                    # print( ">> moveBackToSensor" + " req_sensor_state off " + self.stateName(got_state) ); 
                    # pass
            # else:
                # pass             

    # def countTrucksAndPosition(self, noTrucksToCount, sensor, state_to_use):
        # print(">> countTrucksAndPosition: count trucks")
        # if state_to_use = "ACTIVE"
            # self.countTrucksActive(noTrucksToCount, sensor, state_to_use)
        # else:
        
        # # wait 1 second for layout to catch up, then set speed
        # print(">> countTrucksAndPosition: counted trucks, wait 5 secs")
        # self.waitMsec(5000)       
        # print(">> countTrucksAndPosition: self.moveToDisconnectPosition(sensor)")
        # # self.moveToDisconnectPosition(sensor)
        # # print(">> countTrucksAndPosition: moved to disconnect position, wait 5 secs")
        # # self.waitMsec(5000) 
                            
                            
    # def countTrucks(self, noTrucksToCount, sensor, state_to_use): #state-to_use can be "ACTIVE" or "INACTIVE"
        # pass
        
        # #can count 0 to n trucks on active
        # #can count 1 to n trucks on inactive
        
        # #check for invalid count
        # if state_to_use == "INACTIVE" and noTrucksToCount == 0:
            # print "!!!!!!!!!!!!!state_to_use == 'INACTIVE' and noTrucksToCount == 0"
            
        # # delay so that we are on a truck then count the number of off events
        # print("no trucks to count " + str(noTrucksToCount))
        # count = 0
        # on_count = 0
        # while 1:
            # print("waiting change on sensor " + self.sensorName(sensor))
            # self.waitChange([sensor])
            # sensorstate = sensor.getKnownState()
            # print(">>countTrucks: sensor state is " + self.stateName(sensorstate)) 
            # if sensorstate == INACTIVE and state_to_use == self.stateName(sensorstate):
                # count+= 1
                # if count == noTrucksToCount:
                    # print("Bingo count is " + str(count))
                    # self.setSpeed(self.stop)
                    # break
                # else:           
                    # print(">>countTrucks: ignoring sensor 1, count is " + str(count) + " noTrucksToCount " + str(noTrucksToCount))
                    # print(">>countTrucks: ignoring sensor 2, sensor state is " + self.stateName(sensorstate)) 
            # elif sensorstate == ACTIVE and state_to_use == self.stateName(sensorstate):
                # on_count+=1
                # print(">>countTrucks: sensor on_count " + self.stateName(sensorstate) + " count = " + str(on_count))
                # print("noTrucksToCount " + str(noTrucksToCount))
                # if on_count == noTrucksToCount:
                    # print("Bingo on_count is " + str(on_count))
                    # self.setSpeed(self.stop)
                    # break
                # else:
                    # print(">>countTrucks: ignoring sensor 1a, on_count is " + str(on_count) + " noTrucksToCount " + str(noTrucksToCount))
                    # print(">>countTrucks: ignoring sensor 2a, sensor state is " + self.stateName(sensorstate)) 
            # else:
                # print(">>countTrucks: ignoring sensor 1b, count is " + str(count) + " noTrucksToCount " + str(noTrucksToCount))
                # print(">>countTrucks: ignoring sensor 2b, on_count is " + str(on_count))
                # print(">>countTrucks: ignoring sensor 3b, sensor state is " + self.stateName(sensorstate)) 
                
    def countTrucksActive(self, noTrucksToCount, sensor):
        on_count = -1 #can count 0 to n trucks on active   The first truck is O in case we dont want to pick up one
        while 1:
            waitChangeSensorActive(sensor)
            on_count+=1
            print(">>countTrucksActive: on_count = " + str(on_count))
            print("noTrucksToCount " + str(noTrucksToCount))
            if on_count == noTrucksToCount:
                print("Bingo on_count is " + str(on_count))
                self.setSpeed(self.stop)
                break
                    
    def countTrucksInactive(self, noTrucksToCount, sensor):
        off_count = 0 #can count 1 to n trucks on inactive, because if a truck exits a sensor that is the first truck
        while 1:
            waitChangeSensorInactive(sensor)
            off_count+=1
            print(">>countTrucksInActive: off_count = " + str(off_count))
            print("noTrucksToCount " + str(noTrucksToCount))
            if off_count == noTrucksToCount:
                print("Bingo off_count is " + str(off_count))
                self.setSpeed(self.stop)
                break                    
            
    def countTrucks(self, noTrucksToCount, sensor, state_to_use): #state-to_use can be "ACTIVE" or "INACTIVE"
        pass
        
        #can count 0 to n trucks on active
        #can count 1 to n trucks on inactive
        
        #check for invalid count
        if state_to_use == "INACTIVE" and noTrucksToCount == 0:
            print "!!!!!!!!!!!!!state_to_use == 'INACTIVE' and noTrucksToCount == 0"
        
        # delay so that we are on a truck then count the number of off events
        print("counting " + str(noTrucksToCount) + " trucks on " + state_to_use)
        off_count = 0
        on_count = -1
        print "off_count is " + str(off_count)
        print "on_count is " + str(on_count)
        while 1:
            print("waiting change on sensor " + self.sensorName(sensor))
            self.waitChange([sensor])
            sensorstate = sensor.getKnownState()
            print(">>countTrucks: sensor state is " + self.stateName(sensorstate)) 
            if sensorstate == INACTIVE and state_to_use == self.stateName(sensorstate):
                print "off_count is @x " + str(off_count)
                off_count += 1
                print "off_count is @y " + str(off_count)
                if off_count == noTrucksToCount:
                    print("Bingo count is " + str(off_count))
                    self.setSpeed(self.stop)
                    break
                else: 
                    print "off_count is @z " + str(off_count)                
                    print(">>countTrucks: ignoring sensor @1, off_count is " + str(off_count) + " noTrucksToCount " + str(noTrucksToCount))
                    print(">>countTrucks: ignoring sensor @2, sensor state is " + self.stateName(sensorstate)) 
            elif sensorstate == ACTIVE and state_to_use == self.stateName(sensorstate):
                on_count+=1
                print(">>countTrucks: sensor on_count " + self.stateName(sensorstate) + " on_count = " + str(on_count))
                print("noTrucksToCount " + str(noTrucksToCount))
                if on_count == noTrucksToCount:
                    print("Bingo on_count is " + str(on_count))
                    self.setSpeed(self.stop)
                    break
                else:
                    print(">>countTrucks: ignoring sensor @1a, on_count is " + str(on_count) + " noTrucksToCount " + str(noTrucksToCount))
                    print(">>countTrucks: ignoring sensor @2a, sensor state is " + self.stateName(sensorstate)) 
            else:
                print(">>countTrucks: ignoring sensor @1b, off_count is " + str(off_count) + " noTrucksToCount " + str(noTrucksToCount))
                print(">>countTrucks: ignoring sensor @2b, on_count is " + str(on_count))
                print(">>countTrucks: ignoring sensor @3b, sensor state is " + self.stateName(sensorstate)) 
                


           

    def disconnect(Branch):
        self.throttle.setSpeedSetting(0)
        self.pause(1) # pause for 1 sec
  
        
              

    def swapRouteSameDirectionTravelling(self, fromBranch, toBranch):
        self.setDirection(fromBranch, toBranch)

    def swapRouteOppDirectionTravelling(self, fromBranch, toBranch):
        self.setDirection(fromBranch, toBranch)


    def sensorName(self, sensor) :
        if sensor == self.sensor1:
            return "Sensor1"
        elif sensor == self.sensor2:
            return "Sensor2"
        elif sensor == self.sensor3:
            return "Sensor3"
        elif sensor == self.sensor4:
            return "Sensor4"
        else:
            return "Invalid"
    
    # Define routine to map status numbers to text
    def stateName(self, state) :
        if (state == ACTIVE) :
            return "ACTIVE"
        if (state == INACTIVE) :
            return "INACTIVE"
        if (state == INCONSISTENT) :
            return "INCONSISTENT"
        if (state == UNKNOWN) :
            return "UNKNOWN"
        return "(invalid)"
    
    # def moveTrucks_old(self, noTruckstoMove, fromBranch, destBranch, pegs):
        
        # noTrucksOnStack4 = self.noTrucksOnStack(pegs, 4)
        # if self.initialmove :
            # self.swapRouteSameDirectionTravelling(4, fromBranch)
            # self.moveEngineToBranch(4, fromBranch) # move
            # # and connect with existing trucks if any
            # self.pause(1)
            # self.connectTrucks(fromBranch)
            # self.initialmove = False

        # noTrucksOnTrain = noTrucksOnStack4
        # #noTrucksToMove = noTrucks
        # self.moveToDisconnectTrucks(noTrucksOnTrain,
                               # noTrucksToMove, fromBranch)
        # #move to right place todisconnect
        # #move fromonelinked list to another
        # # self.disconnectTrucks(noTrucksOnStack4,
                         # # noTrucksToMove, fromBranch, destBranch)
        
        # self.disconnect(fromBranch) # disconnect

        # self.moveEngineToBranch4(fromBranch, 4, TrucksToMove)
       
        # self.moveEngineToBranch(4, destBranch, TrucksToMove)
 
        # #self.connectTrucksToTrain4(destBranch)
        # self.swapRouteOppDirectionTravelling(4, fromBranch)
        
    def moveTrucksAllAtOnce(self, noTrucksOnTrain, startsInBranch4, fromBranch, destBranch, noTruckstoMove):
        if startsInBranch4 :
            noTrucksOnStack4 = self.noTrucksOnStack(pegs, 4)
            self.moveTrucks(noTrucksOnStack4,4,fromBranch)
            self.initialmove = False
            noTrucksOnTrain = noTrucksOnStack4
        
        if fromBranch != 4:
            noTrucks = self.moveTrucks(noTrucksOnTrain, noTruckstoMove, fromBranch, 4)
        if destBranch != 4:       
            noTrucks = self.moveTrucks(noTrucks, noTruckstoMove, 4, destBranch)
        
        return noTrucks
            



    # #def moveTrucksOneByOne(startBranch, fromBranch, refPos, noTrucks, destBranch) 
    # def moveTrucksOneByOne_old(self, startBranch, fromBranch, destBranch, noTrucks):
        
        # # engine starts in fromBranch
        # # picks uptruck in fromBranch and deposits in destBranch.
        # # it then returns to dest branch if another truck is to be picked up

        # init = True
        # for i in Range(noTrucks):
            # noTrucksOnStack4 = self.noTrucksOnStack(pegs, 4)
            # if fromBranch != 4:
                # print("Hi")
                
            # if fromBranch != 4:
                # print("Hi")
                # if startBranch == 4 and init == true:
                    # moveEngineToBranch(4, fromBranch, 1) # move engine so engine is at stop
                    # connectTrucks(fromBranch)
                # init = False
                # #swapRouteOppDirectionTravelling(fromBranch, 4)
                # #self.swapDirection()

                # noTrucksOnTrain = noTrucksOnStack4
                # noTrucksToMove = 1 # if noTruckstomove is +ve then picking up a truck

                # moveToDisconnectTrucks(noTrucksOnTrain,
                        # noTrucksToMove, fromBranch, 4) #move engine back so can disconnect

                # disconnectTrucks(noTrucksOnStack4, noTrucksToMove, fromBranch, i) 
                # disconnectSignal(fromBranch)
                # noOfTrucks = noTrucksOnTrain + noTrucksToMove
                # moveEngineToBranch(fromBranch, 4, )

            # if destBranch != 4:

                # swapDirectionTravelling(4, destBranch)

                # moveEngineToBranch(4, destBranch)
                # connectTrucks(destBranch)
                # # we have picked a truck up
                # noTrucksOnTrain = noTrucksOnStack4 + 1 

                # noTrucksToMove = -1  # deposit a truck

                # if noTrucksToMove>0: #remove truck
                    # swapRouteOppDirectionTravelling(destBranch, 4)
                    # moveToDisconnectTrucks(noTrucksOnTrain,
                            # noTrucksToMove, destBranch, 4)
                # else:
                    # moveToDisconnectTrucks(noTrucksOnTrain,
                            # noTrucksToMove, 4, destBranch)	

                # disconnectTrucks(noTrucksOnTrain,
                        # noTrucksToMove, destBranch, i * 10)
                # disconnectSignal(destBranch)
                # if noTrucksToMove<0 : #remove truck
                    # swapRouteOppDirectionTravelling(destBranch, 4)
                    # swapRouteSameDirectionTravelling(destBranch, 4)  # should not do anything, but does

                # pause(0) # pause for 1 sec
                # if i != noTrucks - 1:
                    # moveEngineToBranch(destBranch, 4)
                    # #swapRouteOppDirectionTravelling(4, destBranch)
                    # self.swapDirection()
                    
    def setDirection(self, fromBranch, toBranch):
        self.setPoints(fromBranch,toBranch)
        if fromBranch == 4:
            # set loco to forward
            print("Set Loco Forward")
            throttle.setIsForward(True)
        else:
            # set loco to reverse
            print("Set Loco backward")
            throttle.setIsForward(False)
            
    def changeDirection(self):
        global throttle
        if throttle.getIsForward():
            throttle.setIsForward(False)
            print("Changed direction, reverse")
        else:
            throttle.setIsForward(True)
            print("Changed direction, forward")
                    
    def setPoints(self, fromBranch, toBranch):
        print("setting points fromBranch = " + str(fromBranch) + " toBranch = " + str(toBranch))
        if fromBranch == 4:
            if toBranch == 1:
                print("set point1 CLOSED")
                self.point1.setState(CLOSED)
            else:
                print("set point1 THROWN")
                self.point1.setState(THROWN)
            self.waitMsec(50)
            if toBranch == 3:
                print("set point2 CLOSED")
                self.point2.setState(CLOSED)
            else:
                print("set point2 THROWN")
                self.point2.setState(THROWN)
            self.waitMsec(50) 
        else:
            self.setPoints(toBranch, fromBranch)      # only define what we need to do once 
        print("end setting points")

    def setSensor(self, branch):
        print("setting sensor")
        if branch == 1:
            sensor = self.sensor1
        if branch == 2:
            sensor = self.sensor2
        if branch == 3:
            sensor = self.sensor3
        if branch == 4:
            sensor = self.sensor4
        print("end setting sensor")
        return sensor
        
    def setSpeed(self, speed):
        global throttle
        print("set speed to " + str(speed))
        throttle.setSpeedSetting(speed)   
        print ("end set speed to " + str(speed))
        
class Mywindow(JFrame):

    def __init__(self):
        super(Mywindow, self).__init__(windowClosing=self.on_close)
        self.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE)
        
        self.setSize(300,200)
        self.setLocationRelativeTo(None) # None is null in Java
        self.setTitle("Title")
        
        self.button=JButton('Click me to stop program', actionPerformed=self.on_click)
        self.add(self.button)

    def on_click(self,widget):
        global stop_program
        global throttle
        print("clicked onclick")
        if JOptionPane.showConfirmDialog(None,"Are you sure you want to exit","Exit", 
        JOptionPane.YES_NO_OPTION) == JOptionPane.YES_OPTION:
            print ("Bye")
            self.dispose()
            stop_program = True
            #pygame.quit()
            throttle.setSpeedSetting(0)
            print ("stop_program = " ,stop_program)
            pygame.quit()

    def on_close(self, widget):
        print('clicked')

                    

    # instructions = generate_instructions()
    
    # for position in instructions:
        # if type(position[0]) is str:
            # #this is a command for the train
            # print("in test3")
            # print ("stop_program = " ,stop_program)
            # if stop_program == True:
                # pass
                # self.dispose()   # there is no dispose function so it crashes - which is what we want
            # t.decide_what_to_do(position)
            
       



SPACE_PER_PEG = 100

def display_pile_of_pegs(pegs, start_x, start_y, peg_height, screen, base_width):
    """
    Given a pile of pegs, displays them on the screen, nicely inpilated
    like in a piramid, the smaller in lighter color.
    """
    for i, pegwidth in enumerate(pegs):
        #print ("enumerate pegs",i)
        #pegwidth = pegs[i] * base_width
        #self.factor = 1
        pygame.draw.rect(
            screen,
            # Smaller pegs are ligher in color
            #(255-pegwidth*base_width, 255-pegwidth*base_width, 255-pegwidth*base_width),
            (255 - 100, 255 - 100, 255 - 100),
            #pyj2d.locals.blue,
            (
              start_x + (SPACE_PER_PEG - pegwidth* base_width)/2 , # Handles alignment putting pegs in the middle, like a piramid
              start_y - peg_height * i,         # Pegs are one on top of the other, height depends on iteration
              pegwidth*base_width,
              peg_height
            )
        )

def setup(pegs, noPegs):
    print "setup"
    #for i in range(0,2):
    #    assert len(pegs[i]) == noPegs[i], 'not enough disks on peg'
    yield pegs
    #now run the shunting puzzle
    ingle = Inglenook(pegs)

    #don't need these
    #ingle.init_position_branch()
    for p in ingle.solvePuzzle():
        yield p
    print "end of setup"

    #assert ingle.positions.count(1) == 1
    #assert ingle.branches.count(1) == 5
    #assert ingle.branches.count(2) == 3


def setupBlocks(noPegs, base_width, peg_height, sleeping_interval):
    # pegs = [[i  for i in reversed(range(1, noPegs[0]+1))],
    #         #[i  for i in reversed(range(noPegs[0]+1, noPegs[0]+ noPegs[1]+1))],
    #         [1,2,3],[],[]]
    #         #[i  for i in reversed(range(noPegs[0]+ noPegs[1]+1, noPegs[0]+ noPegs[1]+ noPegs[2]+1))],
    #         #[i  for i in reversed(range(noPegs[0]+ noPegs[1]+ noPegs[2]+1, noPegs[0]+ noPegs[1]+ noPegs[2]+ noPegs[3]+1))]]
    
    print "hi1"
    pegs = [[2,1,5,3,4],[6,7,8],[],[]]



    positions = setup(pegs, noPegs)

    pygame.init()
    screen = pygame.display.set_mode( (650, 200) )
    pygame.display.set_caption('Shunting Puzzle')
    index = 0
    print("setupblocksa index != 1 " + str(index))
    for position in positions:

        screen.fill((255, 255, 255))
        # if type (position[0]) != "list":
        #     pass
        # else:
        #     for i, pile in enumerate(position):
        #         display_pile_of_pegs(pile, 50 + SPACE_PER_PEG*i, 500, peg_height, screen, base_width)
        #         # if type(pile[1])== "str":
        #         #     pass
        #         # else:
        #         #     display_pile_of_pegs(pile, 50 + SPACE_PER_PEG * i, 500, peg_height, screen, base_width)
        #     pygame.display.update()
        #     time.sleep(sleeping_interval)
        if type(position[0]) is str:
            #this is a command for the train
            print("setupblocksb index = " + str(index))
            index += 1
            print("setupblocksc index = " + str(index))
            print ">> setup Blocks: position = " 
            print position
            print("setupblocksd index = " + str(index))
            if index == 1:
                print("setupblockse index == 1 " + str(index))
                print("setupblocks index = 1")
                t.decide_what_to_do_first()
            print("setupblocksf index = " + str(index))
            self.noTrucksOnTrain = t.decide_what_to_do(position)
            
            ##train.update_position(position)
            pass
        else:
            print("setupblocksg index != 1 " + str(index))
            print ">> setup Blocks2: position = " 
            print (position)
            for i, pile in enumerate(position):
                display_pile_of_pegs(pile, 20 + SPACE_PER_PEG * i, 100, peg_height, screen, base_width)
            pygame.display.update()
            time.sleep(sleeping_interval)

    pygame.quit()

def run_inglenook():
    print "lo"
    #doctest.testmod()
    setupBlocks(
        noPegs = 4,
        base_width = 10,
        peg_height = 10,
        sleeping_interval = 1
    )
    print "end of run_inglenook"
    
def setup_thread():
    print "hi"
    t = threading.Thread(target=run_inglenook, name="run Shunting Puzzle")
    t.daemon = True
    t.start()


# if __name__ == '__main__':
    # setup_thread()

# t = Move_train()
# t.start()
# t.waitMsec(5000)
# print(Move_train().__dict__)
# win = Mywindow()
# win.setVisible(1)
# print "hi"
# print __name__
# setup_thread()
  

if __name__ == "__builtin__":
    # def generate_instructions():
        # #yield ["move_trucks", noTrucks, fromBranch, destBranch, self.pegs]
        # # should be
        # #moveTrucks(self, noTrucksOnTrain, noTruckstoMove, fromBranch, destBranch):
        # yield ["move_trucks",  1,  0, 4, 1]
        # yield ["move_trucks",  2,  1, 1, 2]
    
    print (__name__)
    t = Move_train()
    t.start()
    t.waitMsec(5000)
    print(Move_train().__dict__)
    win = Mywindow()
    win.setVisible(1)
    setup_thread() 