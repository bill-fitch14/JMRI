import java
from javax.swing import JOptionPane

class Speak:

    ## ***********************************************************************************

    ## sound routines

    ## ***********************************************************************************

    def speak(self, msg):
        os = self.get_operating_system()
        if os == "WINDOWS":
            self.speak_windows(msg)
        elif os == "LINUX":
            self.speak_linux(msg)
        elif os == "MAC":
            self.speak_mac(msg)

    def get_operating_system(self):
        #detecting the operating system using `os.name` System property
        os = java.lang.System.getProperty("os.name")
        os = os.lower()
        if "win" in os:
            return "WINDOWS"
        elif "nix" in os or "nux" in os or "aix" in os:
            return "LINUX"
        elif "mac" in os:
            return "MAC"
        return None

    def speak_windows(self,msg) :
        try:
            cmd1 = "Add-Type -AssemblyName System.Speech"
            cmd2 = '$SpeechSynthesizer = New-Object -TypeName System.Speech.Synthesis.SpeechSynthesizer'
            cmd3 = "$SpeechSynthesizer.Speak('" + msg + "')"
            cmd = cmd1 + ";" + cmd2 + ";" + cmd3
            os.system("powershell " + cmd )
        except:
            msg = "Announcements not working \n Only supported on windows versions with powershell and SpeechSynthesizer"
            JOptionPane.showMessageDialog(None, msg, "Warning", JOptionPane.WARNING_MESSAGE)

    def speak_mac(self, msg):
        try:
            java.lang.Runtime.getRuntime().exec("say {}".format(msg))
        except:
            msg = "Announcements not working \n say not working on your Mac"
            JOptionPane.showMessageDialog(None, msg, "Warning", JOptionPane.WARNING_MESSAGE)

    def speak_linux(self, msg):
        try:
            #os.system("""echo %s | spd-say -e -w -t male1""" % (msg,))
            #os.system("""echo %s | spd-say -e -w -t female3""" % (msg,))
            #os.system("""echo %s | spd-say -e -w -t child_male""" % (msg,))
            os.system("""echo %s | spd-say -e -w -t child_female""" % (msg,))  #slightly slower
        except:
            msg = "Announcements not working \n spd-say not set up on your linux system"
            JOptionPane.showMessageDialog(None, msg, "Warning", JOptionPane.WARNING_MESSAGE)