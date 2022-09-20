"""
Rheena Zennia Blas
120347046
"""
import random

class Process():
        def __init__(self, PId, time, Io, queue):
            try:
                self._PId = PId
                self._time = time
                self._Io = Io
                self._queue = queue
                self._state = "READY"
                self._IoTime = None
                if self._Io:
                    self._IoTime = time*.4
            except IndexError():
                print("Invalid queue")

        def getPId(self):
            return self._PId

        def getIoTime(self):
            return self._IoTime

        def getIo(self):
            return self._Io

        def setIo(self, i):
            self._Io = i
            return self.Io

        def getQueue(self):
            return self._queue

        def setQueue(self, q):
            self._queue = q
            self._prevq = q

        def getTime(self):
            return self._time

        def setTime(self, t):
            self._time = t

        def getState(self):
            return self._state

        def setState(self, t):
            self._state = t

        PId = property(getPId)
        IoTime = property(getIoTime)
        Io = property(getIo, setIo)
        time = property(getTime, setTime)
        queue = property(getQueue, setQueue)
        state = property(getState, setState)

        def __str__(self):
            output = f"Process: {self._PId}\tTime: {self._time}\tQueue: {self._queue}\tI/O= {self._Io}"
            return output
        
class Queue():
    def __init__(self, priority, timeSlice):
        self._body = []
        self._priority = priority
        self._timeSlice = timeSlice
        self._length = len(self._body)

    def getLength(self):
        self._length = len(self._body)
        return self._length

    length = property(getLength)

    def __str__(self):
        output = ""
        if self._timeSlice == 0:
            output += "Blocked Queue\n"
        if self._length > 1:
            output += f"Queue {self._priority} has timeslice {self._timeSlice} secs:\n"
            for i in range(self._length):
                output += f"{self._body[i]}\n"
        elif self._length == 1:
            output += f"Queue {self._priority} has timeslice {self._timeSlice} secs:\n{self._body[0]}\n"
        else:
            output += f"Queue {self._priority} is empty which has a timeslice of {self._timeSlice} secs.\n"
        return output

