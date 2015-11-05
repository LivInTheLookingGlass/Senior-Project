import os, pickle, select, socket, time

seedlist = [socket.gethostname() + ":44565"]
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
  server.bind((socket.gethostname(),44564))
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
  server.bind((socket.gethostname(),44565))
  server.listen(5)
  while True:
    print "listening on", (socket.gethostname(),44565)
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
