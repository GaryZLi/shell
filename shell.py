import sys
import os

# PCB = [[0, 1], [(0, 2), 2, 3], [(1, 1)], [(1, 1)]]
# RCB = [1, 1, 2, 3]
# PRL = [[0, 0, 0, 0], [0, 0, 0, 0], ]
class Process:
    def __init__(self):
        # self.head = None # list of parent processes
        self.PCB = None # process
        self.RCB = None # resource 
        self.PRL = None # process resource list
        self.RWL = None # resource waitlist
        self.RL = None # ready list
        self.WL = None # waiting list
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
        self.PCB = [[]]*16
        self.RCB = [1,1,2,3]
        self.PRL = [[0 for _ in range(4)] for _ in range(16)] 
        self.RWL = [[] for _ in range(16)]
        self.RL = [0, [], []]
        self.WL = [0, [], [], []]

        self.currentProcess = 0
        self.PCB[0] = [0]

        print("process 0 created")
        self.write('init')

    def create(self, priority):
        if priority == 0 or self.PCB == None:
            return self.write(-1)

        # get the next free process
        for createdProcess in range(0, len(self.PCB)):
            if len(self.PCB[createdProcess]) == 0:
                self.PCB[createdProcess] = [(self.currentProcess, priority)] # initialize the created process with (parentProcess, priority)
                break

        self.PCB[self.currentProcess].append(createdProcess) # add the process to parent's list
        self.RL[priority].append(createdProcess) # add current process to ready list
        # print("process %d created" % createdProcess)

        self.scheduler()

    def destroy(self, process, total = 0): 
        if len(self.PCB[process]) == 0:
            return self.write(-1)            

        while len(self.PCB[process]) > 1: # loops thru all its children processes
            total += 1 
            self.destroy(self.PCB[process][1], total)

        index = self.PCB[process].pop() # pop the process --> (parentProcess, priority) 
        self.PCB[index[0]].remove(process) # then remove it from parent list
        self.RL[index[1]].remove(process) # remove process from ready list

        #idk if this is right -->  destroy from waiting list, add back resource, 
        for resource in range(0, len(self.PRL[self.currentProcess])): # if this process contains any resource, add it back to resource list
            if self.PRL[self.currentProcess][resource] > 0:
                self.RCB[resource] += self.PRL[self.currentProcess][resource]
        self.PRL[self.currentProcess] = [0, 0, 0, 0]              
                    
        return total + 1

    def request(self, resource, units): # remove from ready list if blocked
        if self.currentProcess == 0: #can 0 request resource?
            return self.write(-1)

        if resource > 3:
            return self.write(-1)

        if self.RCB[resource] >= units: # resource has enough units to fulfill request
            self.RCB[resource] -= units
            self.PRL[self.currentProcess][resource] += units

        else: # otherwise add it to waiting list and block the current process from ready list, so schedular wont choose it
            self.RWL[self.currentProcess].append([resource, units])
            self.WL[resource].append(self.currentProcess) # append current process to the waitlist

        self.scheduler()

    # get current process, release its resources
    def release(self, resource, units): # add back into ready list for the waiting processes, when released resource is available
        if self.currentProcess == 0:
            return self.write(-1)
        
        currentUnits =  self.PRL[self.currentProcess][resource] # get the units of the resource
       
        # amount we're trying to release is greater than what we have
        if units > currentUnits:
            return self.write(-1)
        # otherwise, we have enough resources to release
        else:
            self.RCB[resource] += units
            self.PRL[self.currentProcess][resource] -= units

            # check waitling list for any resources requesting the released resource, if so add them
            if len(self.WL[resource]) > 0: # if there's a process waiting for that resource
                for requestList in range(0, len(self.RWL[self.WL[resource][0]])):
                    if self.RWL[self.WL[resource][0]][requestList][0] == resource: # our process has a list requesting the released resource
                        self.RWL[self.WL[resource][0]].pop(requestList) # pop it off the process's waitlist
                        self.RCB[resource] -= units
                        self.PRL[self.WL[resource].pop(0)][resource] += units # pop the process off the waiting list, add requested resource to that process

        self.scheduler()

    def timeout(self):
        priority = self.PCB[self.currentProcess][0][1]
        self.RL[priority].append(self.RL[priority].pop(0))

        self.scheduler()

    def scheduler(self): #fix scheduler for blocked resources
        for priority in range(len(self.RL)-1, 0, -1):
            for process in self.RL[priority]:
                if len(self.RWL[process]) == 0: # if empty
                    self.currentProcess = process
                    self.write(self.currentProcess)
                    return

        self.currentProcess = 0 # if none in ready list is empty, current process
        self.write(0)

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
                        self.scheduler()
                    elif line[0] == "rq":
                        self.request(int(line[1]), int(line[2]))
                    elif line[0] == "rl":
                        self.release(int(line[1]), int(line[2]))
                    elif line[0] == "to":
                        self.timeout()

