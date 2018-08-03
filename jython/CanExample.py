# Sample script to show how to send and receive CAN Frames
#
#
# Author: Bob Jacobsen, copyright 2008
# Author: Gert Muller, copyright 2012
#
# Part of the JMRI distribution

import jmri

import java


print "hello"




# First, example of receiving. Put a listener in place.
class MyCanListener (jmri.jmrix.can.CanListener) :
    def message(self, msg) :
        print "Sending own frame"

        print "ID: 0x"+java.lang.Integer.toHexString(msg.getHeader())
        print "content: ", msg.toString()
        print "..................................................................................."
        # this handles messages being sent by ignoring them
        return
    def reply(self, msg) :
        print "received Frame"
        print "ID: 0x"+java.lang.Integer.toHexString(msg.getHeader())
        print "content: ", msg.toString()
        print "..................................................................................."
        return
    
# Get the traffic controller
tc = None
 
# Old way first...
try:
  tc = jmri.jmrix.can.TrafficController.instance()
except:
  # Then the new way...
  try:
    tc = jmri.InstanceManager.getDefault(jmri.jmrix.can.CanSystemConnectionMemo).getTrafficController()
    print "traffic controller found"
  except:
    print "no traffic controller"
    tc = None
 
tc.addCanListener(MyCanListener())


# Send a frame
frame = jmri.jmrix.can.CanMessage(tc.getCanid())


frame.setNumDataElements(2)   # will load 2 bytes
frame.setElement(0, 0x45)
frame.setElement(1, 0x67)
if tc != None:
  tc.sendCanMessage(frame, None)
  print "CAN frame sent!"
else:
  print "Sorry, no Traffic Controller!"

