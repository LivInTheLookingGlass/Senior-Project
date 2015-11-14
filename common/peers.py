import multiprocessing, os, pickle, select, socket, sys, time
from common.safeprint import safeprint
from common.bounty import *

global ext_port
global ext_ip
global port
ext_port = -1
ext_ip = ""
port = 44565

if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

def get_lan_ip():
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
        return s.getsockname()[0]

seedlist = ["127.0.0.1:44565", "localhost:44565", "10.132.80.128:44565"]
peerlist = [get_lan_ip() + ":44565", "24.10.111.111:44565"]
remove   = []
bounties = []

#constants
peers_file      = "data" + os.sep + "peerlist.pickle"
close_signal    = "Close Signal.......".encode("utf-8")
peer_request    = "Requesting Peers...".encode("utf-8")
bounty_request  = "Requesting Bounties".encode("utf-8")
incoming_bounty = "Incoming Bounty....".encode("utf-8")
valid_signal    = "Bounty was valid...".encode("utf-8")
invalid_signal  = "Bounty was invalid.".encode("utf-8")

Alive = True

def getFromFile():
  if os.path.exists(peers_file):
    peerlist = pickle.load(open(peers_file,"rb"))

def saveToFile():
  if not os.path.exists(peers_file.split(os.sep)[0]):
    os.mkdir(peers_file.split(os.sep)[0])
  pickle.dump(peerlist,open(peers_file,"wb"),1)

def getFromSeeds():
  for seed in seedlist:
    safeprint(seed)
    peerlist.extend(requestPeerlist(seed))
    time.sleep(1)

def requestPeerlist(address):
  con = socket.socket()
  con.settimeout(5)
  safeprint(address)
  try:
    safeprint(address.split(":")[0] + ":" + address.split(":")[1])
    con.connect((address.split(":")[0],int(address.split(":")[1])))
    con.send(peer_request)
    connected = True
    s = ""
    while connected:
      a = con.recv(64)
      safeprint(a.decode())
      if a == close_signal:
        con.close()
        connected = False
      elif a == peer_request:
        if not ext_ip == "":
          c = pickle.dumps(peerlist + [ext_ip+":"+str(ext_port)],1)
        c = pickle.dumps(peerlist,1)
        if type(c) != type("a".encode("utf-8")):
          safeprint("Test here")
          c = c.encode("utf-8")
        con.send(c)
        time.sleep(0.01)
        con.send(close_signal)
      else:
        s += a.decode()
    s = s.encode('utf-8')
    safeprint(pickle.loads(s))
    con = socket.socket()
    con.settimeout(5)
    #test section
    con.connect((address.split(":")[0],int(address.split(":")[1])))
    con.send(incoming_bounty)
    time.sleep(0.01)
    b = Bounty(get_lan_ip() + ":44565","1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9",1150)
    b = pickle.dumps(b,1)
    if type(b) == type("a"):
        b = b.encode('utf-8')
    safeprint(b)
    con.send(b)
    time.sleep(0.01)
    con.send(close_signal)
    time.sleep(0.01)
    con.close()
    #end test section
    return pickle.loads(s)
  except Exception as e:
    safeprint("Failed:" + str(type(e)))
    safeprint(e)
    remove.extend([address])
    return []

def initializePeerConnections(newPort):
  port = newPort
  getFromFile()
  safeprint("peers fetched from file")
  getFromSeeds()
  safeprint("peers fetched from seedlist")
  trimPeers()
  if len(peerlist) < 12:
    safeprint(len(peerlist))
    newlist = []
    for peer in peerlist:
      newlist.extend(requestPeerlist(peer))
    peerlist.extend(newlist)
  trimPeers()
  safeprint("peer network extended")
  saveToFile()
  safeprint("peer network saved to file")
  safeprint(peerlist)

def trimPeers():
  temp = list(set(peerlist))
  for peer in remove:
    try:
      del temp[temp.index(peer)]
    except:
      continue
  del remove[:]
  del peerlist[:]
  peerlist.extend(temp)

