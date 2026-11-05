"""ПР-6, пункт 4: иллюстрация потерянного уведомления."""
import threading
condition=threading.Condition()
# No thread is waiting at this moment: notification is not stored.
with condition:
    condition.notify()
print("notify() выполнен до wait(): уведомление потеряно.")
print("Если поток затем ждёт, он может зависнуть. Условие проверяют в while под mutex.")
