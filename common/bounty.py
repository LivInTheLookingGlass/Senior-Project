import os, pickle, re, sys, rsa
from common.safeprint import safeprint
from common.call import parse
from multiprocessing import Lock
from hashlib import sha256

global bountyList
global bountyLock
global bountyPath
global masterKey
bountyList = []
bountyLock = Lock()
bounty_path = "data" + os.sep + "bounties.pickle"
masterKey = rsa.PublicKey(729718364227516960054295457142870147346925650464049779453646035926050199850326176647776838438938636661228002448973439854960184665555127389717151244506525402822373346832616397761206559623788599190346863336276264188776227828388404545963626831368271897836511731886293682431585966696566956586753957061875750759629551953550884681595197232292996000727346222730268449333005244786147077213736904023547731667408727418270821683767049274149406495083497549800959104387705136505347356831591749348784075618969053560235935338903984498115314670847476855038220451066460680035126053662454299081605363723838286302366301689234068690059316763799353143310559458946931318030844074363736788753178540199530225135107033856254305990087025967311915085112106420563306477842216888317797721574213850513617438213884040008525804176775715666690615899232712962058014027424402924843894781126276571499753462902008866715676378206701092204594546847042695125234724069900669714879723998617459025957963035684337989448663829900190832766576886449445998282639604992499686311883781123909372514474812566745325833006488779304055744191085394500902876859106482982701389204359219619381519269665200901406370105464312892270576240630264902441599619105421899943737252817890677315597882826571452667291297867328746814757255859312415632041433394104078891786311847142328363538513641680341734265250695496776566453276314580141676284207452110911626332891796798261026918947965108108877705758484536741616285552644326769470282221294071586139149996954364049943466039880711404230731628646248873232006643911012626023072154931894232739379505522865390152470432852547479160421591889324386660716759305915846468178029427406274264127584562536435501990522185363177223199949369223173966625384842438760255385301454341488784995219962112304732703967034969073210830294157329183542340361222144325778056660904508019431390791813146428095240192923570820580206747811269863474545538133775066351370475810177599879939522958590455452068291841209413729663053749796655380139821219686135783575616500844500412856724119371178526348549811013160430296131484346160922951511938309653435559070497873479498675961624001852506934102504791910222791868089298784254619281037009019775386472113074556466631655138811963898397216625947305254734110750776827226524243761296420962180234223676323640815767978717570666035083384226389557220885498260773635973720746044553716885329739097031530119234094297080532925101344078010970180292718887769653856948048674677603855338372966228989, 65537)


def getUTC():
    from calendar import timegm
    from time import gmtime
    return timegm(gmtime())


