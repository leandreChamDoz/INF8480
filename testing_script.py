import sys
import urllib2
import time
from threading import Thread, Lock

mean_time = 0
mutex = Lock()
num_corr = 0
url = "http://132.207.12.209:8000"

def query_balancer():
    deb = int(round(time.time() * 1000))

    try:
        con = urllib2.urlopen(url)
        con.read()
        con.close()
    except:
        sys.exit(1)

    fin = int(round(time.time() * 1000))

    mutex.acquire()

    global mean_time, num_corr
    mean_time += fin - deb
    num_corr += 1

    mutex.release()

def launch_queries():
    threads = []
    for i in range(0, 30):
        threads.append(Thread(target=query_balancer))
        threads[-1].start()
    
    for i in threads:
        i.join()
    print(str(num_corr) + ' received answers')
    print('mean time : ' + str(mean_time / num_corr) + ' ms')
    sys.exit(0)

launch_queries()