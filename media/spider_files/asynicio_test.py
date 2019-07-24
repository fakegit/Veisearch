import threading
import time
import random
from threading import Condition
import queue
cond = Condition()
q = queue.Queue()
def producter(i,q):

    while True:
        num = random.randrange(100)
        q.put(num)
        print("生产者-{0}-生产了--{1}--".format(i,num))
        time.sleep(1)


def customer(i,q):
    while True:
        num = q.get()
        print("消费者-{0}-消费了--{1}--".format(i,num))
        time.sleep(1)


if __name__ == "__main__":

    for i in range(4):
        threading.Thread(target=producter,args=(i,q),name=str(i)).start()

    for i in range(3):
        threading.Thread(target=customer,args=(i,q),name=str(i)).start()