class Bounty(object):
    """An object representation of a Bounty
    Parts:
    ip         -- The ip address of the requesting node
    btc        -- The Bitcoin address of the requesting party
    reward     -- The reward amount in satoshis to be given over 24 hours
                   (x == 0 or 1440 <= x <= 100000000) (1440 is 1 satoshi/min)
    ident      -- A value set by the issuer to determine which problem/test to send
    timeout    -- Unix time at which the bounty expires (defaults to 24 hours)
    data       -- A dictionary containing optional, additional information
        author -- String which represents the group providing the Bounty
        reqs   -- Dict containing requirements keyed by the related python call
                   ("sys.platform":"win32")
        perms  -- Dict containing the minimum required security policies
                   (if empty, most restrictive assumed)
        key    -- A tuple which contains the RSA n and e values for this Bounty
                   (required only when reward is 0)
        sig    -- A Bytes object of str(Bounty) signed by the above key
                   (required only when reward is 0)
        TDL    -- More to be defined in later versions
    """

    def __repr__(self):
        """Gives a string representation of the bounty"""
        output = "<Bounty: ip=" + str(self.ip) + ", btc=" + str(self.btc) + ", reward=" + str(self.reward)
        if self.ident != None:
            output = output + ", id=" + str(self.ident)
        if self.timeout is not None:
            output = output + ", timeout=" + str(self.timeout)
        if self.data and self.data != {'author': '', 'reqs': {}, 'perms': {}}:
            if self.data.get('author') and self.data.get('author') != '':
                output = output + ", author=" + str(self.data.get('author'))
            if self.data.get('reqs') and self.data.get('reqs') != {} and isinstance(self.data.get('reqs'), dict):
                output = output + ", reqs=" + str(sorted(self.data.get('reqs').items(), key=lambda x: x[0]))
            if self.data.get('perms') and self.data.get('perms') != {} and isinstance(self.data.get('perms'), dict):
                output = output + ", perms=" + str(sorted(self.data.get('perms').items(), key=lambda x: x[0]))
        return output + ">"

    def __eq__(self, other):
        """Determines whether the bounties are equal"""
        try:
            return (self.reward == other.reward) and (self.ident == other.ident) and (self.data == other.data)
        except:
            return False

    def __ne__(self, other):
        """Determines whether the bounties are unequal"""
        try:
            return not self.__eq__(other)
        except:
            return False

    def __lt__(self, other):
        """Determines whether this bounty has a lower priority"""
        try:
            if self.reward < other.reward:
                return True
            elif self.timeout < other.timeout:
                return True
            else:
                return False
        except:
            return False

    def __gt__(self, other):
        """Determines whether this bounty has a higher priority"""
        try:
            if self.reward > other.reward:
                return True
            elif self.timeout > other.timeout:
                return True
            else:
                return False
        except:
            return False

    def __le__(self, other):
        """Determines whether this bounty has a lower priority or is equal"""
        boolean = self.__lt__(other)
        if boolean:
            return boolean
        else:
            return self.__eq__(other)

    def __ge__(self, other):
        """Determines whether this bounty has a higher or is equal"""
        boolean = self.__gt__(other)
        if boolean:
            return boolean
        else:
            return self.__eq__(other)

    def __hash__(self):
        h = [self.__repr__()]
        if self.data.get('key') or self.data.get('sig') or self.data.get('cert'):
            h.append(str(self.data))
        return hash(tuple(h))

    def __init__(self, ipAddress, btcAddress, rewardAmount, **kargs):
        """Initialize a Bounty; constructor"""
        self.ip = ipAddress
        self.btc = btcAddress
        self.reward = rewardAmount
        self.ident = None
        if kargs.get('timeout') is not None:
            self.timeout = kargs.get('timeout')
        else:
            self.timeout = getUTC() + 86400
        self.data = {'author': '',
                     'reqs': {},
                     'perms': {}}
        if kargs.get('ident') is not None:
            self.ident = kargs.get('ident')
        if kargs.get('dataDict') is not None:
            self.data.update(kargs.get('dataDict'))
        if kargs.get('keypair') is not None:
            self.sign(kargs.get('keypair'))

    def isValid(self):
        """Internal method which checks the Bounty as valid under the most minimal version

        ip      -- Must be in valid range
        btc     -- Must be in valid namespace
        reward  -- Must be in valid range
        timeout -- Must be greater than the current time
        """
        try:
            safeprint("Testing IP address", verbosity=1)
            if not checkIPAddressValid(self.ip):
                return False
            safeprint("Testing Bitcoin address", verbosity=1)
            # The following is a soft check
            # A deeper check will need to be done in order to assure this is correct
            if not checkBTCAddressValid(self.btc):
                return False
            safeprint("Testing reward and/or signiture validity", verbosity=1)
            if self.reward not in range(1440, 100000001) or (not self.reward and self.checkSign()):
                return False
            safeprint("Testing timeout", verbosity=1)
            if self.timeout < getUTC():  # check against current UTC
                return False
            safeprint("Testing bounty requirements", verbosity=1)
            if parse(self.data.get('reqs')):
                return 1
            return -1
        except:
            return False

    def isPayable(self, factor):
        """check if address has enough"""
        return True  # later make this a wrapper for pywallet.balance()

    def checkSign(self):
        """check if the signature attatched to the Bounty is valid"""
        try:
            from rsa import verify, PublicKey
            safeprint(keyList)
            if self.data.get('cert'):  # where key = (PublicKey.n, PublicKey.e)
                expected = str(self).encode('utf-8')
                n = self.data.get('key')[0]
                e = self.data.get('key')[1]
                if rsa.verify(str((n, e)), self.data.get('cert'), masterKey):
                    return verify(expected, self.data.get('sig'), PublicKey(n, e))
            return False
        except:
            return False

    def sign(self, privateKey):    #where privateKey is a private key generated by rsa.PrivateKey()
        """Signa bounty and attach the key value"""
        try:
            from rsa import sign
            expected = str(self).encode('utf-8')
            self.data.update({'key' : (privateKey.n, privateKey.e),
                              'sig' : sign(expected, privateKey, 'SHA-256')})
        except:
            return False


def checkBTCAddressValid(address):
    """Check to see if a Bitcoin address is within the valid namespace. Will potentially give false positives based on leading 1s"""
    if not re.match(re.compile("^[a-km-zA-HJ-Z1-9]{26,35}$"), address):
        return False
    decimal = 0
    for char in address:
        decimal = decimal * 58 + '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'.index(char)
    bcbytes = ""
    if sys.version_info[0] < 3:
        """long does not have a to_bytes() in versions less than 3. This is an equivalent function"""
        bcbytes = (('%%0%dx' % (25 << 1) % decimal).decode('hex')[-25:])
    else:
        bcbytes = decimal.to_bytes(25, 'big')
    return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]


def checkIPAddressValid(address):
    try:
        a = socket.getaddrinfo(*address)
        return len(address[0].split(":")) == 1 and address[0] in range(1024, 49152)  # Make sure it's not ipv6
    except:
        return False


