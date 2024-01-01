from functools import wraps
import threading
from threading import Thread
import time
import functools
import sys
import inspect, itertools
from collections import OrderedDict
#from javax.swing import JOptionPane
import globals as glb

stop_flag = False
glb_threadNo = 0


#reference https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
class thread_with_trace(threading.Thread): 
  def __init__(self, *args, **keywords): 
    threading.Thread.__init__(self, *args, **keywords) 
    self.killed = False
  
  def start(self): 
    self.__run_backup = self.run 
    self.run = self.__run       
    threading.Thread.start(self) 
  
  def __run(self): 
    sys.settrace(self.globaltrace) 
    self.__run_backup() 
    self.run = self.__run_backup 
  
  def globaltrace(self, frame, event, arg): 
    if event == 'call': 
      return self.localtrace 
    else: 
      return None
  
  def localtrace(self, frame, event, arg): 
    if self.killed:
      print("in local trace")
      if event == 'line': 
        raise SystemExit() 
    return self.localtrace 
  
  def kill(self): 
    self.killed = True

def indent1(function_name):
    global indentno
    # global indenta
    # global prompt, prompt1
    if function_name == "decide_what_to_do_first":
        indentno = 0

    setprompt(function_name)

    # y = [x[3] for x in inspect.stack()]
    # is_there_a_truck_in_hierarchy = y.count("is_there_a_truck")
    # count_at_spur_in_hierarchy = y.count("count_at_spur")
    # rectify_matters_in_hierarchy = y.count("rectify_matters")

    # if is_there_a_truck_in_hierarchy:

    # if rectify_matters_in_hierarchy > 0:
    #     prompt = ">>thread rectify: "
    #     prompt1 = "<<thread rectify: "
    # elif is_there_a_truck_in_hierarchy > 0:
    #     prompt = ">>thread truck: "
    #     prompt1 = "<<thread truck: "
    # elif count_at_spur_in_hierarchy > 0:
    #     prompt = ">>thread count: "
    #     prompt1 = "<<thread count: "
    # else:
    #     prompt = ">>>>>>>calling: "
    #     prompt1 = "<<<<<<<called:  "
    # elif count_at_spur_in_hierarchy:
    #     indenta = 20
    # else:
    #     indenta = 0
    indentno = indentno + 2

def dedent1():
    global indentno
    global indenta
    # global prompt, prompt1
    indentno = indentno - 2
    indenta = 0

def setprompt(function_name):
    global prompt, prompt1
    global indenta
    function_names_in_stack = [x[3] for x in inspect.stack()]
    # print "a", function_names_in_stack
    # print function_name
    function_names_in_stack.append (function_name)
    is_there_a_truck_in_hierarchy = function_names_in_stack.count("is_there_a_truck")
    count_at_spur_in_hierarchy = function_names_in_stack.count("count_at_spur")
    rectify_mid_in_hierarchy = function_names_in_stack.count("rectify_trucks_back_to_mid")
    rectify_siding_in_hierarchy = function_names_in_stack.count("rectify_trucks_back_to_siding")

    # indent 10 if is_there_a_tryck is in the hierarchy, 20 if count_at_spur in hierasrchy etc. Only one should appear at a time
    indenta = 10 * is_there_a_truck_in_hierarchy + 20 * count_at_spur_in_hierarchy + \
              10 * rectify_mid_in_hierarchy + 20 * rectify_siding_in_hierarchy
    glb.indenta = indenta   #store so myprint in module move_train can pick it up

    # if is_there_a_truck_in_hierarchy:
    if rectify_mid_in_hierarchy > 0:
        prompt = ">>thread recmid: "
        prompt1 = "<<thread recmid: "
    elif rectify_siding_in_hierarchy > 0:
        prompt = ">>thread recsid: "
        prompt1 = "<<thread recsid: "
    elif is_there_a_truck_in_hierarchy > 0:
        prompt = ">>thread truck: "
        prompt1 = "<<thread truck: "
    elif count_at_spur_in_hierarchy > 0:
        prompt = ">>thread count: "
        prompt1 = "<<thread count: "
    else:
        prompt = ">>>>>>>calling: "
        prompt1 = "<<<<<<<called:  "

# def _dump_args(func):
#     "This decorator dumps out the arguments passed to a function before calling it"
#     argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
#     fname = func.func_name
#     def echo_func(*args,**kwargs):
#         print fname, "(", ', '.join(
#             '%s=%r' % entry
#             for entry in zip(argnames,args[:len(argnames)])+[("args",list(args[len(argnames):]))]+[("kwargs",kwargs)]) +")"
#     return echo_func
def displayMessage(msg, f, title = ""):
    global display_message_flag

    if 'display_message_flag' not in globals():
        display_message_flag = False

    # if display_message_flag:
    if False:
        s = JOptionPane.showOptionDialog(None,
                                         msg,
                                         title,
                                         JOptionPane.YES_NO_OPTION,
                                         JOptionPane.PLAIN_MESSAGE,
                                         None,
                                         ["OK"],
                                         None)
        if s == JOptionPane.CLOSED_OPTION:
            f("dud arg")    #crash
            # crashhere
        return s

