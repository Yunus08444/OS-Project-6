"""ПР-6, пункт 1B(b): bounded ring queue via mutex + Condition."""
import threading
from collections import deque
CAPACITY, PER_PRODUCER, PRODUCERS, CONSUMERS = 5, 1000, 3, 2
buffer=deque()
cv=threading.Condition()
finished=0
consumed=[]
errors=[]

def producer(pid):
    global finished
    for n in range(PER_PRODUCER):
        with cv:
            while len(buffer)>=CAPACITY:
                cv.wait()
            buffer.append((pid,n))
            if len(buffer)>CAPACITY: errors.append("overflow")
            cv.notify_all()
    with cv:
        finished+=1
        cv.notify_all()

def consumer():
    while True:
        with cv:
            while not buffer and finished<PRODUCERS:
                cv.wait()
            if not buffer and finished==PRODUCERS:
                return
            item=buffer.popleft()
            cv.notify_all()
        consumed.append(item)

threads=[threading.Thread(target=consumer) for _ in range(CONSUMERS)]
threads += [threading.Thread(target=producer,args=(p,)) for p in range(PRODUCERS)]
for t in threads: t.start()
for t in threads: t.join()
expected={(p,n) for p in range(PRODUCERS) for n in range(PER_PRODUCER)}
assert len(consumed)==3000 and set(consumed)==expected and not buffer and not errors
print("Condition ring OK: 3000 unique values; no overflow; buffer empty.")
