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
        
    
    
    def init(self):
        global throttle
        #speeds
        self.stop = 0
        self.slow = 0.1
        self.decouple = 0.2
        self.medium = 0.5
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
            self.sensor1 = sensors.provideSensor("MS+N259E7;-N259E7")
            print ("This is an success message! s1 set up")
            self.sensor2 = sensors.provideSensor("MS+N259E6;-N259E6")
            print ("This is an success message! s2 set up")
            self.sensor3 = sensors.provideSensor("MS+N259E5;-N259E5")
            print ("This is an success message! s3 set up")
            self.sensor4 = sensors.provideSensor("MS+N259E8;-N259E8")
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
        instruction_first = [generate_first_instructions]
        self.decide_what_to_do(instruction_first)
    
    def generate_first_instructions(self):
        # the move trucks instruction is shown commented out, so we can see what the yield does
        #moveTrucks(self, noTrucksInitially, noTruckstoMove, fromBranch, destBranch):
        yield ["move_trucks",  5,  5, 4, 3]
        #we move from branch 4 to branch 3 depositing all 5 trucks
        
    def decide_what_to_do(self, instructions):
        print("inside what to do")
        print instructions
        if instructions[0] == "moveTrucksOneByOne":
            self.moveTrucksOneByOne(instructions[1],instructions[2],instructions[3],instructions[4])
            pass
        elif instructions[0] == "move_trucks":
            print(" about to moveTrucks",instructions[1], instructions[2], instructions[3], instructions[4])
            self.moveTrucks(instructions[1], instructions[2], instructions[3], instructions[4])
            pass
        else:
            pass           
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
    def moveTrucks(self, noTrucksInitially, noTrucksToMove, fromBranch, destBranch):
        print("in movetrucks")
        print("Movetrucks",noTrucksInitially, noTrucksToMove, fromBranch, destBranch)
        if fromBranch != 4:
            print("in movetrucks 1")
            self.moveEngineToBranch(fromBranch, 4, noTrucksInitially)  #count from 0 so exclude engine
            #sself.swapDirection()
            self.moveToDisconnectTrucks(noTrucksInitially, noTrucksToMove, destBranch)
            
        else:
            #self.moveEngineToBranch(fromBranch, destBranch, noTrucksToMove)
            print("in movetrucks 2")
            self.moveToDisconnectTrucks(noTrucksInitially, noTrucksToMove, destBranch)
        return noTrucksInitially + noTrucksToMove 


    def moveEngineToBranch(self,fromBranch, toBranch, trucksToMove):
        print("In moveEngineToBranch")
        #set direction
        self.setDirection(fromBranch, toBranch)
        self.setPoints(fromBranch, toBranch)
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
        
    # def moveToDisconnectTrucks(self, noTrucksInitially,
                               # noTrucksToMove, fromBranch, toBranch ):
                               
    def decouple():
        self.setSpeed(self.stop)
        self.setDirection(fromBranch, toBranch)
        self.setSpeed(self.decouple)
        self.waitMsec(500)
        self.setSpeed(self.stop)
        self.setDirection(toBranch, fromBranch)
        self.setSpeed(self.decouple)
        self.waitMsec(1000)
        self.setSpeed(self.stop)
                               
    def moveToDisconnectTrucks(self, noTrucksInitially, noTrucksToMove, destBranch):
        
        #dest branch is never 4
        self.setDirection(4, destBranch)
        self.setPoints(4,destBranch)
        self.setSpeed(self.slow)
        sensor = self.setSensor(destBranch)
        
        # deed to determine the direction to pick up or remove trucks from engine at from branch
        
        noTrucksToAdd = noTrucksToMove - noTrucksInitially
        noTrucksToCount = abs(noTrucksToAdd)
        print(">>moveToDisconnectTrucks: noTrucksToAdd " + str(noTrucksToAdd) + " noTrucksToCount " + str(noTrucksToCount))
        if noTrucksToAdd > 0:
            # picking up trucks
            print(">>moveToDisconnectTrucks: picking up trucks");
            self.countTrucksAndPosition(0, sensor, "INACTIVE")
            self.setSpeed(self.stop)
            #need to check that have connected
            #change direction
            print(">>moveToDisconnectTrucks: stopped at first truck");
            self.setDirection(4, destBranch)
            self.countTrucksAndPosition(noTrucksToCount, sensor, "INACTIVE")
            self.setSpeed(self.stop)
            print(">>moveToDisconnectTrucks: picked up trucks");
            # self.setSpeed(self.stop)
            # self.moveToDisconnectPosition(sensor) 
        else:
            #dropping off trucks
            print(">>moveToDisconnectTrucks: dropping off trucks");
            self.countTrucksAndPosition(noTrucksToCount, sensor, "INACTIVE")
            # self.setSpeed(self.stop)
            #need to check that have connected
            print("DONE1");
            print(">>moveToDisconnectTrucks: dropped off trucks");
            # self.setDirection(Branch, 4)
            # self.moveToDisconnectPosition(sensor) 

    def countTrucksAndPosition(self, noTrucksToCount, sensor, state_to_use):
        print(">> countTrucksAndPosition: count trucks")
        self.countTrucks(noTrucksToCount, sensor, state_to_use)
        # wait 1 second for layout to catch up, then set speed
        print(">> countTrucksAndPosition: counted trucks, wait 5 secs")
        self.waitMsec(5000)       
        print(">> countTrucksAndPosition: self.moveToDisconnectPosition(sensor)")
        self.moveToDisconnectPosition(sensor)
        print(">> countTrucksAndPosition: moved to disconnect position, wait 5 secs")
        self.waitMsec(5000) 
                            
                            
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
                
    def moveToDisconnectPosition(self, sensor):
        if sensor == self.sensor1:
            self.moveBackToSensor(sensor, self.sensorOff)
        elif sensor == self.sensor2:
            self.moveBackToSensor(sensor, self.sensorOn)
        elif sensor == self.sensor3:
            self.moveBackToSensor(sensor, self.sensorOn)
            #need to move a little more
        else:
            pass  # sensor 4 does not need positioning 

    def moveBackToSensor(self, sensor, required_sensor_state):
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

                # noTrucksInitially = noTrucksOnStack4
                # noTrucksToMove = 1 # if noTruckstomove is +ve then picking up a truck

                # moveToDisconnectTrucks(noTrucksInitially,
                        # noTrucksToMove, fromBranch, 4) #move engine back so can disconnect

                # disconnectTrucks(noTrucksOnStack4, noTrucksToMove, fromBranch, i) 
                # disconnectSignal(fromBranch)
                # noOfTrucks = noTrucksInitially + noTrucksToMove
                # moveEngineToBranch(fromBranch, 4, )

            # if destBranch != 4:

                # swapDirectionTravelling(4, destBranch)

                # moveEngineToBranch(4, destBranch)
                # connectTrucks(destBranch)
                # # we have picked a truck up
                # noTrucksInitially = noTrucksOnStack4 + 1 

                # noTrucksToMove = -1  # deposit a truck

                # if noTrucksToMove>0: #remove truck
                    # swapRouteOppDirectionTravelling(destBranch, 4)
                    # moveToDisconnectTrucks(noTrucksInitially,
                            # noTrucksToMove, destBranch, 4)
                # else:
                    # moveToDisconnectTrucks(noTrucksInitially,
                            # noTrucksToMove, 4, destBranch)	

                # disconnectTrucks(noTrucksInitially,
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
        if fromBranch == 4:
            if toBranch == 3:
                self.point1.setState(CLOSED)
            else:
                self.point1.setState(THROWN)
            self.waitMsec(50)
            if toBranch == 1:
                self.point2.setState(CLOSED)
            else:
                self.point2.setState(THROWN)
            self.waitMsec(50) 
        else:
            self.setPoints(toBranch, fromBranch)      # only define what we need to do once     

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
        global throttle
        throttle.setSpeedSetting(speed)   
        print ("set throttle to " + str(speed))
        
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
    for position in positions:
        index += 1
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
            print "position = " 
            print position
            if index == 1:
                t.decide_what_to_do_first
            t.decide_what_to_do(position)
            #train.update_position(position)
            pass
        else:
            print (position)
            for i, pile in enumerate(position):
                display_pile_of_pegs(pile, 20 + SPACE_PER_PEG * i, 100, peg_height, screen, base_width)


                # if type(pile[1])== "str":
                    # #train.decide_what_to_do(pile)
                    # pass
                # else:
                    # display_pile_of_pegs(pile, 50 + SPACE_PER_PEG * i, 500, peg_height, screen, base_width)
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
        # #moveTrucks(self, noTrucksInitially, noTruckstoMove, fromBranch, destBranch):
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