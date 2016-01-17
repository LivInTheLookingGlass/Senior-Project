import multiprocessing, os, pickle
from common import settings

nextPort = multiprocessing.Value('i', 44566)
if settings.config.get('port'):
  nextPort.value = settings.config.get('port')


def port():
    ret = nextPort.value
    nextPort.value = (nextPort.value - 44566) % 55434 + 44566
    return ret


isMine(string):
    bounty = pickle.loads(string)
    try:
        myCopy = pickle.load(open("bounty-" + str(bounty.ident) + os.sep + "bounty.pickle", "rb"))
        return myCopy == bounty and hash(myCopy) == hash(bounty)
    except:
        return False
