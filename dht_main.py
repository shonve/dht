#coding:utf-8

import dht_cs
import time
from define import THREAD_NUMBER, WORKING_TIME, BOOTSTRAP_NODES

if __name__ == '__main__':
    thread_num = THREAD_NUMBER
    working_time = WORKING_TIME
    threads = []
    for i in xrange(thread_num):
        i += 8000
        thread = dht_cs.DHT(host='0, 0, 0, 0', port=i)
        thread.start()
        i -= 8000
        thread.bootstrap(BOOTSTRAP_NODES[i][0], BOOTSTRAP_NODES[i][1])
        threads.append(thread)

    time.sleep(WORKING_TIME)
    for i in threads:
        print 'stop thread'
        i.stop()
        i.join()
        print 'finish thread'
