from multiprocessing import Queue
import multiprocessing, os, pickle, select, socket, sys, time
from common.safeprint import safeprint
from common.bounty import *

global ext_port
global ext_ip
global port
ext_port = -1
ext_ip = ""
port = 44565

seedlist = ["127.0.0.1:44565", "localhost:44565", "10.132.80.128:44565"]
peerlist = ["24.10.111.111:44565"]
remove   = []
bounties = []

#constants
peers_file      = "data" + os.sep + "peerlist.pickle"
close_signal    = "Close Signal".encode("utf-8")
peer_request    = "Requesting Peers".encode("utf-8")
bounty_request  = "Requesting Bounties".encode("utf-8")
incoming_bounty = "Incoming Bounty".encode("utf-8")
valid_signal    = "Bounty was valid".encode("utf-8")
invalid_signal  = "Bounty was invalid".encode("utf-8")

sig_length = len(max(close_signal,peer_request,bounty_request,incoming_bounty,valid_signal,invalid_signal,key=len))

def pad(string):
    return string + " ".encode('utf-8') * (sig_length - (((len(string) - 1) % sig_length) + 1))

close_signal    = pad(close_signal)
peer_request    = pad(peer_request)
bounty_request  = pad(bounty_request)
incoming_bounty = pad(incoming_bounty)
valid_signal    = pad(valid_signal)
invalid_signal  = pad(invalid_signal)

if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

def get_lan_ip():
    """Retrieves the LAN ip. Unfortunately uses an external connection in Python 3."""
    if sys.version_info[0] < 3:
        ip = socket.gethostbyname(socket.gethostname())
        if ip.startswith("127.") and os.name != "nt":
            interfaces = ["eth0","eth1","eth2","wlan0","wlan1","wifi0","ath0","ath1","ppp0",]
            for ifname in interfaces:
                try:
                    ip = get_interface_ip(ifname)
                    break
                except IOError:
                    pass
        return ip
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))
        a = s.getsockname()[0]
        s.close()
        return a

def getFromFile():
    """Load peerlist from a file"""
    if os.path.exists(peers_file):
        try:
            peerlist = pickle.load(open(peers_file,"rb"))
        except:
            safeprint("Could not load peerlist from file")

def saveToFile():
    """Save peerlist to a file"""
    if not os.path.exists(peers_file.split(os.sep)[0]):
        os.mkdir(peers_file.split(os.sep)[0])
    pickle.dump(peerlist,open(peers_file,"wb"),0)

def getFromSeeds():
    """Make peer requests to each address on the seedlist"""
    for seed in seedlist:
        safeprint(seed,verbosity=1)
        peerlist.extend(requestPeerlist(seed))
        time.sleep(1)

def requestPeerlist(address):
    """Request the peerlist of another node. Currently has additional test commands"""
    con = socket.socket()
    con.settimeout(5)
    safeprint(address,verbosity=1)
    try:
        safeprint(address.split(":")[0] + ":" + address.split(":")[1])
        con.connect((address.split(":")[0],int(address.split(":")[1])))
        con.send(peer_request)
        connected = True
        received = "".encode('utf-8')
        while connected:
            packet = con.recv(sig_length)
            safeprint(packet.decode(),verbosity=3)
            if packet == close_signal:
                con.close()
                connected = False
            elif packet == peer_request:
                handlePeerRequest(con,False)
                con.send(close_signal)
            else:
                received += packet
        safeprint(pickle.loads(received),verbosity=2)
        #test section
        con = socket.socket()
        con.settimeout(5)
        con.connect((address.split(":")[0],int(address.split(":")[1])))
        con.send(incoming_bounty)
        bounty = Bounty(get_lan_ip() + ":44565","1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9",1440)
        bounty = pickle.dumps(bounty,0)
        if type(bounty) == type("a"):
            bounty = bounty.encode('utf-8')
        safeprint(bounty,verbosity=3)
        con.send(pad(bounty))
        con.send(close_signal)
        con.close()
        #end test section
        return pickle.loads(received)
    except Exception as error:
        safeprint("Failed:" + str(type(error)))
        safeprint(error)
        remove.extend([address])
        return []

def requestBounties(address):
    """Request the bountylist of another node"""
    con = socket.socket()
    con.settimeout(5)
    safeprint(address,verbosity=1)
    try:
        safeprint(address.split(":")[0] + ":" + address.split(":")[1])
        con.connect((address.split(":")[0],int(address.split(":")[1])))
        con.send(bounty_request)
        connected = True
        received = "".encode('utf-8')
        while connected:
            packet = con.recv(sig_length)
            safeprint(packet,verbosity=3)
            if packet == close_signal:
                con.close()
                connected = False
            else:
                received += packet
        safeprint(pickle.loads(received),verbosity=2)
        try:
            bounties = pickle.loads(received)
            for bounty in bounties:
                addBounty(pickle.dumps(bounty,0))
                safeprint("Bounty added")
        except Exception as error:
            safeprint("Could not add bounties. This is likely because you do not have the optional dependency PyCrypto")
            safeprint(type(error))
            #later add function to request without charity bounties
    except Exception as error:
        safeprint("Failed:" + str(type(error)))
        safeprint(error)
        remove.extend([address])

