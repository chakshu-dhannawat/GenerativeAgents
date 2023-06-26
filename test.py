from queue import Queue
from threading import Thread
import time

a = 1
  
# A thread that produces data
def producer():
    now = time.time()
    global a
    time.sleep(0.5)
    a+=1
    time.sleep(2)
    print(a)
    print(time.time()-now)
          
# A thread that consumes data
def consumer():
    global a
    print(a)
    time.sleep(1)
    print(a)
    a+=1


# Create the shared queue and launch both threads
q = Queue()
t1 = Thread(target = consumer)
t2 = Thread(target = producer)
t1.start()
t2.start()
