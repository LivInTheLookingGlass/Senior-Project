import multiprocessing, sys, datetime

print_lock = multiprocessing.RLock()
def safeprint(content):
  string = "[" + str(multiprocessing.current_process().pid) + "] " + datetime.datetime.now().strftime('%H%M%S') + ": " + str(content) + '\r\n'
  with print_lock:
    sys.stdout.write(string)
