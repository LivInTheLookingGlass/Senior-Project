import multiprocessing, sys
from time import sleep

print_lock = multiprocessing.Lock()
def safeprint(content):
  with print_lock:
    sys.stdout.write("[" + str(multiprocessing.current_process().pid) + "] " +  str(content) + '\r\n')
    sleep(0.1)
