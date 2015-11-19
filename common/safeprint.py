import multiprocessing, sys, datetime

print_lock = multiprocessing.Lock()
def safeprint(content):
  with print_lock:
    sys.stdout.write(("[" + str(multiprocessing.current_process().pid) + "] " + datetime.datetime.now().strftime('%H%M%S') + ": " + str(content) + '\r\n'))
