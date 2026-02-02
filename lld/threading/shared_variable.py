import threading
import time
counter = 0
lock = threading.Lock()
def count_up():
    global counter
    for _ in range(10**4):
        with lock:
            temp = counter
            time.sleep(0.0000001)
            counter = temp+1

t1 = threading.Thread(target=count_up)
t2 = threading.Thread(target=count_up)
t1.start()
t2.start()
t1.join()
t2.join()
print(counter)