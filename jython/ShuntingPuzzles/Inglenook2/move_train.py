import jarray
import jmri
import java.beans
#import jmri.jmrit.automat.AbstractAutomaton as aa
import sys, os
from javax.swing import JFrame, JButton, JOptionPane


sys.path.append('Z:\\Config Profiles\\jython\\an inglenook puzzle')


class Move_train(jmri.jmrit.automat.AbstractAutomaton) :

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
        
        print"in C:\Users\bill_\Dropbox\Config Profiles\jython\an inglenook puzzle\move_train.py"
            
        try:
            print ("trying to set up sensors")
            #self.sensor1 = sensors.provideSensor("MS+N259E7;-N259E7")
            self.sensor1 = sensors.provideSensor("sensor1")
            print ("This is an success message! s1 set up")
            #self.sensor2 = sensors.provideSensor("MS+N259E6;-N259E6")
            self.sensor2 = sensors.provideSensor("sensor2")
            print ("This is an success message! s2 set up")
            #self.sensor3 = sensors.provideSensor("MS+N259E5;-N259E5")
            self.sensor3 = sensors.provideSensor("sensor3")
            print ("This is an success message! s3 set up")
            #self.sensor4 = sensors.provideSensor("MS+N259E8;-N259E8")
            self.sensor4 = sensors.provideSensor("sensor4")
            print ("This is an success message! s4 set up")
        except:
            print ("sensors not set!")
            
        try:
            print ("trying to set up points")
            'self.point1 = turnouts.provideTurnout("MT+N0E10;-N0E10")
            self.point1 = turnouts.provideTurnout("point1")
            'self.point2 = turnouts.provideTurnout("MT+N0E11;-N0E11")
            self.point2 = turnouts.provideTurnout("point2")
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
        

        # self.sensor1 = DebounceSensor()  # create one of these
        # self.sensor1.init('+N259E5','-N256E5', 0.5, 3) # invoke this for the sensor pair

        # self.sensor2 = DebounceSensor()  # create one of these
        # self.sensor2.init('NS775', 'ISNS775', 0.5, 3)  # invoke this for the sensor pair

        # self.sensor3 = DebounceSensor()  # create one of these
        # self.sensor3.init('NS775', 'ISNS775', 0.5, 3)  # invoke this for the sensor pair

        # self.sensor4 = DebounceSensor()  # create one of these
        # self.sensor4.init('NS775', 'ISNS775', 0.5, 3)  # invoke this for the sensor pair

    def handle(self):
        #train.init()
        print("in test1")       
        instructions = generate_instructions()
        print("in test2")   

        for position in instructions:
            if type(position[0]) is str:
                #this is a command for the train
                print("in test3")
                print ("stop_program = " ,stop_program)
                if stop_program == True:
                    pass
                    #self.dispose()   # there is no dispose function so it crashes - which is what we want
                t.decide_what_to_do(position)
        print("End of Program")
        while 1:
            pass
            
    def decide_what_to_do_first(self):
        #set up the trucks 5 in branch 3 and 3 in branch 2, and return to branch 4
        instruction_first = [generate_first_instructions]
        self.decide_what_to_do(instruction_first)
        
    def decide_what_to_do(self, instructions):
        print("inside what to do")
        print instructions
        if instructions[0] == "moveTrucksOneByOne":
            print(" about to moveTrucksOnebyOne ",instructions[1], instructions[2], instructions[3], instructions[4])
            self.moveTrucksOneByOne(instructions[1],instructions[2],instructions[3],instructions[4])
            pass
        elif instructions[0] == "move_trucks":
            print(" about to moveTrucks ",instructions[1], instructions[2], instructions[3], instructions[4])
            self.moveTrucks(instructions[1], instructions[2], instructions[3], instructions[4])
            pass
        else:
            pass
            
    def moveTrucks(self, noTrucksInitially, noTrucksToMove, fromBranch, destBranch):
        print("in movetrucks")
        print("Movetrucks",noTrucksInitially, noTrucksToMove, fromBranch, destBranch)
        if fromBranch != 4:
            print("in movetrucks 1")
            self.moveEngineToBranch(fromBranch, 4, noTrucksInitially)  #count from 0 so exclude engine
            #self.swapDirection()
            self.moveToDisconnectTrucks(noTrucksInitially, noTrucksToMove, destBranch)
            
        else:
            #self.moveEngineToBranch(fromBranch, destBranch, noTrucksToMove)
            print("in movetrucks 2")
            self.moveToDisconnectTrucks(noTrucksInitially, noTrucksToMove, destBranch)
        return noTrucksInitially + noTrucksToMove 

    # def noTrucksOnStack(self, pegs, branch_no):
        # noTrucks = len(pegs[branch_no - 1])
        # return noTrucks

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
        
        print ">>moveToDisconnectTrucks: noTrucksInitially " + str(noTrucksInitially) + \
        ", noTrucksToMove " + str(noTrucksToMove) + ", destBranch " + str(destBranch)
        
        # need to determine the direction to pick up or remove trucks from engine at from branch
        
        noTrucksToAdd = noTrucksToMove - noTrucksInitially
        noTrucksToCount = abs(noTrucksToAdd)
        print(">>moveToDisconnectTrucks: noTrucksToAdd " + str(noTrucksToAdd) + " noTrucksToCount " + str(noTrucksToCount))
        if noTrucksToAdd > 0:
            # picking up trucks
            print(">>!!!!moveToDisconnectTrucks: picking up " + str(noTrucksToAdd) + " trucks");
            self.countTrucksAndPosition(0, sensor, "ACTIVE")  #needs to be active since count is zero
            # need to go on 1/2 a truck here to connect
            
            #....
            
            self.setSpeed(self.stop)
            #need to check that have connected
            #change direction
            print(">>moveToDisconnectTrucks: slowed at first truck")
            self.setDirection(4, destBranch)
            self.countTrucksAndPosition(noTrucksToCount + 1, sensor, "INACTIVE")
            self.setSpeed(self.stop)
            print(">>moveToDisconnectTrucks: picked up trucks");
            # self.setSpeed(self.stop)
            # self.moveToDisconnectPosition(sensor) 
        else:
            #dropping off trucks
            print(">>!!!!moveToDisconnectTrucks: dropping off " + str(noTrucksToAdd) + " trucks");
            self.countTrucksAndPosition(noTrucksToCount, sensor, "ACTIVE")
            self.setSpeed(self.stop)
            # self.moveToDisconnectPosition(sensor) 
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

        # noTrucksInitially = noTrucksOnStack4
        # #noTrucksToMove = noTrucks
        # self.moveToDisconnectTrucks(noTrucksInitially,
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
        
throttle = None
stop_program = False
do_train_moves = False

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
            throttle.setSpeedSetting(0)
            print ("stop_program = " ,stop_program)

    def on_close(self, widget):
        print('clicked')

                    
print (__name__)
if __name__ == "__builtin__":
    def generate_instructions():
        #yield ["move_trucks", noTrucks, fromBranch, destBranch, self.pegs]
        # should be
        #moveTrucks(self, noTrucksInitially, noTruckstoMove, fromBranch, destBranch):
        yield ["move_trucks",  4,  4, 4, 3]
        yield ["move_trucks",  3,  1, 4, 1]
        yield ["move_trucks",  0,  0, 4, 1]
    
    win = Mywindow()
    win.setVisible(1)
    t = Move_train()
    print ("In move_train.py")
    print(Move_train().__dict__)
    t.start()
    
