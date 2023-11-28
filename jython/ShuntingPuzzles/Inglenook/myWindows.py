from javax.swing import JFrame, JButton, JOptionPane
import config
import threading
#from move_train import throttle, config.stop_program
# import pyj2d as pygame

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
        #global config.stop_program
        #global config.throttle
        print("clicked onclick")
        #if JOptionPane.showConfirmDialog(None,"Are you sure you want to exit","Exit", 
        #JOptionPane.YES_NO_OPTION) == JOptionPane.YES_OPTION:
        if 1==1:
            print ("Bye")
            
            config.stop_program = True

            config.throttle.setSpeedSetting(0)
            #print ("stopped" + "thread is", thread) 
            name = threading.currentThread().getName()
            print("Current thread is " + name)
            print ("config.stop_program = " ,config.stop_program)
            for thread in threading.enumerate():
                print(thread.name)
                if thread.name != "MainThread" \
                    and thread.name != "run Shunting Puzzle":
                    print(thread.name)
                    #if JOptionPane.showConfirmDialog(None,"do you want to kill thread?","Exit", 
                    #JOptionPane.YES_NO_OPTION) == JOptionPane.YES_OPTION:
                    if 1==1:
                        try:
                            thread.kill()
                            print("killed")
                        except:
                            print("exception - not killed")
                    else:
                        print("chose not to kill")

                    
                    #if JOptionPane.showConfirmDialog(None,"do you want to join thread?","Exit", 
                    #JOptionPane.YES_NO_OPTION) == JOptionPane.YES_OPTION:
                    #if thread != None:
                    #   try:
                    #       thread.join()
                    #       print("joined")
                    #   except:
                    #      print("exception - not joined")
                    #else:
                    #   print("thread not None")
                    #print ("stopped")
            pygame.quit()
            print ("pygame quitted")
            for thread in threading.enumerate():
                print(thread.name)
                #if thread.name != "MainThread": 
                    #thread.kill()
                    #thread.join()
                    #print ("stopped")
            #pygame.QUIT
            #
            #self.dispose()

    def on_close(self, widget):
        print('clicked')
        pygame.quit()
        self.dispose()


class Mywindow2(JFrame):

    def __init__(self):
        super(Mywindow2, self).__init__(windowClosing=self.on_close)
        self.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE)
        
        self.setSize(300,200)
        #self.setLocationRelativeTo(None) # None is null in Java
        self.setLocation(500,500)
        self.setTitle("Test")
        
        self.button=JButton('Click me to stop program', actionPerformed=self.on_click)
        self.add(self.button)

    def on_click(self,widget):
        #global config.stop_program
        #global throttle
        print("clicked onclick")
        #if JOptionPane.showConfirmDialog(None,"Are you sure you want to exit","Exit", 
        #JOptionPane.YES_NO_OPTION) == JOptionPane.YES_OPTION:
        if 1==1 :
            print ("Bye")
            
            config.stop_program = True
            #pygame.quit()
            config.throttle.setSpeedSetting(0)
            print ("config.stop_program = " ,config.stop_program)
            for thread in threading.enumerate():
                print(thread.name)
                if thread.name != "MainThread" \
                    and thread.name != "run Shunting Puzzle":
                    #thread.kill()
                    #thread.join()
                    print ("to be stopped")
            #pygame.quit()
            #print ("pygame quitted")
            #for thread in threading.enumerate():
                #print(thread.name)
                #if thread.name != "MainThread": 
                    #thread.kill()
                    #thread.join()
                    #print ("stopped")
            #self.dispose()
            
    def on_close(self, widget):
        print('clicked')
        self.dispose()        

                    
            
       