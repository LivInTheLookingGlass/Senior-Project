from common import bounty
from common.peers import *
from common import settings
from common.safeprint import safeprint
from multiprocessing import Queue
from time import sleep, time
import pickle

def testBounty(ip, btc, rwd, desc):
    safeprint(desc)
    test = bounty.Bounty(ip,btc,rwd)
    a = pickle.dumps(test,1)
    safeprint(bounty.addBounty(a))
 
def main():
    settings.setup()
    try:
        import miniupnpc
    except:
        safeprint("Dependency miniupnpc is not installed. Running in outbound only mode")
        settings.config['outbound'] = True
    safeprint("settings are:")
    safeprint(settings.config)
    q = Queue()
    ear = listener(settings.config['port'],settings.config['outbound'],q)
    ear.daemon = True
    ear.start()
    feedback = []
    stamp = time()
    while q.empty():
        if time() - 5 > stamp:
            break
    try:
        feedback = q.get(False)
    except:
        safeprint("No feedback received from listener")
    ext_ip = ""
    ext_port = -1
    if feedback != []:
        settings.outbound = feedback[0]
        if settings.outbound is not True:
            ext_ip = feedback[1]
            ext_port = feedback[2]
    initializePeerConnections(settings.config['port'], ext_ip, ext_port)
    #######TEST SECTION#######
    testBounty('8.8.8.8:8888',"1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9",1090,"Correctly formed bounty")
    testBounty('8.8.8.8',"1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9",1090,"Malformed bounty 1 (ip failure)")
    testBounty('8.8.8:8888',"1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9",1090,"Malformed bounty 2 (ip failure)")
    testBounty('8.8.8.8:88888888888888',"1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9",1090,"Malformed bounty 3 (ip failure)")
    testBounty('8.8.12348.8',"1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9",1090,"Malformed bounty 4 (ip failure)")
    testBounty('8.8.8.8:8888',"1JTGcHS3GMhBGGww4ZEDmP7u9",1090,"Malformed bounty 5 (btc failure)")
    testBounty('8.8.8.8:8888',"1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9",-1090,"Malformed bounty 6 (reward failure)")
    testBounty('8.8.8.8:8888',"1LhPsd4ng3AXmVPzrLWprWFx351pW4HJm8",1090,"Correctly formed bounty 2")
    testBounty('8.8.8.8:8888',"1MWSdYMKEpfWVxC6BGYARxsksaQuyEWzG5",1090,"Correctly formed bounty 3")
    testBounty('8.8.8.8:8888',"1EgGfDetymjMzcQ1AEhHjHEyXHjnEavwgg",1090,"Correctly formed bounty 4")
    safeprint(bounty.getBountyList())
    bounty.saveToFile(bounty.bountyList)
    bounty.loadFromFile()
#    bounty.bountyList = bounty.loadFromFile()
    safeprint(bounty.getBountyList())
    safeprint(bounty.getBounty(settings.config.get('charity'),settings.config.get('propagate_factor')))
    
if __name__ == "__main__":
    main()
