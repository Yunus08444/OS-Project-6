"""ПР-6, пункт 3: барьер на 4 потока, три фазы."""
import threading, time
barrier=threading.Barrier(4)
lock=threading.Lock()
passed=[]

def task(tid):
    for phase in range(1,4):
        time.sleep(0.002*(tid+1))
        with lock: print(f"Thread {tid}: phase {phase} before barrier")
        barrier.wait()
        with lock:
            passed.append((tid,phase))
            print(f"Thread {tid}: phase {phase} passed")

threads=[threading.Thread(target=task,args=(i,)) for i in range(4)]
for t in threads:t.start()
for t in threads:t.join()
assert len(passed)==12
print("Barrier passed: all 4 threads across 3 phases.")
