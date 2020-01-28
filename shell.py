import sys
import os

# PCB[16]
# ready list - 3lv
# rcb[4] 
# 0, 1 = 1
# 2 = 2
# 3 = 3

def write(i):
    with open("test", "a+") as file:
        if i == 0:
            if os.stat("test").st_size > 0:
                file.write("\n" + str(i) + " ")
            else:
                file.write("0 ")
        else:
            file.write(str(i))
            
    
        

def init():
    print("process 0 created")
    write(0)

def create(priority):
    with open("test", "a+") as file:
        file.write(str(priority) + " ")

def destroy(process):
    pass

def request(resource, units): #has sched
    pass

def release(resource, units):
    pass

def timeout():
    pass

def scheduler():
    pass

def shell():
    with open(sys.argv[1], "r") as file:
        for line in file:
            line = line.split()

            if (len(line) > 0):
                if line[0] == "in":
                    init()
                elif line[0] == "cr":
                    create(4)
                # elif line[0] == "de":
                #     destroy()
                # elif line[0] == "rq":
                #     request()
                # elif line[0] == "rl":
                #     release()
                # elif line[0] == "to":
                #     timeout()

shell()