import jarray
import jmri
import java.beans
#import jmri.jmrit.automat.AbstractAutomaton as aa
import sys, os
from javax.swing import JFrame, JButton, JOptionPane


# move_train import move_train
#from move_train2 import Move_train 
import doctest
import time
import pyj2d as pygame
from pyj2d.locals import *
import threading


frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second

# logValue = 3
logging = "noprint"

sys.path.append('Z:\\ConfigProfiles\\jython\\timesaver')
from timesaver import *

throttle = None
stop_program = False

import logging
logging.basicConfig(filename='Z:\\ConfigProfiles\\jython\\timesaver\\example.log',filemode='w',level=logging.DEBUG)
logging.debug('******************************')
logging.info('So should this')
logging.warning('And this, too')


class Move_train(jmri.jmrit.automat.AbstractAutomaton) :

    # def __init__(self,instructions):
        # self.instructions = instructions
        
    # def run_generator(self,instruction)
        # #instruction = self.instructions.next()
        # self.decide_what_to_do(instruction)
        
    tender = True
    indentno = 0
    
    def myprint(self, *args):
        if logging == "print":
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
        #self.myprint("bell")
        snd = jmri.jmrit.Sound("resources/sounds/Bell.wav")
        snd.play()
        #self.myprint("bell end")
        
    def indent(self):
        self.indentno = self.indentno + 2
        
    def dedent(self):
        self.indentno = self.indentno - 2
    
    def init(self):
        self.indent()
        self.myprint(" in Move_train inir")
        global throttle
        #speeds
        self.stop = 0
        self.slow = 0.1
        self.uncouple = 0.1
        self.medium = 0.5
        self.couple = 0.3
        self.fast = 0.7
        
        #sensor States
        self.sensorOn = 1
        self.sensorOff = 0
        
        self.initialmove = True
        self.myprint("Inside init(self)xx")
        
        list = sensors.getSystemNameList()
        self.myprint( list)
        list = turnouts.getSystemNameList()
        self.myprint( list)  
        try:
            self.myprint ("trying to set up sensors")
            
            #self.sensor1 = sensors.provideSensor("MS+N259E5;-N259E5")
            self.sensor1 = sensors.provideSensor("sensor1")
            self.myprint ("This is an success message! s1 set up")
            #self.sensor2 = sensors.provideSensor("MS+N259E6;-N259E6")
            self.sensor2 = sensors.provideSensor("sensor2")
            self.myprint ("This is an success message! s2 set up")
            #self.sensor = sensors.provideSensor("MS+N259E7;-N259E7")
            self.sensor3 = sensors.provideSensor("sensor3")
            self.myprint ("This is an success message! s3 set up")
            #self.sensor4 = sensors.provideSensor("MS+N259E8;-N259E8")
            self.sensor4 = sensors.provideSensor("sensor4")
            self.myprint ("This is an success message! s4 set up")
            self.myprint ("in move_train2.py")
        except:
            self.myprint ("sensors not set!")
            
        try:
            self.myprint ("trying to set up points")
            self.point1 = turnouts.provideTurnout("point1")
            self.point2 = turnouts.provideTurnout("point2")
            self.myprint ("set up points")
        except:
            self.myprint ("points not set!")
         
        # get loco address. For long address change "False" to "True"
        try:
            self.myprint("throttle set up2")
            throttle = self.getThrottle(3, False)  # short address 3
            #throttle = self.throttle
            self.myprint("throttle set up3")
            self.myprint (throttle)
        except:
            self.myprint("throttle not set up")
        
        self.myprint ("finished init")
        self.myprint(self.__dict__)
        self.myprint(dir())
        self.dedent()
    
    def decide_what_to_do_first(self):
        self.indent()
        #set up the trucks 5 in branch 3 and 3 in branch 2, and return to branch 4
        # self.noTrucksOnTrain = 0
        
        self.myprint("decide_what_to_do_first")

        self.noTrucksOnTrain = 0
        self.initialBranch = 4
        self.noTrucksToMoveFromPreviousStep = 0
        self.myprint ("self.noTrucksOnTrain:" + str(self.noTrucksOnTrain))
        self.myprint ("self.initialBranch:" + str(self.initialBranch))
        # instruction_first = [generate_first_instructions]
        # self.noTrucksOnTrain = self.decide_what_to_do(instruction_first,self.noTrucksOnTrain)
        self.myprint("end decide_what_to_do_first")
        self.dedent()
    
    def generate_first_instructions(self):
        self.indent()
        # the move trucks instruction is shown commented out, so we can see what the yield does
        #moveTrucks(self, noTrucksOnTrain, noTruckstoMove, fromBranch, destBranch):
        
        #we move from branch 4 to branch 3 depositing all 5 trucks
        self.dedent()

        
        pass
        
    def decide_what_to_do(self, instructions):
        self.indent()
    
        # decide_what_to_do uses the instructions and also uses two variables
        #  * noTrucksOnTrain
        #  * initialBranch
    
    
        self.myprint("decide_what_to_do")
        self.myprint (instructions)
        print("printed instructions")
        if instructions[0] == "move_trucks_one_by_one":
            #the argumants in inglenook are yield ["move_trucks_one_by_one", noTrucks, fromBranch, destBranch, self.pegs]
            #the arguments in this file are moveTrucksOneByOne(self, noTrucksOnTrain, startsInBranch4, fromBranch, destBranch, noTrucksToMove, pegs)
            self.myprint (">>decidewhattodo, move_trucks_one_by_one" )
            self.myprint ("instructions[0]:" + str(instructions[0]))
            self.myprint ("instructions[1]:" + str(instructions[1]))
            self.myprint ("instructions[2]:" + str(instructions[2]))
            self.myprint ("instructions[3]:" + str(instructions[3]))
            self.myprint ("instructions[4]:" + str(instructions[4]))
            self.myprint ("noTrucksOnTrain " + str(self.noTrucksOnTrain))
            self.myprint ("initialBranch " + str(self.initialBranch))
            
            self.moveTrucksOneByOne( instructions[1],instructions[2],instructions[3],instructions[4])
            pass
        elif instructions[0] == "move_trucks":
            self.myprint(" about to moveTrucks",instructions[1], instructions[2], instructions[3], instructions[4])
            self.moveTrucks(instructions[1], instructions[2], instructions[3])
            pass
        else:
            self.myprint("!!!!!!!!!unrecognised instruction " & instructions[0])
            pass
        self.myprint("end decide_what_to_do")
        self.dedent()
        #return noTrucksOnTrain
            
    def startFromBranch4(self, destBranch, pegs):
        self.indent()
        self.myprint("In startFromBranch4")
        self.noTrucksOnTrain =  self.noTrucksOnStack(pegs, 4)
        noTrucksToMove = 0
        fromBranch = 4 
        destBranch = destBranch
        self.moveEngineToBranch(noTrucksOnTrain, noTrucksToMove, fromBranch, destBranch)
        connectTrucks(fromBranch)
        self.dedent()
                
    def moveTrucksOneByOne(self, noTrucksToMove, fromBranch, destBranch,  pegs):
        self.indent()    
        
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
        
        self.myprint (">>moveTrucksOneByOne " )
        self.myprint ("self.noTrucksOnTrain:" + str(self.noTrucksOnTrain))
        self.myprint ("self.initialBranch:" + str(self.initialBranch))
        self.myprint ("fromBranch:" + str(fromBranch))
        self.myprint ("destBranch:" + str(destBranch))
        self.myprint ("noTrucksToMove:" + str(noTrucksToMove))
        
        if self.initialBranch != fromBranch:
            self.myprint ("!!!!!!!!!!self.initialBranch != fromBranch:" + str(noTrucksToMove))
            # noTrucksOnStack4 = self.noTrucksOnStack(pegs, 4)
            self.moveTrucks(self.noTrucksOnTrain, self.initialBranch, fromBranch)
            #connectTrucks(fromBranch)
            self.myprint ("!!!!!!!!!!moveTrucksOneByOne: self.initialBranch != fromBranch:" + str(noTrucksToMove))
		
        self.myprint ("!!!!!!!!!!!moveTrucksOneByOne: stage2 " + str(noTrucksToMove))
        for i in Range(noTrucksToMove):
            noTrucksToMoveInOneGo = 1
            if fromBranch != 4:
                self.myprint ("!!!!!!!!!!!moveTrucksOneByOne: stage2a " + str(noTrucksToMoveInOneGo))
                self.moveTrucks(noTrucksToMoveInOneGo+1, fromBranch, 4) #need to count 2 trucks 
            if destBranch != 4: 
                self.myprint ("!!!!!!!!!!!moveTrucksOneByOne: stage2b " + str(noTrucksToMoveInOneGo))
                self.moveTrucks(noTrucksToMoveInOneGo, 4, destBranch)
        
        self.noTrucksOnTrain = noTrucks
        self.initialBranch = fromBranch 
        self.dedent()      
            
    def moveTrucks(self, noTrucksToMove, fromBranch, destBranch):
        self.indent()
    
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
        
        
        self.myprint (">>moveTrucks " )
        self.myprint ("self.noTrucksOnTrain:" + str(self.noTrucksOnTrain))
        self.myprint ("self.initialBranch:" + str(self.initialBranch))
        self.myprint ("self.noTrucksToMoveFromPreviousStep "+ str(self.noTrucksToMoveFromPreviousStep))
        self.myprint ("fromBranch: " + str(fromBranch))
        self.myprint ("destBranch: " + str(destBranch))
        self.myprint ("noTrucksToMove: " + str(noTrucksToMove))
        self.myprint("in movetrucks")
        #self.myprint("Movetrucks",str(noTrucksOnTrain), noTrucksToMove, fromBranch, destBranch)
        
        
        
        if self.initialBranch == fromBranch:
            noTrucksToMove = self.noTrucksToMoveFromPreviousStep - noTrucksToMove
            noTrucksToMoveFromPreviousStep = 0
            # now move and disconnect
        
        if self.initialBranch != fromBranch:
            self.myprint("(1) self.initialBranch != fromBranch")
            if self.initialBranch != 4:
                self.myprint("(1a) self.initialBranch != fromBranch")
                operation = self.moveToDisconnectPosition(self.noTrucksOnTrain, 
                self.noTrucksToMoveFromPreviousStep, initialBranch)
                self.myprint("operation = " + str(operation))
                sensor = self.setSensor(initialBranch)
                self.uncouple(fromBranch, toBranch, sensor, operation)
                noTrucksToMoveFromPreviousStep = 0
                self.myprint("end (1a) self.initialBranch != fromBranch")
            # move to fromBranch. We take the current number of trucks on train. i.e. 0 extra trucks
            if self.initialBranch != 4:
                self.myprint("(1b) self.initialBranch != fromBranch: self.initialBranch != 4")
                # move from initialBranch to mainLine
                self.moveToBranch(self.noTrucksOnTrain, 0, 4)
                self.myprint("end (1b) self.initialBranch != fromBranch: self.initialBranch != 4")
            # if frombranch != mainLine
            # move from mainLine to fromBranch
            if fromBranch != 4:
                self.myprint("(1c) self.initialBranch != fromBranch: fromBranch != 4")
                self.moveToBranch(self.noTrucksOnTrain, 0, fromBranch)
                self.myprint("end (1c) self.initialBranch != fromBranch: fromBranch != 4" + "noTrucksOnTrain = " + str(self.noTrucksOnTrain))
                self.myprint("waiting 30 secs 1(c)")
                self.setSpeed(self.stop)
                #self.waitMsec(30000)
                #self.myprint("waiting 30 secs2")
            #now move and disconnect
            self.myprint("end (1) self.initialBranch != fromBranch")

        if fromBranch != 4:
            self.myprint("(2) in movetrucks fromBranch: fromBranch != 4")
            self.myprint ("fromBranch: " + str(fromBranch))
            self.myprint ("destBranch: " + str(destBranch))
            self.myprint ("noTrucksToMove: " + str(noTrucksToMove))
            self.myprint ("self.noTrucksOnTrain:" + str(self.noTrucksOnTrain))
            # disconnect 
            self.myprint("move to disconnect position")
            operation = self.moveToDisconnectPosition(self.noTrucksOnTrain, noTrucksToMove, fromBranch)
            self.myprint ("moved to disconnect position")
            self.myprint ("operation = " + str(operation))
            self.myprint ("fromBranch= " + str(fromBranch))
            self.myprint("attempting to uncouple")
            self.uncouple1(fromBranch, operation)
            
            
            # take trucksToMove from frombranch to mainLine
            self.myprint("take trucksToMove from frombranch to mainLine")
            self.moveToBranch(self.noTrucksOnTrain, noTrucksToMove, 4)
            self.myprint("end (2) in movetrucks fromBranch: fromBranch != 4")
            
        if destBranch != 4:
            self.myprint("(3) in movetrucks fromBranch: destBranch != 4")
            self.moveToBranch(self.noTrucksOnTrain, noTrucksToMove, destBranch)
            self.myprint("end (3) in movetrucks fromBranch: destBranch != 4")
            self.myprint("waiting 30 secs1")
            self.waitMsec(1000)
            #self.moveToDisconnectPosition(self.noTrucksOnTrain, noTrucksToMove, destBranch)
            # self.myprint("about to couple need to do this only if necessary")
            # self.couple1(destBranch) 
            # self.myprint("coupled")
            #self.waitMsec(1000)
            self.myprint("waited 30 secs1")
            
           
        # note: we do not disconnect here because if we need to pick up in the same branch we do
        # not disconnect, hence we do the disconnect in the next move, if self.initialBranch != fromBranch
            
        # set the two global variables
        self.noTrucksOnTrain = self.noTrucksOnTrain + self.noTrucksToMoveFromPreviousStep
        self.initialBranch = fromBranch
        self.noTrucksToMoveFromPreviousStep = noTrucksToMove
        self.myprint("set variables")
        
       # we are now ready to do the final deposit in the next step
       
        self.myprint ("end moveTrucks " )
        self.dedent()

    def fred(self,fromBranch,operation):
        self.indent()
        self.myprint("in uncouple")

    def moveEngineToBranch(self,fromBranch, toBranch, trucksToMove):
        self.indent()
        self.myprint("In moveEngineToBranch")
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
        self.countTrucksInActive(noTrucksToCount, sensor)
        self.setSpeed(self.stop)
        self.waitMsec(1000)
        
        #go on for a bit
        self.setSpeed(self.slow)
        self.waitMsec(500)
        self.setSpeed(self.stop)
        
        #uncouple
        self.uncouple()
        
        self.myprint ("end moveEngineToBranch " )
        self.dedent()
        
 
    def couple1(self, branch):   #couple seems to be a reserved word, so use couple1
        logging = "print"
        self.indent()
        self.myprint("in couple")
        

        
        fromBranch = 4
        toBranch = branch
        self.setDirection(fromBranch, toBranch)
        timeCouple = 400
        self.myprint("about to call bell")
        self.mysound()
        self.myprint("called bell")
        self.setSpeedSetDelay(self.couple, timeCouple)  
        self.setSpeedSetDelay(self.stop,2000)
        
        
        self.myprint("finished couple part 1a waiting 3 secs")
        print("finished couple part 1a waiting 3 secs")
        self.waitMsec(5000)
        #self.mysound()
        self.myprint("finished couple part 1")
        
        tr1 = timeCouple * self.couple 
        #print(tr1)
        tr2 = (self.slow )
        #print tr2
        timeReturn = tr1/tr2
        #print timeReturn
        #self.myprint("timeReturn = " + str(timeReturn))
        timeReturn = int(timeReturn*0.5)
        self.myprint("int timeReturn = " + str(timeReturn))
        #self.waitMsec(1000)
        
        self.setDirection(toBranch, fromBranch)
        #self.mysound()
        self.setSpeedSetDelay(self.slow, timeReturn)
        #self.mysound()
        #self.waitMsec(500)
        self.setSpeedSetDelay(self.stop,2000)
        print("finished couple part 2 waiting 5 secs")
        self.waitMsec(5000)
        #self.myprint("finished couple part 3")

        self.myprint("finished couple")
        self.dedent()
        logging = "noprint"


    
    def uncouple1(self, branch, operation):     #uncouple seems to be a reserved word, so use uncouple1
        logging = "print"
        self.indent()
        self.myprint("in uncouple")
        fromBranch = branch
        toBranch = 4
        sensor = self.setSensor(branch)
        self.setSpeed(self.stop)
        # #if operation == "PICKUP":
        # self.myprint("in pickup")
        # #whiz forward
        # self.setDirection(fromBranch, toBranch)
        # self.setSpeed(self.uncouple)
        # #self.waitMsec(500)
        # #count twice 'cos in active
        # #waitChangeActive(sensor)    # sets speed 0
        # noTrucksToCount = 1  # starts from 0 ( we are in a truck so that is 0
        # self.countTrucksActive(noTrucksToCount, sensor)
        # self.setSpeed(stop)
        self.waitMsec(1000)

        
        #whiz back
        self.myprint("in whizback")
        self.setDirection(toBranch, fromBranch)
        self.setSpeedSetDelay(self.uncouple,50)
        #self.waitMsec(1000)
        noTrucksToCount = 1
        self.countTrucksInactive(noTrucksToCount, sensor)
        #waitChangeInactive(sensor)  # sets speed 0
        self.myprint("countTrucksActive returned")
        self.setSpeed(self.stop)
        self.waitMsec(1000)
        
        #whiz forward again
        self.myprint("in forward again")
        self.setDirection(fromBranch, toBranch)
        self.setSpeedSetDelay(self.fast, 50)
        #self.waitMsec(100) # need to be times because has dropped off truck
        #waitChangeActive(sensor)    # sets speed 0
        # noTrucksToCount = 1
        # self.countTrucksActive(noTrucksToCount, sensor)
        self.setSpeedSetDelay(self.stop,100)
        self.myprint("end whiz forward")
        
        if operation == "DROPOFF":
        #whiz back
            self.myprint("in drop off")
            self.setDirection(toBranch, fromBranch)
            self.setSpeedSetDelay(self.fast,100)
            #waitChangeInactive(sensor)  # sets speed 0
            self.setSpeed(self.stop)
            self.myprint("end in dropoff")
        self.dedent()
        logging = "noprint"
        
    def waitChangeSensorActive(self, sensor):
        self.indent()
        #self.myprint("in waitChangeSensorActive" + " sensor " + self.sensorName(sensor))
        while 1:
            self.waitChange([sensor])
            got_state = sensor.getKnownState()      
            if got_state == ACTIVE:
                #self.myprint("got_state active")
                self.dedent()            
                break               

    def waitChangeSensorInactive(self, sensor):
        self.indent()
        self.myprint("in waitChangeSensorInactive" + " sensor " + self.sensorName(sensor))
        #waitChangeSensor(sensor,self.sensorOff)
        while 1:
            self.waitChange([sensor])
            got_state = sensor.getKnownState()
            if got_state == INACTIVE:
                #self.myprint("got_state inactive")
                self.dedent()            
                break
    
    def waitChangeSensor(self, sensor, required_sensor_state):
        self.indent()
        self.myprint("in waitChangeSensor")
        global throttle
        self.changeDirection()        
        self.setSpeed(self.slow)
        while 1:
            self.waitChange([sensor])
            got_state = sensor.getKnownState()
            self.myprint( ">> moveBackToSensor " + self.stateName(got_state) );   
            if required_sensor_state == self.sensorOn:
                self.myprint( ">> moveBackToSensor" + " sensor state on " + self.stateName(got_state) ); 
                if got_state == ACTIVE:
                    self.setSpeed(0)
                    #self.waitMsec(1000)
                    self.dedent()             
                    break
                else:
                    self.myprint( ">> moveBackToSensor" + " req_sensor_state on " + self.stateName(got_state) );       
                    pass
            elif required_sensor_state == self.sensorOff:
                self.myprint( ">> moveBackToSensor" + " sensor state off" );
                if got_state == INACTIVE:
                    self.setSpeed(0)
                    #self.waitMsec(1000)
                    self.dedent()
                    break
                else:
                    self.myprint( ">> moveBackToSensor" + " req_sensor_state off " + self.stateName(got_state) ); 
                    pass
            else:
                pass
        
    def moveToBranch(self, noTrucksOnTrain, noTrucksToMove, destBranch):
        self.indent()
        # move the train to destbranch without any coupling or decoupling
        # we have already checked that the branch we are in is not destBranch
        self.myprint("in moveToBranch")
        self.myprint("noTrucksToMove " + str(noTrucksToMove) + " destBranch " + str(destBranch))
        if destBranch != 4:
            self.myprint("destBranch != 4:")
            self.setDirection(4,destBranch)
            self.waitMsec(5000)
            self.setSpeed(self.slow)
            noToCount = 0
            sensor = self.setSensor(destBranch)
            self.myprint("got here0")
            self.countTrucksActive(noTrucksToMove, sensor) 
            self.myprint("got here1")
            self.myprint("about to couple")
            self.couple1(destBranch)
            self.myprint("got here2")
        else:
            self.myprint("moving to branch 4")
            anyBranch = 1  # choose andy branch, the direction is the same
            self.setDirection(anyBranch,4)
            self.setSpeed(self.slow)
            # going towards head count nuber of times becomes inactive
            if self.tender == True:
                extra = 2  # for engine and tender count
            else:
                extra = 1  # for engine count)
            sensor = self.setSensor(destBranch)
            self.countTrucksInactive(noTrucksToMove+extra, sensor) 
            self.setSpeed(self.stop)
            
        self.myprint("end moveToBranch: " + "noTrucksToMove " + str(noTrucksToMove) + " destBranch " + str(destBranch))
        self.dedent()
       
    def moveToDisconnectPosition(self, noTrucksOnTrain, noTrucksToMove, destBranch):
        self.indent()
        
        self.myprint ("destBranch: " + str(destBranch))
        self.myprint ("noTrucksToMove: " + str(noTrucksToMove))
        self.myprint ("noTrucksOnTrain: " + str(noTrucksOnTrain))
    
        #self.moveToDisconnectPosition(self.noTrucksOnTrain, noTrucksToMoveFromPreviousStep, destBranch)
        
        # we have already moved the train to the branch and coupled the train
        # this routine moves the train to the new decoupling position
        self.myprint ("in moveToDisconnectPosition ")
        self.myprint( "moveToDisconnectPosition: destBranch = " + str(destBranch))
        
        #dest branch is never 4
        #self.setDirection(4, destBranch)
        self.setPoints(4,destBranch)
        
        sensor = self.setSensor(destBranch)
        self.setSpeed(self.slow)
        
        # need to determine the direction to pick up or remove trucks from engine at from branch
        
        noTrucksToAdd = noTrucksToMove 
        noTrucksToCount = abs(noTrucksToAdd)
        self.myprint("  >>moveToDisconnectTrucks: noTrucksToAdd " + str(noTrucksToAdd) + " noTrucksToCount " + str(noTrucksToCount))
        
        #Assuming we are connected and need to pick up or drop off and return to destBranch
        if noTrucksToAdd >= 0:
            # picking up trucks
            self.myprint(">>moveToDisconnectTrucks: picking up Trucks");
            self.setDirection(destBranch,4)
            # self.myprint(">>moveToDisconnectTrucks: picking up trucks");
            sensor = self.setSensor(destBranch)
            self.setSpeed(self.slow)
            self.countTrucksActive(noTrucksToCount, sensor)   # counts from 0
            self.setSpeed(self.stop)
            # #need to check that have connected
            
            #stop here
            
            # #change direction
            # self.myprint(">>moveToDisconnectTrucks: moving back to Siding 4");
            # self.setDirection(4, destBranch)
            # noTrucksToCount = noTrucksOnTrain + NoTrucksToMove
            # sensor = self.setSensor(4)
            # self.setSpeed(self.slow)
            # self.countTrucksInactive(noTrucksToCount, sensor)   # counts from 1
            # self.setSpeed(self.stop)
            #self.moveToDisconnectPosition2(sensor) 
            self.myprint(">>moveToDisconnectTrucks: picked up trucks");
            operation = "PICKUP"
        else:
            #dropping off trucks
            if noTrucksToCount > noTrucksOnTrain:
                self.myprint("!!!!>>moveToDisconnectTrucks: dropping off trucks: error not enough trucks")
            self.myprint(">>moveToDisconnectTrucks: dropping off " + str(noTrucksToCount) + " trucks");
            self.setDirection(4, destBranch)
            self.setSpeed(self.slow)
            self.countTrucksInactive(noTrucksToCount, sensor)   # counts from 0
            self.setSpeed(self.stop)
            #need to check that have connected
            self.myprint("DONE1");
            self.myprint(">>moveToDisconnectTrucks: dropped off trucks");
            # self.setDirection(Branch, 4)
            sensor = self.setSensor(destBranch)
            #self.moveToDisconnectPosition2(sensor) 
            operation = "DROPOFF"
        self.myprint ("end moveToDisconnectPosition ")
        self.dedent()
        return operation
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
            # self.myprint( ">> moveBackToSensor " + self.stateName(got_state) );   
            # if required_sensor_state == self.sensorOn:
                # self.myprint( ">> moveBackToSensor" + " sensor state on " + self.stateName(got_state) ); 
                # if got_state == ACTIVE:
                    # self.setSpeed(0)
                    # #self.waitMsec(1000)             
                    # break
                # else:
                    # self.myprint( ">> moveBackToSensor" + " req_sensor_state on " + self.stateName(got_state) );       
                    # pass
            # elif required_sensor_state == self.sensorOff:
                # self.myprint( ">> moveBackToSensor" + " sensor state off" );
                # if got_state == INACTIVE:
                    # self.setSpeed(0)
                    # #self.waitMsec(1000)
                    # break
                # else:
                    # self.myprint( ">> moveBackToSensor" + " req_sensor_state off " + self.stateName(got_state) ); 
                    # pass
            # else:
                # pass             

    # def countTrucksAndPosition(self, noTrucksToCount, sensor, state_to_use):
        # self.myprint(">> countTrucksAndPosition: count trucks")
        # if state_to_use = "ACTIVE"
            # self.countTrucksActive(noTrucksToCount, sensor, state_to_use)
        # else:
        
        # # wait 1 second for layout to catch up, then set speed
        # self.myprint(">> countTrucksAndPosition: counted trucks, wait 5 secs")
        # self.waitMsec(5000)       
        # self.myprint(">> countTrucksAndPosition: self.moveToDisconnectPosition(sensor)")
        # # self.moveToDisconnectPosition(sensor)
        # # self.myprint(">> countTrucksAndPosition: moved to disconnect position, wait 5 secs")
        # # self.waitMsec(5000) 
                            
                            
    # def countTrucks(self, noTrucksToCount, sensor, state_to_use): #state-to_use can be "ACTIVE" or "INACTIVE"
        # pass
        
        # #can count 0 to n trucks on active
        # #can count 1 to n trucks on inactive
        
        # #check for invalid count
        # if state_to_use == "INACTIVE" and noTrucksToCount == 0:
            # self.myprint "!!!!!!!!!!!!!state_to_use == 'INACTIVE' and noTrucksToCount == 0"
            
        # # delay so that we are on a truck then count the number of off events
        # self.myprint("no trucks to count " + str(noTrucksToCount))
        # count = 0
        # on_count = 0
        # while 1:
            # self.myprint("waiting change on sensor " + self.sensorName(sensor))
            # self.waitChange([sensor])
            # sensorstate = sensor.getKnownState()
            # self.myprint(">>countTrucks: sensor state is " + self.stateName(sensorstate)) 
            # if sensorstate == INACTIVE and state_to_use == self.stateName(sensorstate):
                # count+= 1
                # if count == noTrucksToCount:
                    # self.myprint("Bingo count is " + str(count))
                    # self.setSpeed(self.stop)
                    # break
                # else:           
                    # self.myprint(">>countTrucks: ignoring sensor 1, count is " + str(count) + " noTrucksToCount " + str(noTrucksToCount))
                    # self.myprint(">>countTrucks: ignoring sensor 2, sensor state is " + self.stateName(sensorstate)) 
            # elif sensorstate == ACTIVE and state_to_use == self.stateName(sensorstate):
                # on_count+=1
                # self.myprint(">>countTrucks: sensor on_count " + self.stateName(sensorstate) + " count = " + str(on_count))
                # self.myprint("noTrucksToCount " + str(noTrucksToCount))
                # if on_count == noTrucksToCount:
                    # self.myprint("Bingo on_count is " + str(on_count))
                    # self.setSpeed(self.stop)
                    # break
                # else:
                    # self.myprint(">>countTrucks: ignoring sensor 1a, on_count is " + str(on_count) + " noTrucksToCount " + str(noTrucksToCount))
                    # self.myprint(">>countTrucks: ignoring sensor 2a, sensor state is " + self.stateName(sensorstate)) 
            # else:
                # self.myprint(">>countTrucks: ignoring sensor 1b, count is " + str(count) + " noTrucksToCount " + str(noTrucksToCount))
                # self.myprint(">>countTrucks: ignoring sensor 2b, on_count is " + str(on_count))
                # self.myprint(">>countTrucks: ignoring sensor 3b, sensor state is " + self.stateName(sensorstate)) 
                
    def countTrucksActive(self, noTrucksToCount, sensor):
        self.indent()
        self.myprint ("in countTrucksActive: sensor " + self.sensorName(sensor) + " noTruckstocount " + str(noTrucksToCount))
        #self.myprint( "noTrucksToCount = " + str(noTrucksToCount) + " sensor = " + self.sensorName(sensor))
        on_count = -1 #can count 0 to n trucks on active   The first truck is O in case we dont want to pick up one
        stop = False
        while 1:
            #self.myprint("waiting for sensorActive")
            self.waitChangeSensorActive(sensor)
            on_count+=1
            self.myprint("waited sensor active on_count = " + str(on_count))
            #self.myprint("sensor changed active " + self.sensorName(sensor) + "noTrucksToCount " + str(noTrucksToCount) + ("on_count = " + str(on_count)))
            if on_count == noTrucksToCount:
                self.myprint("Bingo on_count is " + str(on_count))
                self.setSpeed(self.stop)
                self.myprint("end countTrucksActive")
                stop = True
            if stop == True:
                self.dedent()
                break
                
    def countTrucksInactive(self, noTrucksToCount, sensor):
        self.indent()
        self.myprint ("in countTrucksInactive ")
        self.myprint( "noTrucksToCount = " + str(noTrucksToCount) + " sensor = " + self.sensorName(sensor))
        off_count = 0 #can count 1 to n trucks on inactive, because if a truck exits a sensor that is the first truck
        stop = False
        while 1:
            self.myprint("about to waitChangeSensorInactive") 
            self.waitChangeSensorInactive(sensor)
            off_count+=1
            self.myprint(">>countTrucksInActive: off_count = " + str(off_count))
            self.myprint("noTrucksToCount " + str(noTrucksToCount))
            if off_count == noTrucksToCount:
                self.myprint("Bingo off_count is " + str(off_count))
                self.setSpeed(self.stop)    
                self.dedent()
                stop = True
            self.myprint("end of if")
            if stop == True:
                self.dedent()
                break
            self.myprint("end of while")
            
    def countTrucks(self, noTrucksToCount, sensor, state_to_use):
        self.indent() #state-to_use can be "ACTIVE" or "INACTIVE"
        self.myprint ("in countTrucks ")
        pass
        
        #can count 0 to n trucks on active
        #can count 1 to n trucks on inactive
        
        #check for invalid count
        if state_to_use == "INACTIVE" and noTrucksToCount == 0:
            self.myprint ("!!!!!!!!!!!!!state_to_use == 'INACTIVE' and noTrucksToCount == 0")
        
        # delay so that we are on a truck then count the number of off events
        self.myprint("counting " + str(noTrucksToCount) + " trucks on " + state_to_use)
        off_count = 0
        on_count = -1
        self.myprint ("off_count is " + str(off_count))
        self.myprint ("on_count is " + str(on_count))
        while 1:
            self.myprint("waiting change on sensor " + self.sensorName(sensor))
            self.waitChange([sensor])
            sensorstate = sensor.getKnownState()
            self.myprint(">>countTrucks: sensor state is " + self.stateName(sensorstate)) 
            if sensorstate == INACTIVE and state_to_use == self.stateName(sensorstate):
                self.myprint ("off_count is @x " + str(off_count))
                off_count += 1
                self.myprint ("off_count is @y " + str(off_count))
                if off_count == noTrucksToCount:
                    self.myprint("Bingo count is " + str(off_count))
                    self.setSpeed(self.stop)
                    self.dedent()
                    break
                else: 
                    self.myprint ("off_count is @z " + str(off_count))                
                    self.myprint(">>countTrucks: ignoring sensor @1, off_count is " + str(off_count) + " noTrucksToCount " + str(noTrucksToCount))
                    self.myprint(">>countTrucks: ignoring sensor @2, sensor state is " + self.stateName(sensorstate)) 
            elif sensorstate == ACTIVE and state_to_use == self.stateName(sensorstate):
                on_count+=1
                self.myprint(">>countTrucks: sensor on_count " + self.stateName(sensorstate) + " on_count = " + str(on_count))
                self.myprint("noTrucksToCount " + str(noTrucksToCount))
                if on_count == noTrucksToCount:
                    self.myprint("Bingo on_count is " + str(on_count))
                    self.setSpeed(self.stop)
                    self.dedent()
                    break
                else:
                    self.myprint(">>countTrucks: ignoring sensor @1a, on_count is " + str(on_count) + " noTrucksToCount " + str(noTrucksToCount))
                    self.myprint(">>countTrucks: ignoring sensor @2a, sensor state is " + self.stateName(sensorstate)) 
            else:
                self.myprint(">>countTrucks: ignoring sensor @1b, off_count is " + str(off_count) + " noTrucksToCount " + str(noTrucksToCount))
                self.myprint(">>countTrucks: ignoring sensor @2b, on_count is " + str(on_count))
                self.myprint(">>countTrucks: ignoring sensor @3b, sensor state is " + self.stateName(sensorstate)) 
                


           

    # def disconnect(self, Branch):
        # self.myprint ("in disconnect ")
        # self.throttle.setSpeedSetting(0)
        # self.pause(1) # pause for 1 sec
  
        
              

    def swapRouteSameDirectionTravelling(self, fromBranch, toBranch):
        self.indent()
        self.myprint ("in swapRouteSameDirectionTravelling ")
        self.setDirection(fromBranch, toBranch)
        self.dedent()

    def swapRouteOppDirectionTravelling(self, fromBranch, toBranch):
        self.indent()
        self.myprint ("in swapRouteOppDirectionTravelling ")
        self.setDirection(fromBranch, toBranch)
        self.dedent()



    def sensorName(self, sensor) :
        self.indent()
        #self.myprint ("in sensorName ")
        if sensor == self.sensor1:
            self.dedent()
            return "Sensor1"
        elif sensor == self.sensor2:
            self.dedent()
            return "Sensor2"
        elif sensor == self.sensor3:
            self.dedent()
            return "Sensor3"
        elif sensor == self.sensor4:
            self.dedent()
            return "Sensor4"
        else:
            self.dedent()
            return "Invalid"
    
    # Define routine to map status numbers to text
    def stateName(self, state) :
        self.indent()
        self.myprint ("in stateName ")
        if (state == ACTIVE) :
            self.dedent()
            return "ACTIVE"
        if (state == INACTIVE) :
            self.dedent()    
            return "INACTIVE"
        if (state == INCONSISTENT) :
            self.dedent()
            return "INCONSISTENT"
        if (state == UNKNOWN) :
            self.dedent()
            return "UNKNOWN"
        self.dedent()
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
        
    def moveTrucksAllAtOnce(self, noTrucksOnTrain, startsInBranch4, 
    fromBranch, destBranch, noTruckstoMove):
        self.indent()
        self.myprint ("in moveTrucksAllAtOnce ")
        if startsInBranch4 :
            noTrucksOnStack4 = self.noTrucksOnStack(pegs, 4)
            self.moveTrucks(noTrucksOnStack4,4,fromBranch)
            self.initialmove = False
            noTrucksOnTrain = noTrucksOnStack4
        
        if fromBranch != 4:
            noTrucks = self.moveTrucks(noTrucksOnTrain, noTruckstoMove, fromBranch, 4)
        if destBranch != 4:       
            noTrucks = self.moveTrucks(noTrucks, noTruckstoMove, 4, destBranch)
        self.dedent()
        
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
                # self.myprint("Hi")
                
            # if fromBranch != 4:
                # self.myprint("Hi")
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
    
        self.indent()
        self.myprint ("in setDirection ")
        self.setPoints(fromBranch,toBranch)
        if toBranch != 4:
            # set loco to forward
            self.myprint("Set Loco Forward")
            throttle.setIsForward(True)
        else:
            # set loco to reverse
            self.myprint("Set Loco backward")
            throttle.setIsForward(False)
        self.myprint ("end setDirection ")
        self.dedent()
            
    def changeDirection(self):

        self.indent()
        self.myprint ("in changeDirection ")
        global throttle
        if throttle.getIsForward():
            throttle.setIsForward(False)
            self.myprint("Changed direction, reverse")
        else:
            throttle.setIsForward(True)
            self.myprint("Changed direction, forward")
        self.dedent()
                    
    def setPoints(self, fromBranch, toBranch):
        self.indent()
        self.myprint ("in setPoints ")
        
        self.myprint("setting points fromBranch = " + str(fromBranch) + " toBranch = " + str(toBranch))
        if fromBranch == 4:
            if toBranch == 1:
                self.myprint("get point1 CLOSED")
                if self.point1.getState() != CLOSED:
                    self.myprint("set point1 CLOSED")
                    self.point1.setState(CLOSED)
                    self.waitMsec(3000)
            else:
                self.myprint("get point1 THROWN")
                if self.point1.getState() != THROWN:
                    self.myprint("set point1 THROWN")
                    self.point1.setState(THROWN)
                    self.waitMsec(3000)
            
            if toBranch == 3:
                self.myprint("get point2 CLOSED")
                if self.point2.getState() != CLOSED:
                    self.myprint("set point2 CLOSED")
                    self.point2.setState(CLOSED)
                    self.waitMsec(3000)
            else:
                self.myprint("get point2 THROWN")
                if self.point2.getState() != THROWN:
                    self.myprint("set point2 THROWN")
                    self.point2.setState(THROWN)
                    self.waitMsec(3000)
        else:
            self.setPoints(toBranch, fromBranch)      # only define what we need to do once 
        #self.myprint("end setting points: waiting 10 secs")
        #self.waitMsec(10000)
        self.myprint("end setting points")
        self.dedent()

    def setSensor(self, branch):
        self.indent()
        self.myprint ("in setSensor ")
        self.myprint("setting sensor")
        if branch == 1:
            sensor = self.sensor1
        if branch == 2:
            sensor = self.sensor2
        if branch == 3:
            sensor = self.sensor3
        if branch == 4:
            sensor = self.sensor4
        self.myprint("end setting sensor")
        self.dedent()
        return sensor
        
    def setSpeed(self, speed):
        global throttle
        self.indent()
        #self.myprint("in setSpeed")
        self.myprint("in set speed: setting to " + str(speed))
        #self.waitMsec(500)
        if throttle.getSpeedSetting() != speed:
            throttle.setSpeedSetting(speed) 
            self.myprint("end set speed to " + str(speed))
            self.waitMsec(3000)
        else:
            self.myprint("speed already at " + str(speed))
        
        self.dedent()
        
    def setSpeedSetDelay(self, speed, delay):
        global throttle
        self.indent()
        #self.myprint("in setSpeed")
        self.myprint("in set speed: setting to " + str(speed))
        #self.waitMsec(500)
        if throttle.getSpeedSetting() != speed:
            throttle.setSpeedSetting(speed) 
            self.myprint("end set speed to " + str(speed) + "with delay " + str(delay))
            self.waitMsec(delay)
        else:
            self.myprint("speed already at " + str(speed))
        
        self.dedent()        
        
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
        self.myprint('clicked')

                    

    # instructions = generate_instructions()
    
    # for position in instructions:
        # if type(position[0]) is str:
            # #this is a command for the train
            # self.myprint("in test3")
            # self.myprint ("stop_program = " ,stop_program)
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
    i = 0
    grey = (255 - 100, 255 - 100, 255 - 100)
    pygame.draw.rect(
        screen,
        # Smaller pegs are ligher in color
        #(255-pegwidth*base_width, 255-pegwidth*base_width, 255-pegwidth*base_width),
        grey,
        #pyj2d.locals.blue,
        (
          start_y - peg_height * i,         # Pegs are one on top of the other, height depends on iteration 
          start_x + (SPACE_PER_PEG - 4 * base_width)/2 , # Handles alignment putting pegs in the middle, like a piramid
         
          #pegwidth*base_width,
          peg_height,
          4*base_width
          
        )
    )
    for i, pegwidth in enumerate(pegs):
        #print ("enumerate pegs",i)
        #pegwidth = pegs[i] * base_width
        #self.factor = 1
        grey = (255 - 100, 255 - 100, 255 - 100)
        pygame.draw.rect(
            screen,
            # Smaller pegs are ligher in color
            #(255-pegwidth*base_width, 255-pegwidth*base_width, 255-pegwidth*base_width),
            grey,
            #pyj2d.locals.blue,
            (
              start_x + (SPACE_PER_PEG - 4 * base_width)/2 , # Handles alignment putting pegs in the middle, like a piramid  
              start_y - peg_height * i,         # Pegs are one on top of the other, height depends on iteration
              4*base_width
              peg_height
            )
        )
        # draw the truck number
        print("xx")
        font = pygame.font.SysFont('Arial', 12)
        print("yy")
        xcoord = start_x + (SPACE_PER_PEG - pegwidth* base_width)/2 + pegwidth* base_width/2 - base_width/3 
        ycoord = start_y - peg_height * i + 3
        black = (0,0,0)
        screen.blit(font.render(str(pegwidth), True, black), (xcoord, ycoord))

        

        

    