def listen(port, outbound): #pragma: no cover
  server = socket.socket()
  server.bind(("0.0.0.0",port))
  server.listen(10)
  ext_ip = ""
  ext_port = -1
  if outbound is True:
    safeprint("UPnP mode is disabled")
  else:
    safeprint("UPnP mode is enabled")
    import miniupnpc
    u = miniupnpc.UPnP(None, None, 200, port)
    safeprint('inital(default) values :')
    safeprint(' discoverdelay' + str(u.discoverdelay))
    safeprint(' lanaddr' + str(u.lanaddr))
    safeprint(' multicastif' + str(u.multicastif))
    safeprint(' minissdpdsocket' + str(u.minissdpdsocket))
    #u.minissdpdsocket = '../minissdpd/minissdpd.sock'
    # discovery process, it usualy takes several seconds (2 seconds or more)
    safeprint('Discovering... delay=%ums' % u.discoverdelay)
    safeprint(str(u.discover()) + 'device(s) detected')
    try:
      u.selectigd()
      ext_ip = u.externalipaddress()
      safeprint("external ip is: " + str(ext_ip))
    except Exception as e:
      safeprint("Failed: " + str(type(e)))
      safeprint(e)
      outbound = True
  if outbound is False:
    try:
      for i in range(0,20):
        safeprint("Port forward try: " + str(i))
        if u.addportmapping(port+i, 'TCP', get_lan_ip(), port, 'Bounty Net', ''):
          ext_port = port + i
          break
      safeprint("External port is " + str(ext_port))
    except Exception as e:
      safeprint("Failed: " + str(type(e)))
      safeprint(e)
      outbound = True
  while True:
    safeprint("listening on " + str(get_lan_ip()) + ":" + str(port))
    if not outbound:
      safeprint("forwarded from " + ext_ip + ":" + str(ext_port))
    try:
      a, addr = server.accept()
      safeprint("connection accepted")
      b = a.recv(len(peer_request))
      safeprint("Received: " + b.decode())
      if b == peer_request:
        if not outbound:
          c = pickle.dumps(peerlist + [ext_ip+":"+str(ext_port)],1)
        c = pickle.dumps(peerlist,1)
        if type(c) != type("a".encode("utf-8")):
          safeprint("Test here")
          c = c.encode("utf-8")
        a.send(c)
        time.sleep(0.01)
        a.send(peer_request)
        connected = True
        s = ""
        while connected:
          d = a.recv(64)
          safeprint(d.decode())
          if d == close_signal:
            connected = False
          elif d == peer_request:
            continue
          else:
            s += d.decode()
        s = s.encode('utf-8')
        peerlist.extend(pickle.loads(s))
        trimPeers()
      elif b == bounty_request:
        c = pickle.dumps(bountyList,1)
        if type(c) != type("a".encode("utf-8")):
          c = c.encode("utf-8")
        a.send(c)
        time.sleep(0.01)
      elif b == incoming_bounty:
        connected = True
        s = ""
        while connected:
          c = a.recv(len(close_signal))
          safeprint(c.decode())
          if not c == close_signal:
            s += c.decode()
          else:
            a.close()
            connected = False
        safeprint("Adding bounty: " + s.decode())
        if (verify(s.encode('utf-8'))):
          a.send(valid_signal)
        else:
          a.send(invalid_signal)
        addBounty(s)
      a.send(close_signal)
      time.sleep(0.01)
      a.close()
      safeprint("connection closed")
    except Exception as e:
      safeprint("Failed: " + str(type(e)))
      safeprint(e)

class listener(multiprocessing.Process):  #pragma: no cover
  def __init__(self, port, outbound):
    multiprocessing.Process.__init__(self)
    self.outbound = outbound
    self.port = port
  def run(self):
    safeprint("listener started")
    listen(self.port,self.outbound)
