from common import bounty
from common.peers import *
from common import settings
from common.safeprint import safeprint
from multiprocessing import Queue, Value
from time import sleep, time
import pickle

def testBounty(ip, btc, rwd, desc):
    safeprint(desc)
    test = bounty.Bounty(ip,btc,rwd)
    dumped = pickle.dumps(test,1)
    safeprint(bounty.addBounty(dumped))

def main():
    settings.setup()
    try:
        import miniupnpc
    except:
        safeprint("Dependency miniupnpc is not installed. Running in outbound only mode")
        settings.config['outbound'] = True
    safeprint("settings are:")
    safeprint(settings.config)
    queue = Queue()
    live = Value('b',True)
    ear = listener(settings.config['port'],settings.config['outbound'],queue,live,settings.config['server'])
    ear.daemon = True
    ear.start()
    feedback = []
    stamp = time()
    while queue.empty():
        if time() - 5 > stamp:
            break #pragma: no cover
    try:
        feedback = queue.get(False)
    except: #pragma: no cover
        safeprint("No feedback received from listener")
    ext_ip = ""     #Does this affect peers?
    ext_port = -1   #Does this affect peers?
    if feedback != []:
        settings.outbound = feedback[0]
        if settings.outbound is not True:
            ext_ip = feedback[1]
            ext_port = feedback[2]
    initializePeerConnections(settings.config['port'], ext_ip, ext_port)
    requestBounties(get_lan_ip() + ":44565")    #Test function
    requestBounties("localhost:44565")          #test function
    v.value = False
    
if __name__ == "__main__":
    main()
