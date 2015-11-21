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
        a = s.getsockname()[0]
        s.close()
        return a

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
        handlePeerRequest(con,False)
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

def requestBounties(address):
  con = socket.socket()
  con.settimeout(5)
  safeprint(address)
  try:
    safeprint(address.split(":")[0] + ":" + address.split(":")[1])
    con.connect((address.split(":")[0],int(address.split(":")[1])))
    con.send(bounty_request)
    connected = True
    s = "".encode('utf-8')
    while connected:
      a = con.recv(64)
      safeprint(a)
      if a == close_signal:
        con.close()
        connected = False
      else:
        s += a
    safeprint(pickle.loads(s))
    b = pickle.loads(s)
    for bounty in b:
      addBounty(pickle.dumps(bounty,1))
  except Exception as e:
    safeprint("Failed:" + str(type(e)))
    safeprint(e)
    remove.extend([address])

def initializePeerConnections(newPort,newip,newport):
  port = newPort
  ext_ip = newip
  ext_port = newport
  safeprint([ext_ip, ext_port])
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
  safeprint([ext_ip, ext_port])

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

def listen(port, outbound, q, v, serv):
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
    portForward(port)
  if ext_port == -1:
    outbound = True
  safeprint([outbound,ext_ip, ext_port])
  q.put([outbound,ext_ip,ext_port])
  while v.value:    #is True is implicit
    safeprint("listening on " + str(get_lan_ip()) + ":" + str(port))
    if not outbound:
      safeprint("forwarded from " + ext_ip + ":" + str(ext_port))
    try:
      conn, addr = server.accept()
      safeprint("connection accepted")
      b = conn.recv(len(peer_request))
      safeprint("Received: " + b.decode())
      if b == peer_request:
        handlePeerRequest(conn,True)
      elif b == bounty_request:
        handleBountyRequest(conn)
      elif b == incoming_bounty:
        handleIncomingBounty(conn)
      conn.send(close_signal)
      time.sleep(0.01)
      conn.close()
      safeprint("connection closed")
    except Exception as e:
      safeprint("Failed: " + str(type(e)))
      safeprint(e)

def handlePeerRequest(conn, exchange):
  if ext_port != -1:
    c = pickle.dumps(peerlist + [ext_ip+":"+str(ext_port)],1)
  c = pickle.dumps(peerlist,1)
  if type(c) != type("a".encode("utf-8")):
    safeprint("Test here")
    c = c.encode("utf-8")
  conn.send(c)
  time.sleep(0.01)
  if exchange:
    conn.send(peer_request)
    connected = True 
    s = ""
    while connected:
      d = conn.recv(64)
      safeprint(d.decode())
      if d == close_signal:
        connected = False
      else:
        s += d.decode()
    s = s.encode('utf-8')
    peerlist.extend(pickle.loads(s))
    trimPeers()

def handleIncomingBounty(conn):
  connected = True
  s = ""
  while connected:
    c = conn.recv(len(close_signal))
    safeprint(c.decode())
    if not c == close_signal:
      s += c.decode()
    else:
      connected = False
  safeprint("Adding bounty: " + s)
  if addBounty(s):
    conn.send(valid_signal)
  else:
    conn.send(invalid_signal)

def handleBountyRequest(conn):
  c = pickle.dumps(bountyList,1)
  if type(c) != type("a".encode("utf-8")):
    c = c.encode("utf-8")
  conn.send(c)
  time.sleep(0.01)
  
def portForward(port):
  try:
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
    u.selectigd()
    ext_ip = u.externalipaddress()
    safeprint("external ip is: " + str(ext_ip))
    for i in range(0,20):
      try:
        safeprint("Port forward try: " + str(i))
        if u.addportmapping(port+i, 'TCP', get_lan_ip(), port, 'Bounty Net', ''):
          ext_port = port + i
          safeprint("External port is " + str(ext_port))
          break
      except Exception as e:
        safeprint("Failed: " + str(type(e)))
        safeprint(e)
  except Exception as e:
    safeprint("Failed: " + str(type(e)))
    safeprint(e)
    outbound = True

class listener(multiprocessing.Process):  
  def __init__(self, port, outbound, q, v, serv):
    multiprocessing.Process.__init__(self)
    self.outbound = outbound
    self.port = port
    self.q = q
    self.v = v
    self.serv = serv
  def run(self):#pragma: no cover
    safeprint("listener started")
    listen(self.port,self.outbound,self.q,self.v,self.serv)