def verify(string):
    """External method which checks the Bounty as valid under implementation-specific requirements. This can be defined per user.

    ip      -- Must be in valid range
    btc     -- Must be in valid namespace
    reward  -- Must be in valid range
    timeout -- Must be greater than the current time
    """
    test = string
    if isinstance(test, str):
        test = pickle.loads(string)
    try:
            safeprint("Testing IP address", verbosity=1)
            if not checkIPAddressValid(test.ip):
                return False
            safeprint("Testing Bitcoin address", verbosity=1)
            # The following is a soft check
            # A deeper check will need to be done in order to assure this is correct
            if not checkBTCAddressValid(test.btc):
                return False
            safeprint("Testing reward and/or signiture validity", verbosity=1)
            if test.reward not in range(1440, 100000001) or (not test.reward and test.checkSign()):
                return False
            safeprint("Testing timeout", verbosity=1)
            if test.timeout < getUTC():  # check against current UTC
                return False
            safeprint("Testing bounty requirements", verbosity=1)
            if parse(test.data.get('reqs')):
                return 1
            return -1
    except:
        return False


def getBountyList():
    """Retrieves the bounty list. Temporary method"""
    temp = []
    with bountyLock:
        temp = bountyList[:]
    return temp


def saveToFile():
    """Save the current bounty list to a file"""
    if not os.path.exists(bounty_path.split(os.sep)[0]):
        os.mkdir(bounty_path.split(os.sep)[0])
    pickle.dump(getBountyList(), open(bounty_path, "wb"), 0)
    return True


def loadFromFile():
    """Load a previous bounty list from a file"""
    if os.path.exists(bounty_path):
        with bountyLock:
            try:
                safeprint("Loading bounty list from file", verbosity=2)
                templist = pickle.load(open(bounty_path, "rb"))
                safeprint(addBounties(templist), verbosity=3)
                safeprint("Bounty list loaded and added", verbosity=2)
            except:
                return False
        return True
    return False


def addBounty(bounty):
    """Verify a bounty, and add it to the list if it is valid"""
    first = False
    safeprint([sys.version_info[0], sys.version_info[1], sys.version_info[2]])
    if sys.version_info[0] == 2 and sys.version_info[1] == 6 and (isinstance(bounty, str) or isinstance(bounty, unicode)):
        safeprint("Fed as string in 2.6; encoding ascii and ignoring errors")
        try:
            bounty = bounty.encode('ascii', 'ignore')
        except:
            bounty = str(bounty)
    elif type(bounty) == type("aaa") and sys.version_info[0] >= 3:
        safeprint("Fed as string; encoding utf-8")
        bounty = bounty.encode('utf-8')
    safeprint(pickle.loads(bounty))
    safeprint("External verify", verbosity=1)
    try:
        bounty = pickle.loads(bounty)
    except:
        return False
    first = verify(bounty)
    safeprint("Internal verify")
    second = bounty.isValid()
    if not second:
        rval = -3
    elif not first:
        rval = -2
    elif bounty in getBountyList():
        rval = -1
    elif second == -1:
        rval = 0
    else:
        rval = 1
    if rval == 1:
        addValidBounty(bounty)
    return rval


def addValidBounty(bounty):
    """This adds a bounty to the list under the assumption that it's already been validated. Must be of type common.bounty.Bounty"""
    with bountyLock:
        global bountyList
        bountyList.append(bounty)
        temp = list(set(bountyList))  # trim it in the simplest way possible. Doesn't protect against malleability
        del bountyList[:]
        bountyList.extend(temp)


def internalVerify(bounty): #pragma: no cover
    """Proxy for the Bounty.isValid() method, for use with multiprocessing.Pool"""
    return bounty.isValid()


def addBounties(bounties):
    """Add a list of bounties in parallel using multiprocessing.Pool for verification"""
    from multiprocessing.pool import ThreadPool
    pool = ThreadPool()
    safeprint("Mapping verifications", verbosity=3)
    async = pool.map_async(verify, bounties)  # defer this for possible efficiency boost
    internal = pool.map(internalVerify, bounties)
    safeprint("Waiting for verifications", verbosity=3)
    external = async.get()
    safeprint("Received verifications", verbosity=3)
    rvals = []
    safeprint(internal)
    safeprint(external)
    for i in range(len(bounties)):
        safeprint("Finishing the processing of bounty " + str(i+1) + "/" + str(len(bounties)), verbosity=2)
        if not internal[i]:
            rvals.append(-3)
        elif not external[i]:
            rvals.append(-2)
        elif bounties[i] in bountyList:
            rvals.append(-1)
        elif internal[i] == -1:
            rvals.append(0)
        else:
            rvals.append(1)
        safeprint("Passed first if", verbosity=3)
        if rvals[i] == 1:
            addValidBounty(bounties[i])
    safeprint("Verifications parsed", verbosity=3)
    return rvals


def getBounty(charity, factor):
    """Retrieve the next best bounty from the list"""
    temp = getBountyList()
    safeprint("bountyList = " + str(temp), verbosity=3)
    if temp == []:
        return None
    elif charity:
        for bounty in temp:
            if bounty.isValid():
                index = temp.index(bounty)
                return temp.pop(index)
    else:
        best = None
        for bounty in temp:
            if best is None:
                best = bounty
            elif best < bounty and bounty.isValid() and bounty.isPayable(factor):
                best = bounty
        return best
