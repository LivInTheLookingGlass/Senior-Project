import multiprocessing, os, pickle, select, socket, time

seedlist = ["127.0.0.1:44565", "localhost:44565", "10.132.80.128:44565"]
peerlist = ["10.132.80.138:44565"]
remove   = []

#constants
close_signal = "Close Signal"
peer_request = "Requesting Peers..."
peers_file   = "data" + os.sep + "peerlist.pickle"

Alive = True

def getFromFile():
  if os.path.exists(peers_file):
    peerlist = pickle.load(open(peers_file,"r"))

def saveToFile():
  if not os.path.exists(peers_file):
    os.mkdir(peers_file.split(os.sep)[0])
  pickle.dump(peerlist,open(peers_file,"w"))

def getFromSeeds():
  for seed in seedlist:
    print seed
    peerlist.extend(requestPeerlist(seed))
    time.sleep(1)

def requestPeerlist(address):
  con = socket.socket()
  print address
  try:
    print (address.split(":")[0],int(address.split(":")[1]))
    con.connect((address.split(":")[0],int(address.split(":")[1])))
    con.send(peer_request)
    connected = True
    s = ""
    while connected:
      a = con.recv(64)
      print a
      if not a == close_signal:
        s += a
      else:
        con.close()
        connected = False
    return pickle.loads(s)
  except Exception as e:
    print "Failed:", type(e)
    print e
    remove.extend([address])
    return []

def sendPeerlist(address):
  print "currently unsupported"
  s = pickle.dumps(peerlist)
  #send list

def initializePeerConnections():
  getFromFile()
  print "peers fetched from file"
  getFromSeeds()
  print "peers fetched from seedlist"
  trimPeers()
  if len(peerlist) < 12:
    print len(peerlist)
    newlist = []
    for peer in peerlist:
      newlist.extend(requestPeerlist(peer))
    peerlist.extend(newlist)
  trimPeers()
  print "peer network extended"
  saveToFile()
  print "peer network saved to file"

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

def listen(port, ID):
  server = socket.socket()
  server.bind(("0.0.0.0",port))
  server.listen(10)
  prid = "[" + str(ID) + "]"
  while True:
    print prid, "listening on", (get_lan_ip(),port)
    try:
      a, addr = server.accept()
      print prid, "connection accepted"
      b = a.recv(len(peer_request))
      print prid, "Received:", b
      if b == peer_request:
        a.send(pickle.dumps(peerlist + [get_lan_ip()+":"+str(port)]))
      a.send(close_signal)
      time.sleep(1)
      a.close()
    except Exception as e:
      print prid, "Failed:", type(e)
      print e

class listener(multiprocessing.Process):
  def __init__(self, threadID, port):
    multiprocessing.Process.__init__(self)
    self.threadID = threadID
    self.port = port
  def run(self):
    print "hi"
    listen(self.port,self.threadID)

if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

def get_lan_ip():
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
