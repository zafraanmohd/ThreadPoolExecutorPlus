from __future__ import print_function

from functools import wraps
from threading import Thread, current_thread
from concurrent.futures import wait
from ThreadPoolExecutorPlus.thread import ThreadPoolExecutor
import time

def timer():
    def _timer(func):
        @wraps(func)
        def __timer(*args, **kwargs):
            start = time.time()
            thread_name = current_thread().getName()
            result = func(*args, **kwargs)
            print("time taken:", time.time()-start, func.__name__, thread_name)
            return result
        return __timer
    return _timer

def simple_trace():
    def _simple_trace(func):
        @wraps(func)
        def __simple_trace(*args, **kwargs):
            thread_name = current_thread().getName()
            print("ENTER :", func.__name__, thread_name)
            result = func(*args, **kwargs)
            print("EXIT  :", func.__name__, thread_name)
            return result
        return __simple_trace
    return _simple_trace

@simple_trace()
def sleeper(work_counter, i):
    time.sleep(1)
    work_counter[i] = True

def sleeper_callback(*args):
    print('callback.', args, current_thread().getName())

@simple_trace()
def sleeper2(*args):
    time.sleep(1)


pool = ThreadPoolExecutor(100)
pool.set_daemon_opts(min_workers=10, keep_alive_time=5)

@timer()
def main():
    fs = []
    for i in range(10):
        fs.append(pool.submit(sleeper2, [1]*10))
    
    wait(fs)
    print('Here')

main()