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
        self.PCB = [[]]*16
        self.RCB = [1,1,2,3]
        self.RL = [[], []]
        self.currentProcess = 0
        self.PCB[0] = [0]

        print("process 0 created")
        self.write(0)

    def create(self, priority):
        with open("testoutput.txt", "a+") as file:                
            if priority == 0 or self.PCB == None:
                file.write(-1)
                return

            # file.write(str(self.currentProcess) + " ")

        # get the next free process
        for i in range(0, len(self.PCB)):
            if len(self.PCB[i]) == 0:
                self.PCB[i] = [self.currentProcess]
                break

        self.PCB[self.currentProcess].append(i) # add the process
        self.RL[priority-1].append(i) # add to ready list
        print("process %d created" % i)

        for i in self.RL:
            if len(i) > 0:
                self.currentProcess = i[0]
                break

        with open("testoutput.txt", "a+") as file:
            file.write(str(self.currentProcess) + ' ')

    def destroy(self, process, total = 0): #can process 0 be destroyed?
        # if process == 0:
        #     total += len(self.PCB[0]) - 1
        #     return total

        # IM BASICALLY DESTROYING PROCESS 0, AND THIS SKIPS BECUZ LEN(PROCESS 0) > 1
        if len(self.PCB[process]) == 1:
            self.PCB[self.PCB[process].pop()].pop(1)
            return total + 1


        while len(self.PCB[process]) > 0:
            total += 1 
            self.destroy(self.PCB[process][0], total)

        # self.destroy(self.PCB[process][0])
        self.PCB[self.PCB[process].pop()].pop(1) #need to pop itself and everything after itself in its parent

        return total + 1

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
                        self.create(int(line[1]))
                    elif line[0] == "de":
                        print(self.destroy(int(line[1])), "process destroyed")
                    # elif line[0] == "rq":
                    #     request()
                    # elif line[0] == "rl":
                    #     release()
                    # elif line[0] == "to":
                    #     timeout()

        print(self.PCB)

run = Process() 
run.shell()

# a = [[], [10], [11, 2]]


# for x in a:
#     for y in x:
#         print(y)
