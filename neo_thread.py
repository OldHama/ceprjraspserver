import threading
import neo_act as n
import actuator

class led_thread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.pattern = 0
        self.timing = 0
        self.bright = 0
        self.read_profile()
        
    def read_profile(self):
        file = open("profile.txt", 'r')
        pattern_name = file.readlines()
        file.close()
        self.pattern = pattern_name[0].replace('\n', '')
        self.timing = float(pattern_name[1].replace('\n', ''))
        self.bright = float(pattern_name[2].replace('\n', ''))
    
    def write_profile(self, msg):
        file = open("profile.txt", "w")
        file.write(msg)
        file.close()
        
    def run (self):
        while True:
            self.read_profile()
            if self.pattern == 'rainbow':
                n.rainbow_cycle(self.timing, self.bright)
            else:
                n.off()
            actuator.sleep(0.001)

