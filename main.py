from common import bounty
from common.peers import *
from common import settings
from common.safeprint import safeprint
from multiprocessing import Queue, Value
from time import sleep, time
import pickle

def sync():
    from multiprocessing import Manager
    from common import bounty, settings, peers
    man = Manager()
    items = {'config':man.dict(),
             'peerList':man.list(),
             'bountyList':man.list(),
             'bountyLock':bounty.bountyLock,
             'keyList':man.list()}
    items['config'].update(settings.config)
    items['peerList'].extend(peers.peerlist)
    items['bountyList'].extend(bounty.bountyList)
    items['keyList'].extend(bounty.keyList)
    if items.get('config'):
        from common import settings
        settings.config = items.get('config')
    if items.get('peerList'):
        global peerList
        peers.peerlist = items.get('peerList')
    if items.get('bountyList'):
        from common import bounty
        bounty.bountyList = items.get('bountyList')
    if items.get('bountyLock'):
        from common import bounty
        bounty.bountyLock = items.get('bountyLock')
    if items.get('keyList'):
        from common import bounty
        boutny.keyList = items.get('keyList')
    return items

def testBounty(ip, btc, rwd, desc, data=None):
    safeprint(desc)
    test = bounty.Bounty(ip,btc,rwd,dataDict=data)
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
    ear.sync(sync())
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
    live.value = False

if __name__ == "__main__":
    main()
