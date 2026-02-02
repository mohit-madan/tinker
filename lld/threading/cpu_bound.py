import threading
import time

def count_up(n):
    while n > 0:
        n-=1
        # Key detail 🔑
        # time.sleep() releases the GIL
        # That means:
        # - While one thread is sleeping
        # - Another thread can run
        # time.sleep(0.0000001)

# Version A: Single-threaded
start_time = time.time()
count_up(2*10**7)
end_time = time.time()
# print(f"Single-threaded time: {end_time - start_time} seconds")
count_up(2*10**7)
end_time = time.time()
print(f"Single-threaded time: {end_time - start_time} seconds")

start_time = time.time()    
# Version B: Multi-threaded
t1 = threading.Thread(target=count_up, args=(2*10**7,))
t2 = threading.Thread(target=count_up, args=(2*10**7,))

t1.start()
t2.start()
t1.join()
t2.join()
end_time = time.time()
print(f"Multi-threaded time: {end_time - start_time} seconds")