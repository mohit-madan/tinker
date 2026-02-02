from multiprocessing import Process, Queue

data = []
# multi processes do not share memory space

def add_data(q):
    for i in range(10**4):
        q.put(i)
    # print("Inside process: ", "data")

def count_data(q):
    count = 0
    while not q.empty():
        count += q.get()
    return count

if __name__ == "__main__":
    q = Queue()
    p = Process(target=add_data, args=(q,))
    p.start()
    p.join()
    print("Count: ", count_data(q))