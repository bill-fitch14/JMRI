#@add_methods(myprint,mysound,indent,dedent,init)

#from timeout import alternativeaction, variableTimeout, print_name, timeout

import jmri
import java
import inspect

# def myprint(self, *args):
#     if False:     #set to True od False depending upon whether you want to print error messages
#         print(" " * self.indentno),
#         for arg in args:
#             print (arg),
#         print("")
#         # msg = " " * self.indentno
#         # #print(msg + "!")
#         # for arg in args:
#         #     msg = msg + " " + str(arg)
#
# def myprint2(self, *args):
#     # indent fro threads
#     function_names_in_stack = [x[3] for x in inspect.stack()]
#     # is_there_a_truck_in_hierarchy = y.count("is_there_a_truck")
#     # count_at_spur_in_hierarchy = y.count("count_at_spur")
#     is_there_a_truck_in_hierarchy = function_names_in_stack.count("is_there_a_truck")
#     count_at_spur_in_hierarchy = function_names_in_stack.count("count_at_spur")
#     rectify_mid_in_hierarchy = function_names_in_stack.count("rectify_trucks_back_to_mid")
#     rectify_siding_in_hierarchy = function_names_in_stack.count("rectify_trucks_back_to_siding")
#     # if is_there_a_truck_in_hierarchy:
#     # indenta = 10 * is_there_a_truck_in_hierarchy + 20 * count_at_spur_in_hierarchy
#     indenta = 10 * is_there_a_truck_in_hierarchy + 20 * count_at_spur_in_hierarchy + \
#               10 * rectify_mid_in_hierarchy + 20 * rectify_siding_in_hierarchy
#
#     # indent 2 spaced for each call
#     if True:     #set to True or False depending upon whether you want to print error messages
#         print(" " * self.indentno),
#         print(" " * indenta),
#         for arg in args:
#             print (arg),
#         print("")
#         # msg = " " * self.indentno + " " * indenta
#         # #print(msg + "!")
#         # for arg in args:
#         #     msg = msg + " " + str(arg)
#
# def myprint1(self, *args):
#
#     if self.display_message_flag == None:
#         self.display_message_flag = False
#
#     #if self.display_message_flag:
#     if False:
#         print(" " * self.indentno),
#         for arg in args:
#             print (arg),
#         print("")
#         msg = " " * self.indentno
#         #print(msg + "!")
#         for arg in args:
#             msg = msg + " " + str(arg)
#         #logging.debug(msg)
#     #     print "display_message_flag myprint1", self.display_message_flag
#     # else:
#     #     print "display_message_flag myprint1", self.display_message_flag
#
#
# # # use external "nircmd" command to "speak" some text  (I prefer this voice to eSpeak)
# # def speak(self,msg) :
#     # #uncomment next line for speech (Jenkins doesn't like this command)
#     # print("about to speak")
#     # java.lang.Runtime.getRuntime().exec('Z:\\ConfigProfiles\\jython\\sound2\\nircmd speak text "' + msg +'"')
#     # return
#
#
# def indent(self):
#
#     self.indentno = self.indentno + 2
#
# def dedent(self):
#     self.indentno = self.indentno - 2