run = Process() 
run.shell()

# a = [[], [10], [11, 2]]


# for x in a:
#     for y in x:
#         print(y)



































# # class Process:
#     def __init__(self):
#         # self.head = None # list of parent processes
#         self.PCB = None # process
#         self.RCB = None # resource 
#         self.PRL = None # process resource list
#         self.RWL = None # resource waitlist
#         self.RL = None # ready list
#         self.currentProcess = None

#     def write(self, i):
#         with open("testoutput.txt", "a+") as file:
#             if i == 0:
#                 if os.stat("testoutput.txt").st_size > 0:
#                     file.write("\n" + str(i) + " ")
#                 else:
#                     file.write("0 ")
#             else:
#                 file.write(str(i) + ' ')
                
#     def init(self):
#         self.PCB = [[]]*16
#         self.RCB = [1,1,2,3]
#         self.PRL = [[0, 0, 0, 0]] * 16
#         self.RWL = [0] * 16
#         self.RL = [0, [], []]
#         self.currentProcess = 0
#         self.PCB[0] = [0]

#         print("process 0 created")
#         self.write(0)

#     def create(self, priority):
#         if priority == 0 or self.PCB == None:
#             return self.write(-1)

#         # get the next free process
#         for createdProcess in range(0, len(self.PCB)):
#             if len(self.PCB[createdProcess]) == 0:
#                 self.PCB[createdProcess] = [(self.currentProcess, priority)] # initialize the created process with (parentProcess, priority)
#                 break

#         self.PCB[self.currentProcess].append(createdProcess) # add the process to parent's list
#         self.RL[priority].append(createdProcess) # add current process to ready list
#         print("process %d created" % createdProcess)

#         self.scheduler()

#         # self.write(self.currentProcess)

#     def destroy(self, process, total = 0): 
#         while len(self.PCB[process]) > 1: # loops thru all its children processes
#             total += 1 
#             self.destroy(self.PCB[process][1], total)

#         index = self.PCB[process].pop() # pop the process --> (parentProcess, priority) 
#         self.PCB[index[0]].remove(process) # then remove it from parent list
#         self.RL[index[1]].remove(process) # remove process from ready list
#         # remove it from waiting list?
#         return total + 1

#     def request(self, resource, units): # has sched, remove from ready list if blocked
#         if self.RCB[resource] <= units: # resource has enough units to fulfill request
#             self.RCB[resource] -= units
#             self.PRL[self.currentProcess][resource] += units
#         else: # otherwise add it to waiting list and block the current process from ready list, so schedular wont choose it
#             self.RWL[self.currentProcess] = [resource, units]

#             # self.RL[self.PCB[self.currentProcess][0][1]].remove(self.currentProcess)

#         self.scheduler()


#     # get current process, release its resources
#     def release(self, resource, units): # add back into ready list for the waiting processes
#         currentUnits =  self.PRL[self.currentProcess][resource] # get the units of the resource

#         # # amount we're trying to release is greater than what we have
#         if units > currentUnits:
#             self.write(-1)
#         # otherwise, we have enough resources to release
#         else:
#             self.RCB[resource] += units
#             self.PRL[self.currentProcess][resource] -= units
#             self.write(self.currentProcess)

#     def timeout(self):
#         priority = self.PCB[self.currentProcess][0][1]
#         self.RL[priority].append(self.RL[priority].pop(0))

#         self.scheduler()

#     def scheduler(self): #fix scheduler for blocked resources
#         if len(self.RL[2]) > 0:
#             self.currentProcess = self.RL[2][0]
#         elif len(self.RL[1]) > 0:
#             self.currentProcess = self.RL[1][0]
#         else:
#             self.currentProcess = 0

#         self.write(self.currentProcess)
#         print('process', self.currentProcess, 'is running')

#     def shell(self):
#         with open(sys.argv[1], "r") as file:
#             for line in file:
#                 line = line.split()

#                 if (len(line) > 0):
#                     if line[0] == "in":
#                         self.init()
#                     elif line[0] == "cr":
#                         self.create(int(line[1]))
#                     elif line[0] == "de":
#                         print(self.destroy(int(line[1])), "process destroyed")
#                         self.scheduler()
#                     elif line[0] == "rq":
#                         self.request(int(line[1]), int(line[2]))
#                     elif line[0] == "rl":
#                         self.release(int(line[1]), int(line[2]))
#                     elif line[0] == "to":
#                         self.timeout()

#         print(self.PCB)

# run = Process() 
# run.shell()

# # a = [[], [10], [11, 2]]


# # for x in a:
# #     for y in x:
# #         print(y)
