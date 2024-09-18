
class OptionDialog( jmri.jmrit.automat.AbstractAutomaton ) :
    CLOSED_OPTION = False
    logLevel = 0

    def List(self, title, list_items):
        list = JList(list_items)
        list.setSelectedIndex(0)
        i = []
        self.CLOSED_OPTION = False
        options = ["OK"]
        while len(i) == 0:
            s = JOptionPane.showOptionDialog(None,
                                             list,
                                             title,
                                             JOptionPane.YES_NO_OPTION,
                                             JOptionPane.PLAIN_MESSAGE,
                                             None,
                                             options,
                                             options[0])
            if s == JOptionPane.CLOSED_OPTION:
                self.CLOSED_OPTION = True
                if self.logLevel > 1 : print "closed Option"
                return
            i = list.getSelectedIndices()
        index = i[0]
        return list_items[index]


    #list and option buttons
    def ListOptions(self, list_items, title, options):
        list = JList(list_items)
        list.setSelectedIndex(0)
        self.CLOSED_OPTION = False
        s = JOptionPane.showOptionDialog(None,
                                         list,
                                         title,
                                         JOptionPane.YES_NO_OPTION,
                                         JOptionPane.PLAIN_MESSAGE,
                                         None,
                                         options,
                                         options[1])
        if s == JOptionPane.CLOSED_OPTION:
            self.CLOSED_OPTION = True
            return
        index = list.getSelectedIndices()[0]
        return [list_items[index], options[s]]

        # call using
        # list_items = ["list1","list2"]
        # options = ["opt1", "opt2", "opt3"]
        # title = "title"
        # result = OptionDialog().ListOptions(list_items, title, options)
        # list= result[0]
        # option = result[1]
        # print "option= " ,option, " list = ",list

    def variable_combo_box(self, options, default, msg, title = None, type = JOptionPane.QUESTION_MESSAGE):


        result = JOptionPane.showInputDialog(
            None,                                   # parentComponent
            msg,                                    # message text
            title,                                  # title
            type,                                   # messageType
            None,                                   # icon
            options,                                # selectionValues
            default                                 # initialSelectionValue
        )

        return result


    def displayMessage2(self, msg, title = ""):
        self.displayMessage(msg, "", False)
    def displayMessage1(self, msg, title = ""):
        self.displayMessage(msg, "", False)

    def displayMessage(self, msg, title = "", display = False):
        global display_message_flag

        if 'display_message_flag' not in globals():
            display_message_flag = True

        # if display_message_flag:
        if display:

            s = JOptionPane.showOptionDialog(None,
                                             msg,
                                             title,
                                             JOptionPane.YES_NO_OPTION,
                                             JOptionPane.PLAIN_MESSAGE,
                                             None,
                                             ["OK"],
                                             None)
            if s == JOptionPane.CLOSED_OPTION:
                title = "choose"
                opt1 = "continue"
                opt2 = "stop system"
                msg = "you may wish to abort"
                s1 = self.customQuestionMessage2str(msg, title, opt1, opt2)
                if s1 == opt2:
                    #stop system
                    Mywindow2()
                    StopMaster().stop_all_threads()

                return s
            #JOptionPane.showMessageDialog(None, msg, 'Message', JOptionPane.WARNING_MESSAGE)
            return s
        #     print "display_message_flag ", display_message_flag
        # else:
        #     print "display_message_flag ", display_message_flag

    def customQuestionMessage(self, msg, title, opt1, opt2, opt3):
        self.CLOSED_OPTION = False
        options = [opt1, opt2, opt3]
        s = JOptionPane.showOptionDialog(None,
                                         msg,
                                         title,
                                         JOptionPane.YES_NO_CANCEL_OPTION,
                                         JOptionPane.QUESTION_MESSAGE,
                                         None,
                                         options,
                                         options[2])
        if s == JOptionPane.CLOSED_OPTION:
            self.CLOSED_OPTION = True
            return
        return s

    def customQuestionMessage3str(self, msg, title, opt1, opt2, opt3):
        self.CLOSED_OPTION = False
        options = [opt1, opt2, opt3]
        s = JOptionPane.showOptionDialog(None,
                                         msg,
                                         title,
                                         JOptionPane.YES_NO_CANCEL_OPTION,
                                         JOptionPane.QUESTION_MESSAGE,
                                         None,
                                         options,
                                         options[0])
        if s == JOptionPane.CLOSED_OPTION:
            self.CLOSED_OPTION = True
            return
        if s == JOptionPane.YES_OPTION:
            s1 = opt1
        elif s == JOptionPane.NO_OPTION:
            s1 = opt2
        else:
            s1 = opt3
        return s1

    def customQuestionMessage2(self, msg, title, opt1, opt2):
        self.CLOSED_OPTION = False
        options = [opt1, opt2]
        s = JOptionPane.showOptionDialog(None,
                                         msg,
                                         title,
                                         JOptionPane.YES_NO_OPTION,
                                         JOptionPane.QUESTION_MESSAGE,
                                         None,
                                         options,
                                         options[0])
        if s == JOptionPane.CLOSED_OPTION:
            self.CLOSED_OPTION = True
            return
        return s

    def customQuestionMessage2str(self, msg, title, opt1, opt2):
        self.CLOSED_OPTION = False
        options = [opt1, opt2]
        s = JOptionPane.showOptionDialog(None,
                                         msg,
                                         title,
                                         JOptionPane.YES_NO_OPTION,
                                         JOptionPane.QUESTION_MESSAGE,
                                         None,
                                         options,
                                         options[1])
        if s == JOptionPane.CLOSED_OPTION:
            self.CLOSED_OPTION = True
            return
        if s == JOptionPane.YES_OPTION:
            s1 = opt1
        else:
            s1 = opt2
        return s1

    def customMessage(self, msg, title, opt1):
        self.CLOSED_OPTION = False
        options = [opt1]
        s = JOptionPane.showOptionDialog(None,
                                         msg,
                                         title,
                                         JOptionPane.YES_OPTION,
                                         JOptionPane.PLAIN_MESSAGE,
                                         None,
                                         options,
                                         options[0])
        if s == JOptionPane.CLOSED_OPTION:
            self.CLOSED_OPTION = True
            return
        return s

    def input(self,msg, title, default_value):
        options = None
        x = JOptionPane.showInputDialog( None, msg,title, JOptionPane.QUESTION_MESSAGE, None, options, default_value);
        #x = JOptionPane.showInputDialog(None,msg)
        return x

class modifiableJComboBox:

    def __init__(self,list, msg):
        #list = self.get_all_roster_entries()
        jcb = JComboBox(list)
        jcb.setEditable(True)
        JOptionPane.showMessageDialog( None, jcb, msg, JOptionPane.QUESTION_MESSAGE)
        self.ans = str(jcb.getSelectedItem())

    def return_val(self):
        return self.ans