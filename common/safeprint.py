import multiprocessing, sys, datetime
from common import settings

print_lock = multiprocessing.RLock()


def safeprint(msg, verbosity=0):
    """Prints in a thread-lock, taking a single object as an argument"""
    string = ("[" + str(multiprocessing.current_process().pid) + "] " + 
              datetime.datetime.now().strftime('%H:%M:%S: ') + str(msg) + '\r\n')
    with print_lock:
        with open("output.txt", "a") as log:
            log.write(string)
        if settings.config.get('verbose') >= verbosity:
            sys.stdout.write(string)
