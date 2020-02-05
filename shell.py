import sys
import os

# PCB[16]
# ready list - 3lv
# rcb[4] 
# 0, 1 = 1
# 2 = 2
# 3 = 3



class Process:
    def __init__(self):
        self.PCB = []
        self.RCB = []
        self.RL = []
        self.currentProcess = None

    def write(self, i):
        with open("testoutput.txt", "a+") as file:
            if i == 0:
                if os.stat("testoutput.txt").st_size > 0:
                    file.write("\n" + str(i) + " ")
                else:
                    file.write("0 ")
            else:
                file.write(str(i))
                
    def init(self):
        print("process 0 created")
        self.write(0)

    def create(self, priority):
        self.PCB = [0]*16
        self.RCB = [1,1,2,3]
        # RL = []
        self.currentProcess = 0

        with open("testoutput.txt", "a+") as file:
            file.write(str(priority) + " ")
        print("process %d running" % self.currentProcess)

    def destroy(self, process):
        pass

    def request(self, resource, units): #has sched
        pass

    def release(self, resource, units):
        pass

    def timeout(self):
        pass

    def scheduler(self):
        pass

    def shell(self):
        with open(sys.argv[1], "r") as file:
            for line in file:
                line = line.split()

                if (len(line) > 0):
                    if line[0] == "in":
                        self.init()
                    elif line[0] == "cr":
                        self.create(4)
                    # elif line[0] == "de":
                    #     destroy()
                    # elif line[0] == "rq":
                    #     request()
                    # elif line[0] == "rl":
                    #     release()
                    # elif line[0] == "to":
                    #     timeout()

run = Process() 
run.shell()