"""ПР-6, пункт 1: намеренно некорректный общий счётчик без блокировки."""
import threading
counter = 0
THREADS = 4
INCREMENTS = 100_000

def worker():
    global counter
    for _ in range(INCREMENTS):
        counter += 1

threads = [threading.Thread(target=worker) for _ in range(THREADS)]
for t in threads: t.start()
for t in threads: t.join()
print(f"Без lock: {counter} (ожидается {THREADS * INCREMENTS})")
print("В CPython результат может совпасть из-за GIL; логическая гонка всё равно есть.")
