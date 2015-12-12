from common import bounty #pragma: no cover
from common.peers import * #pragma: no cover
from common import settings #pragma: no cover
from common.safeprint import safeprint #pragma: no cover
from multiprocessing import Queue, Process, Value #pragma: no cover
from time import sleep, time #pragma: no cover
import pickle, sys #pragma: no cover
from main import * #pragma: no cover

def waitForty(v,q): #pragma: no cover
    stamp = time()
    while q.empty():
        if time() - 10 > stamp:
            break #pragma: no cover
    try:
        feedback = q.get(False)
    except: #pragma: no cover
        safeprint("No feedback received from listener")
    safeprint("YOUR IP IS " + get_lan_ip() + ":44566")
    requestPeerlist(get_lan_ip() + ":44566")
    sleep(4)
    requestPeerlist("localhost:44566")
    sleep(4)
    if sys.version_info[0] == 3:
        requestBounties(get_lan_ip() + ":44566")
        sleep(4)
        requestBounties("localhost:44566")
        sleep(4)
        safeprint(bounty.bountyList)
    #TODO move test incoming_bounty here
    #TODO move test incoming_bounty here
    safeprint("Sending term signal")
    v.value = False
    requestPeerlist("localhost:44566")

if __name__ == "__main__": #pragma: no cover
    testBounty('8.8.8.8:8888',"1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9",1440,"Correctly formed bounty")
    testBounty('8.8.8.8',"1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9",1440,"Malformed bounty 1 (ip failure)")
    testBounty('8.8.8:8888',"1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9",1440,"Malformed bounty 2 (ip failure)")
    testBounty('8.8.8.8:88888888888888',"1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9",1440,"Malformed bounty 3 (ip failure)")
    testBounty('8.8.12348.8',"1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9",1440,"Malformed bounty 4 (ip failure)")
    testBounty('8.8.8.8:8888',"1JTGcHS3GMhBGGww4ZEDmP7u9",1440,"Malformed bounty 5 (btc failure)")
    testBounty('8.8.8.8:8888',"1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9",-1440,"Malformed bounty 6 (reward failure)")
    testBounty('8.8.8.8:8888',"1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9",0,"Malformed bounty 7 (signature failure)")
    testBounty('8.8.8.8:8888',"1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9",1440,"Malformed bounty 8 (requirement failure)", data={'reqs':{("__builtins__","pow",2,2):4}})
    testBounty('8.8.8.8:8888',"1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9",1440,"Correctly formed bounty 2", data={'reqs':{("sys","platform","index=2","end=3"):"win33"}})
    testBounty('8.8.8.8:8888',"1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9",1440,"Malformed bounty 10 (requirements failure)", data={'reqs':{("__builtins__","pow",2,2):4,("sys","platform"):"win33"}})
    testBounty('8.8.8.8:8888',"1LhPsd4ng3AXmVPzrLWprWFx351pW4HJm8",10900,"Correctly formed bounty 3")
    testBounty('8.8.8.8:8888',"1MWSdYMKEpfWVxC6BGYARxsksaQuyEWzG5",1480,"Correctly formed bounty 4")
    testBounty('8.8.8.8:8888',"1EgGfDetymjMzcQ1AEhHjHEyXHjnEavwgg",10290,"Correctly formed bounty 5")
    safeprint(bounty.getBountyList())
    bounty.saveToFile(bounty.getBountyList())
    bounty.loadFromFile()
    safeprint(bounty.getBountyList())
    safeprint("3 bounties should follow")
    safeprint(bounty.getBounty(settings.config.get('charity'),settings.config.get('propagate_factor')))
    safeprint(bounty.getBounty(False,2))
    safeprint(bounty.getBounty(True,2))
    settings.saveSettings()
    settings.loadSettings()
    saveToFile()
    getFromFile()
    if not (sys.version_info[0] < 3 and sys.platform == "win32"):
        safeprint("Test listener begin")
        v = Value('b',True)
        q = Queue()
        a = Process(target=waitForty,args=(v,q))
        a.start()
        listen(44566,False,q,v,False)