def setup(pegs, rpegs, noPegs):
    print ("setup")
    #for i in range(0,2):
    #    assert len(pegs[i]) == noPegs[i], 'not enough disks on peg'
    yield pegs
    #now run the shunting puzzle
    print ("starting TimeSaver")
    timesaver = TimeSaver(pegs, rpegs)

    #don't need these
    #ingle.init_position_branch()
    print ("starting solvePuzzle")
    for p in timesaver.solvePuzzle():
        yield p
    print ("end of setup")

    #assert ingle.positions.count(1) == 1
    #assert ingle.branches.count(1) == 5
    #assert ingle.branches.count(2) == 3


def setupBlocks(noPegs, base_width, peg_height, sleeping_interval):
    # pegs = [[i  for i in reversed(range(1, noPegs[0]+1))],
    #         #[i  for i in reversed(range(noPegs[0]+1, noPegs[0]+ noPegs[1]+1))],
    #         [1,2,3],[],[]]
    #         #[i  for i in reversed(range(noPegs[0]+ noPegs[1]+1, noPegs[0]+ noPegs[1]+ noPegs[2]+1))],
    #         #[i  for i in reversed(range(noPegs[0]+ noPegs[1]+ noPegs[2]+1, noPegs[0]+ noPegs[1]+ noPegs[2]+ noPegs[3]+1))]]
    
    print ("hi1")
    #this is what we have
    pegs = [[3],[2,1],[4],[],[],[0],[5]]
    #this is what we need
    rpegs = [[1,4],[3],[5],[0],[],[],[2]]

    white = (255, 255, 255)
    black = (0,0,0)
    positions = setup(pegs, rpegs, noPegs)

    pygame.init()
    screen = pygame.display.set_mode( (650, 250) )
    pygame.display.set_caption('Timesaver')
    index = 0
    print("setupblocksa index != 1 " + str(index))
    font = pygame.font.SysFont('Arial', 25)
    for position in positions:

        screen.fill(white)
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
            # #this is a command for the train
            # print("setupblocksb index = " + str(index))
            # index += 1
            # print("setupblocksc index = " + str(index))
            # print (">> setup Blocks: position = " )
            # print (position)
            # print("setupblocksd index = " + str(index))
            # if index == 1:
                # print("setupblockse index == 1 " + str(index))
                # print("setupblocks index = 1")
                # t.decide_what_to_do_first()
            # print("setupblocksf index = " + str(index))
            # self.noTrucksOnTrain = t.decide_what_to_do(position)
            
            # ##train.update_position(position)
            pass
        else:
            print("setupblocksg index != 1 " + str(index))
            print (">> setup Blocks2: position = " )
            print (position)
            for i, pile in enumerate(position):
                print("i=",i)
                if i == 0: 
                    starty = 50
                    j = 0
                    startdraw = 0
                    enddraw = 3
                    vstartdraw = 1.1
                    venddraw = 1
                elif i == 1:
                    starty = 50
                    j = 2;
                    startdraw = 0
                    enddraw = 3
                    vstartdraw = 2
                    venddraw = 1 
                elif i == 2:
                    starty = 100
                    j = 1
                    startdraw = 0
                    enddraw = 1
                    vstartdraw = 0
                    venddraw = -.1 
                elif i == 3 or i== 4 or i == 5:
                    starty = 150
                    j = i - 3
                    startdraw = 0
                    enddraw = 3
                    vstartdraw = 1.1
                    venddraw = 1
                elif i == 6:
                    starty = 200
                    j = 0
                    startdraw = 0
                    enddraw = 1
                    vstartdraw = 2
                # print ("J=",j)
                # print("pile=",pile)
                # print ("starty=",starty)
                startx = 20 + SPACE_PER_PEG * (j+1)
                display_pile_of_pegs(pile, startx , starty, peg_height, 
                screen, base_width)
                #draw the track
                h = 30
                if i == 0  or i == 2 or i == 3 or i == 6:
                    pygame.draw.line(screen, (0,0,0), (startx+ startdraw * SPACE_PER_PEG,starty+peg_height ), 
                    (startx+enddraw * SPACE_PER_PEG, starty+peg_height), 2)
                if i == 0 or i == 2 or i == 3:
                    pygame.draw.line(screen, (0,0,0), (startx+ vstartdraw * SPACE_PER_PEG,starty+peg_height ), 
                    (startx+venddraw * SPACE_PER_PEG, starty+peg_height+50), 2)
                if i == 2:
                    pygame.draw.line(screen, (0,0,0), (startx+ 1 * SPACE_PER_PEG,starty+peg_height ), 
                    (startx+1.1 * SPACE_PER_PEG, starty+peg_height+50), 2)
                   
                
            pygame.display.update()
            time.sleep(sleeping_interval)

    pygame.quit()

def run_timesaver():
    print ("lo")
    #doctest.testmod()
    setupBlocks(
        noPegs = 6,
        base_width = 10,
        peg_height = 20,
        sleeping_interval = 1
    )
    print ("end of run_timesaver")
    
def setup_thread():
    print ("hi")
    t = threading.Thread(target=run_timesaver, name="run TimeSaver")
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
    import sys;sys.path.append(r'C:\Users\bill\.p2\pool\plugins\org.python.pydev.core_7.2.1.201904261721\pysrc')
    import pydevd;pydevd.settrace()
    t = Move_train()
    t.start()
    t.waitMsec(5000)
    print(Move_train().__dict__)
    win = Mywindow()
    win.setVisible(1)
    setup_thread() 