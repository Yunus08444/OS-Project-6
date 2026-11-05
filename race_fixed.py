"""ПР-6, пункт 1: исправленный счётчик с threading.Lock."""
import threading
counter = 0
lock = threading.Lock()
THREADS = 4
INCREMENTS = 100_000

def worker():
    global counter
    for _ in range(INCREMENTS):
        with lock:
            counter += 1

threads = [threading.Thread(target=worker) for _ in range(THREADS)]
for t in threads: t.start()
for t in threads: t.join()
assert counter == THREADS * INCREMENTS, f"counter={counter}"
print(f"С lock: {counter} — корректно")
