import os, pickle, re, sys
from common.safeprint import safeprint
from multiprocessing import Lock
from hashlib import sha256

global bountyList
global bountyLock
global bountyPath
bountyList = []
bountyLock = Lock()
bounty_path = "data" + os.sep + "bounties.pickle"

class Bounty(object):
  """An object representation of a Bounty

  Parts:
  ip       -- The ip address of the requesting node
  btc      -- The Bitcoin address of the requesting party
  reward   -- The reward amount in Satoshis to be given over 24 hours (x | x == 0 or 1440 <= x <= 100000000)
  id       -- A value set by the issuer to determine which problem/test to send
  data     -- A dictionary containing optional, additional information
    author -- String which represents the group providing the Bounty
    reqs   -- Dict containing requirements keyed by the related python calls ("sys.platform":"win32")
    TDL    -- More to be defined in later versions
  """
  ip = ""
  btc = ""
  reward = 0
  data = {}
  
  def __repr__(self):
    """Gives a string representation of the bounty"""
    return ("<Bounty: ip=" + str(self.ip) + ", btc=" + str(self.btc) + ", reward=" + str(self.reward) + ", data=" + str(self.data) + ">")
  
  def __init__(self, ipAddress, btcAddress, rewardAmount, dataDict={}):
    """Initialize a Bounty; constructor"""
    self.ip = ipAddress
    self.btc = btcAddress
    self.reward = rewardAmount
    self.data = dataDict
    
  def isValid(self):
    """Internal method which checks the Bounty as valid under the most minimal version

    ip     -- Must be in valid range
    btc    -- Must be in valid namespace
    reward -- Must be in valid range
    """
    try:
      safeprint("Testing IP address")
      #is IP valid
      boolean = int(self.ip.split(":")[1]) in range(1024,49152)
      boolean = int(self.ip.split(":")[0].split(".")[0]) in range(0,256) and boolean
      boolean = int(self.ip.split(":")[0].split(".")[1]) in range(0,256) and boolean
      boolean = int(self.ip.split(":")[0].split(".")[2]) in range(0,256) and boolean
      boolean = int(self.ip.split(":")[0].split(".")[3]) in range(0,256) and boolean
      if not boolean:
        return False
      #ping IP
      #is Bitcoin address valid
      safeprint("Testing Bitcoin address")
      address = str(self.btc)
      #The following is a soft check
      #A deeper check will need to be done in order to assure this is correct
      if not checkAddressValid(address):
        return False
      #is reward valid
      safeprint("Testing reward")
      reward = int(self.reward)
      return (reward == 0 or (reward >= 1440 and reward <= 100000000))
    except:
      return False
  
  def isPayable(self, factor):
    """check if address has enough"""
    return True

def checkAddressValid(address):
  """Check to see if a Bitcoin address is within the valid namespace. Will potentially give false positives based on leading 1s"""
  if not re.match(re.compile("^[a-zA-Z1-9]{26,35}$"),address):
    return False
  decimal = 0
  for char in address:
      decimal = decimal * 58 + '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'.index(char)
  if sys.version_info[0] < 3:
      """long does not have a to_bytes() in versions less than 3. This is an equivalent function"""
      bcbytes = (('%%0%dx' % (25 << 1) % decimal).decode('hex')[-25:])
      return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]
  else:
      bcbytes = decimal.to_bytes(25, 'big')
      return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]

def verify(string):
  """External method which checks the Bounty as valid under implementation-specific requirements. This can be defined per user.

  ip     -- Must be in valid range
  btc    -- Must be in valid namespace
  reward -- Must be in valid range
  """
  test = pickle.loads(string)
  try:
    safeprint("Testing IP address")
    #is IP valid
    boolean = int(test.ip.split(":")[1]) in range(1024,49152)
    boolean = int(test.ip.split(":")[0].split(".")[0]) in range(0,256) and boolean
    boolean = int(test.ip.split(":")[0].split(".")[1]) in range(0,256) and boolean
    boolean = int(test.ip.split(":")[0].split(".")[2]) in range(0,256) and boolean
    boolean = int(test.ip.split(":")[0].split(".")[3]) in range(0,256) and boolean
    if not boolean:
      return False
    #ping IP
    #is Bitcoin address valid
    safeprint("Testing Bitcoin address")
    address = str(test.btc)
    #The following is a soft check
    #A deeper check will need to be done in order to assure this is correct
    if not checkAddressValid(address):
      return False
    #is reward valid
    safeprint("Testing reward")
    reward = int(test.reward)
    return (reward == 0 or (reward >= 1440 and reward <= 100000000))
  except:
    return False
    
def getBountyList():
  """Retrieves the bounty list. Temporary method"""
  temp = []
  with bountyLock:
    temp = bountyList
  return temp

def saveToFile(bountyList):
  """Save the current bounty list to a file"""
  if not os.path.exists(bounty_path.split(os.sep)[0]):
    os.mkdir(bounty_path.split(os.sep)[0])
  pickle.dump(bountyList,open(bounty_path, "wb"),1)
  return True

def loadFromFile():
  """Load a previous bounty list from a file"""
  if os.path.exists(bounty_path):
    with bountyLock:
      bountyList = pickle.load(open(bounty_path,"rb"))
    return True
  return False
  
def addBounty(bounty):
  """Verify a bounty, and add it to the list if it is valid"""
  first = False
  safeprint([sys.version_info[0],sys.version_info[1],sys.version_info[2]])
  if sys.version_info[0] == 2 and sys.version_info[1] == 6 and (type(bounty) == type("aaa") or type(bounty) == type(unicode("aaa"))):
    safeprint("Fed as string in 2.6; encoding ascii and ignoring errors")
    try:
      bounty = bounty.encode('ascii','ignore')
    except:
      bounty = str(bounty)
  elif type(bounty) == type("aaa") and sys.version_info[0] >= 3:
    safeprint("Fed as string; encoding utf-8")
    bounty = bounty.encode('utf-8')
  safeprint("External verify")
  first = verify(bounty)
  bounty = pickle.loads(bounty)
  safeprint("Internal verify")
  second = bounty.isValid()
  if first and second:
    with bountyLock:
      bountyList.append(bounty)
  return (first and second)

def getBounty(charity, factor):
  """Retrieve the next best bounty from the list"""
  temp = getBountyList()
  safeprint("bountyList = " + str(temp))
  if temp == []:
    return None
  elif charity:
    for bounty in temp:
      if bounty.isValid():
        index = a.index(bounty)
        return a.pop(index)
  else:
    best = None
    for bounty in temp:
      if best is None:
        best = bounty
      elif best.reward < bounty.reward and bounty.isValid() and bounty.isPayable(factor):
        best = bounty
    return best