display_flag = False

def print_name(print_flag = True):
    def _print_name(f):
        # prints the parameters of the def and the values,
        # provided the decorator @print_name() has been placed before the function
        # and provided print_flag (see below) has been set Trur
        # optionally displays a message box with the parameters and values if display_flag is set True
        @wraps(f)
        def wrapper(self, *args):
            global display_flag
            global indentno, indenta
            indent1(f.__name__)
            if f.__name__ == "update_displays":
                display_flag = False
            else:
                display_flag = False
            #print_flag = True
            # if print_flag1 == "True":
            #     print_flag = True
            # else:
            #     print_flag = False

            if print_flag:
                # print "indenta" , indenta
                indentno1 = indentno + indenta
                if indentno%2 == 0:
                    # print "calling function " + str(inspect.stack()[1][3])
                    print("| " * (indentno1/2) + prompt),
                else:
                    print("| " * (indentno1/2) + "| " * indentno1 % 2 + prompt),
                print("{}".format(f.__name__)),
                # print("{}({})".format(f.__name__, ','.join([str(args)])))
                args_name = inspect.getargspec(f)[0]
                del args_name[0]
                args_mod = [x if len(str(x)) < 300 else 'too large to display nicely' for x in args]
                ordered_list = zip(args_name, args_mod)
                print ordered_list
            if display_flag:
                #display args list in pop up
                msg = ordered_list
                title = f.__name__
                # displayMessage(msg, f, title)

            g = f(self, *args)
            if print_flag:
                setprompt(f.__name__)
                if indentno1%2 == 0:
                    print("| " * (indentno1/2) + prompt1 + f.__name__ )
                else:
                    print("| " * (indentno1/2) + "| " * indentno1 % 2 + prompt1 + f.__name__ )
                if f.__name__ == "moveTrucksOneByOne": display_flag = False
            dedent1()
            return g
        return wrapper
    return _print_name

def alternativeaction(alt_function_name, *val_names):
    def _alternativeaction(f):
        @wraps(f)
        def wrapper(self, *args):
            print( "in alt_action - nothing required before call")
            self.myprint3( "in alt_action - nothing required before call")
            self.myprint3(  "alt action is function " + alt_function_name)
            stop_flag=f(self, *args)
            # print( "in alt_action - calling the alternative action code if required")
            # print( "stop_flag = ", stop_flag)
            #
            # # get the function to be called
            # # self.myprint( "sensor_name",val_names)
            # print( "alt_function_name",alt_function_name)
            # altfunc = getattr(self, alt_function_name)
            # print ("altfunc" , altfunc.__name__)
            # # get the parameters of the function (must be a class function)
            # i = 0
            # v = []
            # for val_name in val_names:
            #     print ("val_names", val_names)
            #     # print ("*val_names", *val_names)
            #     print ("val_name", val_name)
            #     try:
            #         v.append( getattr(self, val_name))
            #         print ("getattr(self, val_name)", getattr(self, val_name))
            #         print("v", v)
            #         i+=1
            #     except:
            #         print ("failed to getattr ", val_name)
            #
            # print ("function parameters =",v)
            # # print("test",x1, x1!= None)
            # # is_exception = (x1 != None)
            # # print("aa1", is_exception)
            
            # call alt_func if the timer stopped unexpectedly
            if stop_flag == True:

                altfunc = getattr(self, alt_function_name)
                self.myprint4("Timer stopped unexpectedly, taking alternative action", alt_function_name)
                v = []
                for val_name in val_names:
                    try:
                        v.append( getattr(self, val_name))
                    except:
                        self.myprint0 ("failed to getattr ", val_name)
                altfunc(*v)
                self.myprint4("altfunc finished")
            else:
                # self.myprint( "func completed OK, not calling altfunc")
                self.myprint4("we have not timed out, not calling alternative function, completed OK", alt_function_name)
                    
        return wrapper
    return _alternativeaction
    
# timeout uses timeout0 if count == 0, if count > 0 timeout uses timeoutn

def timeout(timeout):
# def timeout(timeout0, timeoutn=0, count_name = "unknown"):
    def _timeout(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            global stop_flag
            global glb_timeout
            global glb_threadNo

            def newFunc():
                global res
                global glb_timeout
                print "in new func"
##                print ("args[0]=",args[0])
                print "a"
                res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, glb_timeout))]
                try:
                    print "jim"
                    print "calling function", func.__name__
                    res[0] = func(self, *args, **kwargs)
                    print("continued=",res[0])
                except Exception, e:
                    res[0] = e
                    print("could not run function=", func.__name__, res[0])
                return res[0]

            # if count_name != "unknown": count = getattr(self, count_name)
            # else:                       count = 0
            # stop_flag=False
            # if count == 0:  glb_timeout = timeout0
            # else:           glb_timeout = timeoutn
            glb_timeout = float(timeout)/1000.0
            print ("glb_timeout", glb_timeout)
            glb_threadNo += glb_threadNo
            threadName = "ThreadNo"+str(glb_threadNo)
            print ("threadName", threadName)
            t = thread_with_trace(target=newFunc, name = threadName)
            t.daemon = True
            try:
                t.start()
                t.join(glb_timeout)
                print("joined in timeout: glb_timeout = ", glb_timeout)
            except Exception, je:
                print 'error starting thread'
                raise je

            ret = res[0]
            print("stopped",ret)
            if isinstance(ret, BaseException):
                print("need to take alternative action1")
                t.kill()  # stop the daemon thread now we have timed out
                print ("setting stop flag true")
                stop_flag=True
                print("stop_flag=",stop_flag)

            #t=None
            return stop_flag

        return wrapper
    return _timeout

               
