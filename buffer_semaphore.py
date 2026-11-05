"""ПР-6, пункт 1B(a): bounded ring buffer через 2 семафора + mutex."""
import threading
CAPACITY, PER_PRODUCER, PRODUCERS, CONSUMERS = 5, 1000, 3, 2
buf=[None]*CAPACITY
put_idx=get_idx=0
mutex=threading.Lock()
empty=threading.Semaphore(CAPACITY)
full=threading.Semaphore(0)
consumed=[]
errors=[]

def producer(pid):
    global put_idx
    for n in range(PER_PRODUCER):
        item=(pid,n)
        empty.acquire()
        with mutex:
            if buf[put_idx] is not None: errors.append("overflow")
            buf[put_idx]=item
            put_idx=(put_idx+1)%CAPACITY
        full.release()

def consumer():
    global get_idx
    while True:
        full.acquire()
        with mutex:
            item=buf[get_idx]
            if item is None: errors.append("read from empty slot")
            buf[get_idx]=None
            get_idx=(get_idx+1)%CAPACITY
        empty.release()
        if item=="STOP": return
        consumed.append(item)

cs=[threading.Thread(target=consumer) for _ in range(CONSUMERS)]
ps=[threading.Thread(target=producer,args=(i,)) for i in range(PRODUCERS)]
for t in cs+ps: t.start()
for t in ps: t.join()
for _ in range(CONSUMERS):
    empty.acquire()
    with mutex:
        buf[put_idx]="STOP"
        put_idx=(put_idx+1)%CAPACITY
    full.release()
for t in cs: t.join()
expected={(p,n) for p in range(PRODUCERS) for n in range(PER_PRODUCER)}
assert len(consumed)==3000 and set(consumed)==expected and not any(buf) and not errors
print("Semaphore ring OK: 3000 unique values; no overflow; buffer empty.")