class Kernel():
    def __init__(self, frequency, numQueue, time):
        if frequency < 0 | numQueue < 0 | time < 0:
            raise ValueError("Input cannot be a negative number")
        else:
            self._frequency = frequency 
            self._origFreq = frequency
            self._numQueue = numQueue
            self._processes = 0
            self._processIDs = 0
            self._state = "RUNNING"
            self._timeSlice = time
            self._time = 0
            self._pointer = None
            self._que = []
            self._block = Queue(self._numQueue+1, 0)
            #creates a the queues
            for i in range(self._numQueue):
                q = Queue(i, self.time(i))
                self._que.append(q)


    #returns the time slices for each queue
    def time(self, i):
        return (2**i)*self._timeSlice

    #creates a process and is added to the queue specified
    def createProcess(self, time, Io, queue):
        if queue >= self._numQueue:
            raise IndexError(f"Invalid queue. Please put a queue within the range 0-{self._numQueue-1}")
        else:
            process = Process(self._processIDs, time, Io, queue)
            self._que[queue]._body.append(process)
            self._que[queue]._length += 1
            self._processes += 1
            self._processIDs += 1
            self._updatePointer()
        self._updatePower()

    #dequeues the pointer/ the process that is currently is in highest priority 
    def deQueue(self):
        p = self._pointer
        queue = p.queue

        #updates the time of the process and the CPU
        if (queue == self._numQueue-1) & self._frequency != self._origFreq:
            p.time = p.time - (self.time(p.queue)*1.5)
            self._time += self.time(p.queue)
        else:
            p.time = p.time - self.time(p.queue)
            self._time += self.time(p.queue)
        
        #if no I/O or IoTime is not reached yet
        if p.time > 0:
            #checks and enters the block queue if I/O is on
            if p.Io:
                if p.time <= p.IoTime:
                    self._updateBlockQueue(p)
                    print("**************************************************************************************")
                    print(f"Process {p.PId} has entered the blocked queue. Waiting to I/O to complete. (.unblockProcess)")  
                    print("**************************************************************************************\n\n")
                    return
            if p.queue < self._numQueue-1:
                p.queue += 1
                self._updateQueue(queue, p)
        
            #if the process is at the last level
            elif queue == self._numQueue-1:
                self._que[queue]._body.pop(0)
                self._que[queue]._body.append(p) 
            self._updatePointer()
        else:
            self._removeFromQueue(queue)
            self._processes -= 1
            p.state = "TERMINATED"
            print("**********************************")
            print(f"      Process {p.PId} has finished")
            print("**********************************\n\n")
            if self._processes <= 0:
                self._pointer = None
                self._state = "IDLE"
                print("************************************************************")
                print("Idle process is running the CPU, insert a process to awaken.")
                print("************************************************************\n\n")
            else:
                self._updatePointer()
        self._updatePower() 

    #dequeues processes in the queues n times;
    #n is given by the user
    def deQueueMany(self, n):
        num = 0
        while num != n and self._processes > 0:
            self.deQueue()
            num += 1

    #automatically dequeues everything; 
    #if there are processes in block queue, a number is generated and if it is divisible by 2
    #the processes is unblocked
    def deQueueAll(self):
        num = 0
        while num != self._numQueue:
            while self._que[num].length != 0:
                if self._block.length > 0:
                    randomNum = random.randint(0,100) 
                    if randomNum%2 == 0:
                        self.unblockProcess()
                self.deQueue()
            num += 1
        if self._block.length > 0:
            randomNum = random.randint(0,100) 
            if randomNum%2 == 0:
                self.unblockProcess()
            else: 
                self._time += 300
            self.deQueueAll()

    #automatically adjusts the length of queue and removing the process with highet priority
    def _removeFromQueue(self, q):
        self._que[q]._body.pop(0)
        self._que[q].length
        
    #if the process still has time, is removed from the current queue and is added to the next queue
    def _updateQueue(self, q, p):
        self._removeFromQueue(q)
        self._que[q+1]._body.append(p)
        self._que[q+1].length

    #adds a process into the block queue
    #sets the pointer to the new processes that has the highest priority
    def _updateBlockQueue(self, p):
        self._block._body.append(p)
        p.state = "BLOCKED"
        self._removeFromQueue(p.queue)
        self._updatePointer()

    #
    def _removeBlockQueue(self, p, i):
        self._block._body.pop(i)
        p.state = "READY"
        p.Io = False
        if 0 < p.queue < self._numQueue//2 :
            p.queue -= 1
        else:
            p.queue -= 2
        self._que[p.queue]._body.append(p)
        self._que[p.queue].length
        self._updatePointer()
    
    #unblocks specific processes in block queue given their process ID
    def unblockSpecificProcess(self, p):
        q = self._block
        if q.length > 0:
            for num, processes in enumerate(q._body):
                if processes.PId == p:
                    print("**********************************")
                    print(f"       Process {p.PId} Unblocked")
                    print("**********************************\n")
                    self._removeBlockQueue(p, num)
        elif self._block.length <= 0:
            print("**********************************")
            print("No processes in block queue")
            print("**********************************\n")

    #unblocks the first process in the block queue
    def unblockProcess(self):
        q = self._block
        if q.length > 0:
            print("**********************************")
            print(f"       Process {q._body[0].PId} Unblocked")
            print("**********************************\n")
            self._removeBlockQueue(q._body[0], 0)
        elif self._block.length <= 0:
            print("**********************************")
            print("No processes in block queue")
            print("**********************************\n")

    #gets the process with the highest priority
    def _updatePointer(self):
        if self._processes > 0:
            #search the queues 
            for num in range(self._numQueue):
                q = self._que[num]
                if q._length > 0:
                    #go into the queue and get the processes 
                    self._pointer = q._body[0]
                    break
    
    #changes the frequency of the computer when there are less than and equal to 2 processes in the last queue
    #and the total number of process has less than the amount in the last queueS
    #or if the 
    def _updatePower(self):
        #getting out of idle state
        if (self._state != "RUNNING") & self._processes > 0:
            self._state = "RUNNING"
            print("*********************************")
            print("      CPU is now running")
            print("*********************************\n\n")

        if (self._processes <= self._que[-1].length <= 2) | ((self._processes <= 2) & self._block.length != 0) & self._frequency == self._origFreq:
            self._frequency = .1*self._frequency
            print("*********************************")
            print("CPU has entered power saving mode")
            print("*********************************\n\n")
        elif self._frequency != self._origFreq:
            print("**********************************")
            print("       CPU using full power")
            print("**********************************\n\n")
            self._frequency = self._origFreq 


    def getPointer(self):
        #look for the first occurence of process
        return self._pointer

    def getProcesses(self):
        #get the number of process
        return self._processes

    processes = property(getProcesses)
    pointer = property(getPointer)

    def __str__(self):
        output = ""
        if self._processes == 0:
            output += f"~~~CPU has {self._numQueue} queues and 0 processes.~~~\n" #CPU is idle
        else:
            output += f"~~~CPU has {self._processes} processes~~~\n"
            for i in range(len(self._que)):
                if self._que[i].length > 0:
                    output += str(self._que[i])
            #output += f"CPU has 1 process, {self._numQueue} queues.\n"
        if self._block.length != 0:
            output += "Block Queue:\n"
            for i in self._block._body:
                output += f"Process: {i.PId}\tTime: {i.time}\t I/O= {i.Io}\n" 
        output += "\n\n"
        return output


def testrun1():
    CPU = Kernel(1000000000, 8, 100)
    CPU.createProcess(2300, False, 0)
    CPU.createProcess(1000, True, 1)
    CPU.createProcess(2000, True, 2)
    CPU.createProcess(4000, False, 2)
    CPU.createProcess(1000, False, 3)
    CPU.createProcess(6000, True, 4)    
    CPU.createProcess(4800, False, 5)
    print(CPU)
    CPU.deQueue()
    CPU.deQueueMany(8)
    print(CPU)
    CPU.unblockProcess()
    print(CPU)

def testrun():
    CPU = Kernel(1000000000, 8, 100)
    CPU.createProcess(2300, False, 2)
    CPU.createProcess(40000, True, 0)
    CPU.createProcess(2000, True, 2)
    CPU.createProcess(48000, False, 3)
    CPU.createProcess(10000, False, 4)
    CPU.createProcess(6000, True, 1)    
    CPU.createProcess(48000, False, 4)
    print(CPU)
    CPU.deQueueAll()
    print(CPU)
    CPU.createProcess(6000, True, 1) 
    print(CPU)

testrun()


