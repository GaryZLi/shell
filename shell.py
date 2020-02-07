import sys
import os

# PCB = [[0, 1], [(0, 2), 2, 3], [(1, 1)], [(1, 1)]]
# RCB = [1, 1, 2, 3]
# PRL = [[0, 0, 0, 0], [0, 0, 0, 0], ]
class Process:
    def __init__(self):
        # self.head = None # list of parent processes
        self.ProcessList = None # process
        self.ResourceList = None # resource 
        self.ProcessListOfResources = None # process resource list
        self.ProcessResourceWL = None # resource waitlist
        self.ReadyList = None # ready list
        self.WaitList = None # waiting list
        self.currentProcess = None

    def write(self, i):
        with open("output.txt", "a+") as file:
            if i == 'init':
                if os.stat("output.txt").st_size > 0:
                    file.write("\n0 ")
                else:
                    file.write("0 ")
            else:
                file.write(str(i) + ' ')
                
    def init(self):
        self.ProcessList = [[]]*16
        self.ResourceList = [1,1,2,3]
        self.ProcessListOfResources = [[0 for _ in range(4)] for _ in range(16)] 
        self.ProcessResourceWL = [[] for _ in range(16)]
        self.ReadyList = [0, [], []]
        # self.WL = [0, [], [], []] ##
        self.WaitList = [[0], [], [], []]

        self.currentProcess = 0
        self.ProcessList[0] = [0]

        self.write('init')

        print("Created process:", 0)
        print("Process list:", self.ProcessList) 
        print("Resource list:", self.ResourceList)
        print("Process list and its resources:", self.ProcessListOfResources)
        print("Process list and its waiting list:", self.ProcessResourceWL)
        print("Ready list:", self.ReadyList) 
        print("Waitlist:", self.WaitList)

    def create(self, priority):
        if priority == 0 or self.ProcessList == None:
            return self.write(-1)

        # get the next free process
        for createdProcess in range(0, len(self.ProcessList)):
            if len(self.ProcessList[createdProcess]) == 0:
                self.ProcessList[createdProcess] = [(self.currentProcess, priority)] # initialize the created process with (parentProcess, priority)
                break

        self.ProcessList[self.currentProcess].append(createdProcess) # add the process to parent's list
        self.ReadyList[priority].append(createdProcess) # add current process to ready list

        print("Created process:", createdProcess, "Priority:", priority)
        print("Process list:", self.ProcessList) 
        print("Resource list:", self.ResourceList)
        print("Process list and its resources:", self.ProcessListOfResources)
        print("Process list and its waiting list:", self.ProcessResourceWL)
        print("Ready list:", self.ReadyList) 
        print("Waitlist:", self.WaitList)

        self.scheduler()

    def destroy(self, process, total = 0): 
        if len(self.ProcessList[process]) == 0:
            print("no process to destroy")
            return self.write(-1)            

        while len(self.ProcessList[process]) > 1: # loops thru all its children processes
            total += 1 
            self.destroy(self.ProcessList[process][1], total)

        index = self.ProcessList[process].pop() # pop the process --> (parentProcess, priority) 

        self.ProcessList[index[0]].remove(process) # then remove it from parent list
        
        try: # this removes it from ready list
            self.ReadyList[index[1]].remove(process) # remove process from ready list
        except: # if not in ready list, then remove it from waitlist
            self.WaitList[self.ProcessResourceWL[process].pop()[0]].remove(process)

        # add back resources
        for resource in range(0, len(self.ProcessListOfResources[process])): # if this process contains any resource, add it back to resource list
            if self.ProcessListOfResources[process][resource] > 0:
                self.ResourceList[resource] += self.ProcessListOfResources[process][resource]
        self.ProcessListOfResources[process] = [0, 0, 0, 0]              

        print("Destroyed process:", process)
        print("Process list:", self.ProcessList) 
        print("Resource list:", self.ResourceList)
        print("Process list and its resources:", self.ProcessListOfResources)
        print("Process list and its waiting list:", self.ProcessResourceWL)
        print("Ready list:", self.ReadyList) 
        print("Waitlist:", self.WaitList)

        return total + 1

    def request(self, resource, units): # remove from ready list if blocked
        if self.currentProcess == 0: #can 0 request resource?
            return self.write(-1)

        if resource > 3:
            return self.write(-1)

        if self.ResourceList[resource] >= units: # resource has enough units to fulfill request
            self.ResourceList[resource] -= units
            self.ProcessListOfResources[self.currentProcess][resource] += units

        else: # otherwise add it to waiting list and block the current process from ready list, so schedular wont choose it
            self.ProcessResourceWL[self.currentProcess].append([resource, units])
            self.WaitList[resource].append(self.currentProcess) # append current process to the waitlist
            self.ReadyList[self.ProcessList[self.currentProcess][0][1]].remove(self.currentProcess) # remove it from the ready list


        print("Process:", self.currentProcess, "requested Resource:", resource, "Units:", units)
        print("Process list:", self.ProcessList) 
        print("Resource list:", self.ResourceList)
        print("Process list and its resources:", self.ProcessListOfResources)
        print("Process list and its waiting list:", self.ProcessResourceWL)
        print("Ready list:", self.ReadyList) 
        print("Waitlist:", self.WaitList)


        self.scheduler()

    # get current process, release its resources
    def release(self, resource, units): # add back into ready list for the waiting processes, when released resource is available
        if self.currentProcess == 0 or resource > 3:
            return self.write(-1)
        
        currentUnits =  self.ProcessListOfResources[self.currentProcess][resource] # get the units of the resource
       
        # amount we're trying to release is greater than what we have
        if units > currentUnits:
            return self.write(-1)
        # otherwise, we have enough resources to release
        else:
            self.ResourceList[resource] += units
            self.ProcessListOfResources[self.currentProcess][resource] -= units

            # check waitling list for any resources requesting the released resource, if so add them
            if len(self.WaitList[resource]) > 0: # if there's a process waiting for that resource
                for requestList in range(0, len(self.ProcessResourceWL[self.WaitList[resource][0]])):
                    if self.ProcessResourceWL[self.WaitList[resource][0]][requestList][0] == resource: # our process has a list requesting the released resource
                        self.ProcessResourceWL[self.WaitList[resource][0]].pop(requestList) # pop it off the process's waitlist
                        self.ResourceList[resource] -= units
                        process = self.WaitList[resource].pop(0)
                        self.ProcessListOfResources[process][resource] += units # pop the process off the waiting list, add requested resource to that process
                        self.ReadyList[self.ProcessList[process][0][1]].append(process)

        print("Process", self.currentProcess, "released Resource:", resource, "Units:", units)
        print("Process list:", self.ProcessList) 
        print("Resource list:", self.ResourceList)
        print("Process list and its resources:", self.ProcessListOfResources)
        print("Process list and its waiting list:", self.ProcessResourceWL)
        print("Ready list:", self.ReadyList) 
        print("Waitlist:", self.WaitList)



        self.scheduler()

    def timeout(self):
        if self.currentProcess == 0: # can't timeout 0
            return self.scheduler()  

        priority = self.ProcessList[self.currentProcess][0][1]
        self.ReadyList[priority].remove(self.currentProcess)
        self.ReadyList[priority].append(self.currentProcess)

        print("timing out:", self.currentProcess)
        print("Process list:", self.ProcessList) 
        print("Resource list:", self.ResourceList)
        print("Process list and its resources:", self.ProcessListOfResources)
        print("Process list and its waiting list:", self.ProcessResourceWL)
        print("Ready list:", self.ReadyList) 
        print("Waitlist:", self.WaitList) 

        self.scheduler()

    def scheduler(self): #fix scheduler for blocked resources
        for priority in range(len(self.ReadyList)-1, 0, -1):
            for process in self.ReadyList[priority]:
                if len(self.ProcessResourceWL[process]) == 0: # if empty
                    self.currentProcess = process
                    self.write(self.currentProcess)
                    print("current process:", self.currentProcess)
                    return

        self.currentProcess = 0 # if none in ready list is empty, current process
        self.write(0)

        print("current process:", self.currentProcess)

    def shell(self):
        with open(sys.argv[1], "r") as file:
            lineNum = 1
            for line in file:
                line = line.split()
                print("Line:", lineNum, line)
                lineNum += 1
                if (len(line) > 0):
                    if line[0] == "in":
                        self.init()
                    elif line[0] == "cr":
                        self.create(int(line[1]))
                    elif line[0] == "de":
                        if self.destroy(int(line[1])) != None:
                            self.scheduler()
                        # self.destroy(int(line[1]))
                    elif line[0] == "rq":
                        self.request(int(line[1]), int(line[2]))
                    elif line[0] == "rl":
                        self.release(int(line[1]), int(line[2]))
                    elif line[0] == "to":
                        self.timeout()

                input()
                
run = Process() 
run.shell()
