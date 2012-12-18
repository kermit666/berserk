import math
from time import time
from datetime import datetime, timedelta
import logging
import benchmark_notifier

def log(something):
    print(something)
    logging.info(something)


# MEMORY
#---------------------
# import sys

# class Structure(object):
#     data = "abcd"
#     def __init__(self, l):
#         self.reserved = l*self.data

# def memory(size = 1):
#     """
#     @param size: MBs to allocate
#     """
#     # allocate
#     data = range(10000)
#     size = sys.getsizeof(data)
#     log("allocated %d bytes" % (size))
#     # read / write
#---------------------

def memory(size_mb,run_period):
    import memory
    memory.run(size_mb, run_period)

def cpu(run_num, n):
    import fibonacci as fib
    log("Doing %d runs of %dth Fibonacci number calculation" % (run_num, n))
    for i in range(run_num):
        fib.fibonacci(n)
    
def finalize(results):
    log("------------------\n")
    benchmark_notifier.notify_master(host=conf.host, data=results)

def run_from_conf(conf): #TODO: run until datetime.now()==designated_time
    logging.basicConfig(filename='berserk.log',
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s')
    log("------------------\nBERSERK BENCHMARK\n------------------")
    dt1 = datetime.now()
    log("#start %s" % (str(dt1)))
    
    if conf.method=="memory":
        size_mb = conf.size
        run_period = conf.run_period
        memory(size_mb, run_period)
    elif conf.method=="cpu":
        run_num = conf.iterations
        n = conf.iteration_size
        cpu(run_num, n)
        
    dt2 = datetime.now()
    log("#end %s" % (str(dt2)))
    dt_runtime = dt2-dt1
    log("#runtime %s (%d s)" % (str(dt_runtime), dt_runtime.seconds))
    #results = {"dt_runtime": dt_runtime, "runtime": duration}
    results = (dt1, dt2)
    try:
        finalize(results)
    except:
        log("Warning: Can't notify the benchmark master of the outcome.")
    
def sample_run():
    while True:
        #memory()
        cpu()

if __name__ == "__main__":
    #sample_run()
    import conf
    run_from_conf(conf)
