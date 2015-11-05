import os, pickle, select, socket, time

seedlist = ["127.0.0.1:44565", "localhost:44565", "10.132.80.128:44565", "10.132.80.251:44565"]
peerlist = []
server = socket.socket()

def getFromFile():
  if os.path.exists("peerlist.pickle"):
    peerlist = pickle.load("peerlist.pickle")

def saveToFile():
  if os.path.exists("peerlist.pickle"):
    pickle.dump(peerlist,"peerlist.pickle")

def getFromSeeds():
  for seed in seedlist:
    print seed
    peerlist.extend(requestPeerlist(seed))
    time.sleep(3)

def requestPeerlist(address):
  con = socket.socket()
  try:
    print (address.split(":")[0],int(address.split(":")[1]))
    con.connect((address.split(":")[0],int(address.split(":")[1])))
    con.send("Requesting Peers...")
    connected = True
    s = ""
    while connected:
      a = con.recv(24)
      print a
      if not a == "Close Signal":
        s += a
      else:
        con.close()
        connected = False
    return pickle.loads(s)
  except Exception as e:
    print "Failed:", type(e)
    print e
    return []
  
def sendPeerlist(address):
  print "currently unsupported"
  s = pickle.dumps(peerlist)
  #send list

def initializePeerConnections():
  server.bind(("localhost",44564))
  getFromFile()
  print "peers fetched from file"
  getFromSeeds()
  print "peers fetched from seedlist"
  if len(peerlist) < 12:
    for peer in peerlist:
      peerlist.extend(requestPeerlist(peer))
  saveToFile()
  server.listen(5)

def listen():
  print "currently unsupported"
  server = socket.socket()
  server.bind((get_lan_ip(),44565))
  server.listen(5)
  while True:
    print "listening on", (get_lan_ip(),44565)
    a, addr = server.accept()
    print "connection accepted"
    b = a.recv(19)
    print b
    if b == "Requesting Peers...":
      a.send(pickle.dumps(peerlist))
    time.sleep(1)
    a.send("Close Signal")
    time.sleep(1)
    a.close()

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
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1",
            "wifi0",
            "ath0",
            "ath1",
            "ppp0",
            ]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip
