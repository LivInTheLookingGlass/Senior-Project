import os, pickle, re, sys
from common.safeprint import safeprint
from multiprocessing import Lock
from hashlib import sha256

global bountyList
global bountyLock
global bounty_path
bountyList = []
bountyLock = Lock()
bounty_path = "data" + os.sep + "bounties.pickle"

class Bounty(object):
  ip = ""
  btc = ""
  reward = 0
  data = []
  
  def __init__(self, ipAddress, btcAddress, rewardAmount, dataList=[]):
    self.ip = ipAddress
    self.btc = btcAddress
    self.reward = rewardAmount
    self.data = dataList
    
  def isValid(self):
    try:
      safeprint("Testing IP address")
      #is IP valid
      b = int(self.ip.split(":")[1]) in range(1024,49152)
      b = int(self.ip.split(":")[0].split(".")[0]) in range(0,256) and b
      b = int(self.ip.split(":")[0].split(".")[1]) in range(0,256) and b
      b = int(self.ip.split(":")[0].split(".")[2]) in range(0,256) and b
      b = int(self.ip.split(":")[0].split(".")[3]) in range(0,256) and b
      if not b:
        return False
      #ping IP
      #is Bitcoin address valid
      safeprint("Testing Bitcoin address")
      address = str(self.btc)
      #The following is a soft check
      #A deeper check will need to be done in order to assure this is correct
      if not (check_bc_valid(address) and re.match(re.compile("^[a-zA-Z1-9]{26,35}$"),address)):
        return False
      #is reward valid
      safeprint("Testing reward")
      b = int(self.reward)
      return (b >= 0)
    except:
      return False
  
  def isPayable(self):
    #check if address has enough
    return False

def check_bc_valid(bc):
  n = 0
  for char in bc:
      n = n * 58 + '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'.index(char)
  if sys.version_info[0] < 3:
      bcbytes = (('%%0%dx' % (25 << 1) % n).decode('hex')[-25:])
      return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]
  else:
      bcbytes = n.to_bytes(25, 'big')
      return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]

def verify(string):
  test = pickle.loads(string)
  try:
    safeprint("Testing IP address")
    #is IP valid
    b = int(test.ip.split(":")[1]) in range(1024,49152)
    b = int(test.ip.split(":")[0].split(".")[0]) in range(0,256) and b
    b = int(test.ip.split(":")[0].split(".")[1]) in range(0,256) and b
    b = int(test.ip.split(":")[0].split(".")[2]) in range(0,256) and b
    b = int(test.ip.split(":")[0].split(".")[3]) in range(0,256) and b
    if not b:
      return False
    #ping IP
    #is Bitcoin address valid
    safeprint("Testing Bitcoin address")
    address = str(test.btc)
    #The following is a soft check
    #A deeper check will need to be done in order to assure this is correct
    if not (check_bc_valid(address) and re.match(re.compile("^[a-zA-Z1-9]{26,35}$"),address)):
      return False
    #is reward valid
    safeprint("Testing reward")
    b = int(test.reward)
    return (b >= 0)
  except:
    return False
    
def getBountyList():
  a = []
  with bountyLock:
    a = bountyList
  return a

def saveToFile(bountyList):
  if not os.path.exists(bounty_path.split(os.sep)[0]):
    os.mkdir(bounty_path.split(os.sep)[0])
  pickle.dump(bountyList,open(bounty_path, "wb"),1)
  return True

def loadFromFile():
  if os.path.exists(bounty_path):
    with bountyLock:
      bountyList = pickle.load(open(bounty_path,"rb"))
    return True
  return False
  
def addBounty(bounty):
  a = False
  safeprint((sys.version_info[0],sys.version_info[1],sys.version_info[2]))
  if type(bounty) == type("aaa") and sys.version_info[0] >= 3:
    safeprint("Fed as string; encoding utf-8")
    bounty = bounty.encode('utf-8')
  elif sys.version_info[0] == 2 and sys.version_info[1] == 6 and (type(bounty) == type("aaa") or type(bounty) == type(unicode("aaa"))):
    safeprint("Fed as string in 2.6; encoding ascii and ignoring errors")
    try:
      bounty = bounty.encode('ascii','ignore')
    except:
      try:
        bounty = str(bounty)
      except:
        safeprint("I guess we'll have to wing it")
  safeprint("External verify")
  a = verify(bounty)
  b = pickle.loads(bounty)
  safeprint("Internal verify")
  b = b.isValid()
  if a and b:
    with bountyLock:
      bountyList.append(bounty)
  return (a and b)

def getBounty(charity, factor):
  for bounty in bountyList:
    if best is None:
      best = bounty
    elif best.rewardAmount < bounty.rewardAmount and bounty.isValid() and (isPayable(factor) or charity):
      best = bounty
  return best
