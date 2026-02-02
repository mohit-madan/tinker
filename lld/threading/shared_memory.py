from multiprocessing import Process, Queue

data = []
# multi processes do not share memory space

def add_data(q):
    q.put("data")
    # print("Inside process: ", "data")

if __name__ == "__main__":
    # in this case data will not be shared
    q = Queue()
    p = Process(target=add_data, args=(q,))
    p.start()
    p.join()
    # add_data() # In this case data will be shared
    while not q.empty():
        print("Outside process: ", q.get())