def initializePeerConnections(newPort,newip,newport):
    """Populate the peer list from a previous session, seeds, and from the peer list if its size is less than 12. Then save this new list to a file"""
    port = newPort        #Does this affect the global variable?
    ext_ip = newip        #Does this affect the global variable?
    ext_port = newport    #Does this affect the global variable?
    safeprint([ext_ip, ext_port])
    getFromFile()
    safeprint("peers fetched from file",verbosity=1)
    getFromSeeds()
    safeprint("peers fetched from seedlist",verbosity=1)
    trimPeers()
    if len(peerlist) < 12:
        safeprint(len(peerlist))
        newlist = []
        for peer in peerlist:
            newlist.extend(requestPeerlist(peer))
        peerlist.extend(newlist)
    trimPeers()
    safeprint("peer network extended",verbosity=1)
    saveToFile()
    safeprint("peer network saved to file",verbosity=1)
    safeprint(peerlist)
    safeprint([ext_ip, ext_port])

def trimPeers():
    """Trim the peerlist to a single set, and remove any that were marked as erroneous before"""
    temp = list(set(peerlist[:]))
    for peer in remove:
        try:
            del temp[temp.index(peer)]
        except:
            continue
    del remove[:]
    del peerlist[:]
    peerlist.extend(temp)

def listen(port, outbound, q, v, serv):
    """BLOCKING function which should only be run in a daemon thread. Listens and responds to other nodes"""
    if serv:
        from server.bounty import verify, addBounty
    server = socket.socket()
    server.bind(("0.0.0.0",port))
    server.listen(10)
    server.settimeout(5)
    if sys.version_info[0] < 3 and sys.platform == "win32":
        server.setblocking(True)
    ext_ip = ""
    ext_port = -1
    if outbound is True:
        safeprint("UPnP mode is disabled")
    else:
        safeprint("UPnP mode is enabled")
        if not portForward(port):
            outbound = True
    safeprint([outbound,ext_ip, ext_port])
    q.put([outbound,ext_ip,ext_port])
    while v.value:    #is True is implicit
        safeprint("listening on " + str(get_lan_ip()) + ":" + str(port),verbosity=3)
        if not outbound:
            safeprint("forwarded from " + ext_ip + ":" + str(ext_port),verbosity=3)
        try:
            conn, addr = server.accept()
            server.setblocking(True)
            conn.setblocking(True)
            safeprint("connection accepted")
            packet = conn.recv(sig_length)
            safeprint("Received: " + packet.decode(),verbosity=3)
            if packet == peer_request:
                handlePeerRequest(conn,True)
            elif packet == bounty_request:
                handleBountyRequest(conn)
            elif packet == incoming_bounty:
                handleIncomingBounty(conn)
            conn.send(close_signal)
            conn.close()
            server.settimeout(5)
            safeprint("connection closed")
        except Exception as error:
            safeprint("Failed: " + str(type(error)))
            safeprint(error)

def handlePeerRequest(conn, exchange):
    """Given a socket, send the proper messages to complete a peer request"""
    if ext_port != -1:
        send = pickle.dumps(peerlist[:] + [ext_ip+":"+str(ext_port)],0)
    send = pickle.dumps(peerlist[:],0)
    if type(send) != type("a".encode("utf-8")):
        safeprint("Test here")
        send = send.encode("utf-8")
    conn.send(pad(send))
    if exchange:
        conn.send(peer_request)
        connected = True
        received = "".encode('utf-8')
        while connected:
            packet = conn.recv(sig_length)
            safeprint(packet,verbosity=3)
            if packet == close_signal:
                connected = False
            else:
                received += packet
        peerlist.extend(pickle.loads(received))
        trimPeers()

def handleIncomingBounty(conn):
    """Given a socket, store an incoming bounty, and report it valid or invalid"""
    connected = True
    received = "".encode('utf-8')
    while connected:
        packet = conn.recv(sig_length)
        safeprint(packet,verbosity=3)
        if not packet == close_signal:
            received += packet
        else:
            connected = False
    safeprint("Adding bounty: " + received.decode())
    try:
        if addBounty(received):
            conn.send(valid_signal)
            mouth = socket.socket()
            import settings
            mouth.connect(("localhost",settings.config['port'] + 1))
            mouth.send(incoming_bounty)
            mouth.send(pad(received))
            mouth.send(close_signal)
            mouth.close()
        else:
            conn.send(invalid_signal)
    except:
        safeprint("They closed too early")

