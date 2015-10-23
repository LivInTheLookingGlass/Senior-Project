import os, pickle, socket

seedlist = []
peerlist = []

def getFromFile():
  if os.path.exists("peerlist.pickle"):
    peerlist = pickle.load("peerlist.pickle")

def saveToFile():
  if os.path.exists("peerlist.pickle"):
    pickle.dump(peerlist,"peerlist.pickle")

def getFromSeeds():
  for seed in seedlist:
    peerlist.extend(requestPeerlist(seed))

def requestPeerlist(address):
  con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  con.connect(address.split(":"))
  con.send("Requesting Peers...")
  connected = True
  s = ""
  while connected:
    a = con.recv(1024)
    if a is not "Close Signal":
      s += a
    else:
      con.close()
  return pickle.loads(s)
  
def sendPeerlist(address):
  print "currently unsupported"
  s = pickle.dumps(peerlist)
  #send list

def initializePeerConnections():
  getFromFile()
  print "peers fetched from file"
  getFromSeeds()
  print "peers fetched from seedlist"
  if len(peerlist) < 12:
    for peer in peerlist:
      peerlist.extend(requestPeerlist(peer))
  saveToFile()
