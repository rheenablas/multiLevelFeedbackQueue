# multiLevelFeedbackQueue

A multilevel feedback queue implemented through python. 

An outline how the multilevel feedback queue works, the power saving and idle process algorithm used, 

-	Multilevel Feedback Queues Scheduling:
  
  o	 Get the current/highest priority process
  o	Subtract the queue time from the process’ time
  o	If the process still have remaining time
    	Check for I/O
      •	If the time is less than the given I/O time (40% of the given time)
        o	Process enters block queue
      •	If not
        o	Process dequeues
    	Put the process to the next queue
    	If the queue is the last possible queue
      •	It stays in the queue but have the least priority if not empty
  o	Else (if process’ time is less than or equal to zero)
    	Process exits the CPU
    	If the last process terminates
      •	The idle process take over 

-	Power Saving Algorithm:
  o	If the number of total processes is less than the number of processes in the lowest queue and if the number of processes in the lowest queue is less than or equal to 2
    	Then the new frequency is a tenth given frequency 
  o	Frequency reverts back if the number of processes exceeds the threshold

-	Rule of I/O: 
  o	when the user completes the I/O or invoked by the user (.unblockProess() made method), the process will return to the queue
  o	the process’ queue will increase it’s priority by one if it is between 0 and half of the queue; it will increase by two if it is between the lower half of the queue (lower queues)

-	Idle process algorithm:
  o	If there are no more processes in the CPU, the idle process takes over
  o	If processes are inserted again, the idle process waits at the end of the queue, giving the other processes higher priority