def handleIncomingBountyP(conn):
    """Given a socket, store an incoming bounty, and report it valid or invalid"""
    connected = True
    received = "".encode('utf-8')
    while connected:
        packet = conn.recv(sig_length)
        safeprint(packet,verbosity=3)
        if not packet == close_signal:
            received += packet
        else:
            connected = False
    safeprint("Adding bounty: " + received.decode(),verbosity=2)
    try:
        bounty = pickle.loads(received)
        if bounty.isValid():
            from multiprocessing.pool import ThreadPool
            ThreadPool().map(propagate,[(bounty,x) for x in peerlist[:]])
    except Exception as error:
        safeprint("bounty propagation failed: " + str(type(error)))
        safeprint(error)
        return False

def propagate(tup):
    try:
        conn = socket.socket()
        address = tup[1]
        conn.connect((address.split(":")[0],int(address.split(":")[1])))
        conn.send(incoming_bounty)
        conn.send(pad(pickle.dumps(tup[0],0)))
        conn.recv(sig_length)
        conn.close()
    except socket.error as Error:
        safeprint("Connection to " + str(address) + " failed; cannot propagate")

def portForward(port):
    """Attempt to forward a port on your router to the specified local port. Prints lots of debug info."""
    try:
        import miniupnpc
        u = miniupnpc.UPnP(None, None, 200, port)
        #Begin Debug info
        safeprint('inital(default) values :')
        safeprint(' discoverdelay' + str(u.discoverdelay))
        safeprint(' lanaddr' + str(u.lanaddr))
        safeprint(' multicastif' + str(u.multicastif))
        safeprint(' minissdpdsocket' + str(u.minissdpdsocket))
        safeprint('Discovering... delay=%ums' % u.discoverdelay)
        safeprint(str(u.discover()) + 'device(s) detected')
        #End Debug info
        u.selectigd()
        global ext_ip
        ext_ip = u.externalipaddress()
        safeprint("external ip is: " + str(ext_ip))
        for i in range(0,20):
            try:
                safeprint("Port forward try: " + str(i),verbosity=1)
                if u.addportmapping(port+i, 'TCP', get_lan_ip(), port, 'Bounty Net', ''):
                    global ext_port
                    ext_port = port + i
                    safeprint("External port is " + str(ext_port))
                    return True
            except Exception as error:
                safeprint("Failed: " + str(type(error)))
                safeprint(error)
    except Exception as error:
        safeprint("Failed: " + str(type(error)))
        safeprint(error)
        return False

def listenp(port, v):
    """BLOCKING function which should only be run in a daemon thread. Listens and responds to other nodes"""
    server = socket.socket()
    server.bind(("0.0.0.0",port))
    server.listen(10)
    server.settimeout(5)
    if sys.version_info[0] < 3 and sys.platform == "win32":
        server.setblocking(True)
    while v.value:    #is True is implicit
        safeprint("listenp-ing on localhost:" + str(port),verbosity=3)
        try:
            conn, addr = server.accept()
            server.setblocking(True)
            conn.setblocking(True)
            safeprint("connection accepted")
            packet = conn.recv(sig_length)
            safeprint("Received: " + packet.decode(),verbosity=3)
            if packet == incoming_bounty:
               handleIncomingBountyP(conn)
            conn.send(close_signal)
            conn.close()
            server.settimeout(5)
            safeprint("connection closed")
        except Exception as error:
            safeprint("Failed: " + str(type(error)))
            safeprint(error)

class listener(multiprocessing.Process): #pragma: no cover
    """A class to deal with the listener method"""
    def __init__(self, port, outbound, q, v, serv):
        multiprocessing.Process.__init__(self)
        self.outbound = outbound
        self.port = port
        self.q = q
        self.v = v
        self.serv = serv
    def run(self):
        safeprint("listener started")
        self.sync(self.items)
        listen(self.port,self.outbound,self.q,self.v,self.serv)
        safeprint("listener stopped")
    def sync(self,items):
        if items == {}:
            return
        if items.get('config'):
            from common import settings
            settings.config = items.get('config')
        if items.get('peerList'):
            global peerlist
            peerList = items.get('peerList')
        if items.get('bountyList'):
            from common import bounty
            bounty.bountyList = items.get('bountyList')
        if items.get('bountyLock'):
            from common import bounty
            bounty.bountyLock = items.get('bountyLock')
        if items.get('keyList'):
            from common import bounty
            boutny.keyList = items.get('keyList')

class propagator(multiprocessing.Process): #pragma: no cover
    """A class to deal with the listener method"""
    def __init__(self, port, v):
        multiprocessing.Process.__init__(self)
        self.port = port
        self.v = v
    def run(self):
        safeprint("propagator started")
        self.sync(self.items)
        listenp(self.port, self.v)
        safeprint("propagator stopped")
    def sync(self,items):
        if items == {}:
            return
        if items.get('config'):
            from common import settings
            settings.config = items.get('config')
        if items.get('peerList'):
            global peerlist
            peerList = items.get('peerList')
        if items.get('bountyList'):
            from common import bounty
            bounty.bountyList = items.get('bountyList')
        if items.get('bountyLock'):
            from common import bounty
            bounty.bountyLock = items.get('bountyLock')
        if items.get('keyList'):
            from common import bounty
            boutny.keyList = items.get('keyList')
