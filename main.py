from common import bounty, peers, settings
from common.safeprint import safeprint
from multiprocessing import Queue, Value
from time import sleep, time
import pickle


def sync():
    from multiprocessing import Manager
    man = Manager()
    items = {'config': man.dict(),
             'peerList': man.list(),
             'bountyList': man.list(),
             'bountyLock': bounty.bountyLock,
             'keyList': man.list()}
    items['config'].update(settings.config)
    items['peerList'].extend(peers.peerlist)
    items['bountyList'].extend(bounty.bountyList)
    safeprint(items)
    peers.sync(items)
    return items


def initParallels():
    queue = Queue()
    live = Value('b', True)
    ear = peers.listener(settings.config['port'], settings.config['outbound'], queue, live, settings.config['server'])
    ear.daemon = True
    ear.items = sync()
    ear.start()
    mouth = peers.propagator(settings.config['port'] + 1, live)
    mouth.daemon = True
    mouth.items = ear.items
    mouth.start()
    feedback = []
    stamp = time()
    while queue.empty():
        if time() - 5 > stamp:
            break  # pragma: no cover
    try:
        feedback = queue.get(False)
    except:  # pragma: no cover
        safeprint("No feedback received from listener")
    global ext_ip, ext_port
    ext_ip = ""     # Does this affect peers?
    ext_port = -1   # Does this affect peers?
    if feedback != []:
        settings.outbound = feedback[0]
        if settings.outbound is not True:
            ext_ip, ext_port = feedback[1:3]
    return live


def main():
    # Begin Init
    settings.setup()
    try:
        import miniupnpc
    except:
        safeprint("Dependency miniupnpc is not installed. Running in outbound only mode")
        settings.config['outbound'] = True
    safeprint("settings are:")
    safeprint(settings.config)
    live = initParallels()
    peers.initializePeerConnections(settings.config['port'], ext_ip, ext_port)
    # End Init

    # Begin main loop
    if settings.config.get('seed'):
        safeprint("Seed mode activated")
        try:
            while True and not settings.config.get('test'):
                sleep(0.1)
        except KeyboardInterrupt:
            safeprint("Keyboard Interrupt")
    elif settings.config.get('server'):
        safeprint("Server mode activated")
    else:
        safeprint("Client mode activated")
    # End main loop

    # Begin shutdown
    safeprint("Beginning exit process")
    live.value = False
    settings.saveSettings()
    peers.saveToFile()
    bounty.saveToFile()
    # End shutdown

if __name__ == "__main__":
    main()
