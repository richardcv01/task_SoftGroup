import time
import random
from threading import Thread, Lock, RLock
import threading

LOCK = threading.RLock()


def worker(file: object,  *args):
    """
    worker function writes two strings with random pause to
    shared file using synchronization primitive
    :param file: file-object
    :return:
    """
    LOCK.acquire()
    file.write( args[0] +  ': ' + 'started.\n')
    time.sleep(random.random() * 5)
    file.write( args[0] +': ' + 'done.\n')
    LOCK.release()


if __name__ == '__main__':
    file = open('test.txt', 'a', encoding='utf-8')
    for i in range(1, 11):
        name = 'thread_{}'.format(i)
        t = threading.Thread(target=worker, name=name, args=(file,name))
        t.start()