# variableTimeout is called 
# @variableTimeout("timeout_stored")
# or @variableTimeout(timeout_name) where timeout_name = "timeout_stored" is declared in the class
# or just @variableTimeout()
# in all cases timeout_stored needs to be dclared in the calling function by calling
# self.storeTimeout(2) or similar where storeTimeout is declared in the class as

#   def storeTimeout(self, timeout):
#        self.timeout_stored = timeout
#        #self.timeout_name = "timeout_stored"    #this is done at declaration time 

# @print_name()
# def variableTimeout(timeout_name = "timeout_stored"):
#
#     def deco(func):
#         @wraps(func)
#         def wrapper(self, *args, **kwargs):
#             global stop_flag
#             global glb_timeout
#             global glb_threadNo
#
#             def newFunc():
#                 global res
#                 global glb_timeout
#                 print "in new func"
#                 print ("args[0]=",args[0])
#                 res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, glb_timeout))]
#                 try:
#                     res[0] = func(self, *args, **kwargs)
#                     print("continued=",res[0])
#                 except Exception, e:
#                     res[0] = e
#                     print("could not run function=",res[0])
#                 return res[0]
#
#             print("timeout_name = " , timeout_name)
#             glb_timeout = int(getattr(self, timeout_name))
#
#             print ("gbl_timeout = " + str(glb_timeout))
#
#             glb_threadNo += glb_threadNo
#             threadName = "ThreadNo"+str(glb_threadNo)
#             t = thread_with_trace(target=newFunc, name = threadName)
#             t.daemon = True
#             try:
#                 t.start()
#                 t.join(glb_timeout)
#             except Exception, je:
#                 print 'error starting thread'
#                 raise je
#
#             ret = res[0]
#             print("stopped",ret)
#             if isinstance(ret, BaseException):
#                 print("need to take alternative action1")
#                 t.kill()  # stop the daemon thread now we have timed out
#                 stop_flag=True
#                 print("stop_flag=",stop_flag)
#
#             #t=None
#             return stop_flag
#
#         return wrapper
#     return deco

def variableTimeout(timeout_name):
    def _timeout(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            global stop_flag
            global glb_timeout
            global glb_threadNo

            def newFunc():
                global res
                global glb_timeout
                res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, glb_timeout))]
                try:
                    res[0] = func(self, *args, **kwargs)
                except Exception, e:
                    res[0] = e
                    self.myprint4("could not run function=", func.__name__, res[0])
                return res[0]

            #start here
            stop_flag = False
            self.myprint4("getting timeout_name", timeout_name)
            glb_timeout = float(getattr(self, timeout_name))/1000.0
            self.myprint4 ("starting with limit of glb_timeout", glb_timeout)
            glb_threadNo += 1
            threadName = "ThreadNo" + str(glb_threadNo)
            self.myprint4("threadName", threadName)
            t = thread_with_trace(target=newFunc, name = threadName)
            t.daemon = True
            try:
                t.start()
                t.join(glb_timeout)
            except Exception, je:
                self.myprint4('error starting thread')
                raise je

            ret = res[0]
            self.myprint4("stopped",ret)
            if isinstance(ret, BaseException):
                self.myprint4("need to take alternative action1 in variableTimeout")
                t.kill()  # stop the daemon thread now we have timed out
                self.myprint4 ("setting stop flag true")
                stop_flag=True
                self.myprint4("stop_flag=",stop_flag)

            #t=None
            return stop_flag

        return wrapper
    return _timeout

from time import sleep
class foo():

    @print_name()
    #@variableTimeout("delay")
    @timeout(300)
    @alternativeaction("jim")
    def fred(self):
        self.del1()
        print("got here")
        sleep(0.1)
        print("got here")
        sleep(0.1)
        print("got here")
        sleep(0.1)
        print("got here")
        sleep(0.1)
        print("got here")
        sleep(0.1)
        print("got here")
        sleep(0.1)

    def del1(self):
        self.delay = "300"
        print "delay", self.delay




    def jim(self):
        print("called jim")





if __name__ == "__main__":
    global indentno
    global res
    indentno = 0
    res = [1,2]
    print("Hello, World!")
    fo = foo()
    fo.del1()
    fo.fred()

                
                
                

