import sys
import os

# PCB[16]
# ready list - 3lv
# rcb[4] 
# 0, 1 = 1
# 2 = 2
# 3 = 3


class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class Process:
    def __init__(self):
        # self.head = None # list of parent processes
        self.PCB = None # process
        self.RCB = None # resource 
        self.RL = None # ready list
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
        # self.head = []
        # self.head.append(Node(0))
        self.PCB = [0]*16
        self.RCB = [1,1,2,3]
        self.RL = []
        self.currentProcess = 0
        self.PCB[0] = 1

        print("process 0 created")
        self.write(0)

    def create(self, priority):
        with open("testoutput.txt", "a+") as file:
            file.write(str(self.currentProcess) + " ")
        
        for i in range(0, len(self.PCB)):
            if self.PCB[i] == 0:
                self.PCB[i] = 1
                break
        print("process %d created" % i)

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