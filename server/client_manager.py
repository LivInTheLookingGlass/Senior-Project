import multiprocessing, os, pickle
from common import settings

nextPort = multiprocessing.Value('i', 44566)
if settings.config.get('port'):
    nextPort.value = settings.config.get('port')


def port():
    ret = nextPort.value
    nextPort.value = (nextPort.value - 44566) % 55434 + 44566
    return ret


def isMine(string):
    bounty = pickle.loads(string)
    try:
        import os
        path = "bounty-" + str(bounty.ident) + os.sep + "bounty.pickle"
        myCopy = pickle.load(open(path, "rb"))
        return myCopy == bounty and hash(myCopy) == hash(bounty)
    except:
        return False


def handleRequest(sig, conn):
    from common.peers import transact_bounty, start_recipricator, propQueue
    if sig == transact_bounty:
        if isMine(recv(conn)):
            p = port()
            propQueue.put((start_recipricator, p))
            key = send(p, conn, key)


def recipricate(port, live):
    """A method to interact with working clients
    Currently no coin control implemented"""
    import os, pickle, socket
    from common.peers import fetch_test, fetch_main, test_results, main_results, valid_signal, invalid_signal
    ear = socket.socket()
    ear.bind(("0.0.0.0", port))
    ear.listen(1)
    conn, addr = ear.accept()
    key = None
    sig = recv(conn)
    string = recv(conn)
    bounty = pickle.loads(string)
    path = "bounty-" + str(bounty.id) + os.sep
    if isMine(string):
        key = send(open(path + "test.jar").read(), conn, key)
        for expected in open(path + "test.expected.flags").readlines():
            if recv(conn) != expected:
                send(invalid_signal, conn, key)
                conn.close()
                return False
            else:
                send(valid_signal, conn, key)
        send(valid_signal, conn, key)
        send(open(path + "main.jar").read(), conn, key)
        for expected in open(path + "main.expected.flags").readlines():
            if recv(conn) != expected:
                send(invalid_signal, conn, key)
                conn.close()
                return False
            else:
                send(valid_signal, conn, key)
        send(valid_signal, conn, key)
        conn.close()
        return True
    conn.close()
    return False


class recipricator(multiprocessing.Process):
    """A class to deal with working clients"""
    def __init__(self, port, live):
        multiprocessing.Process.__init__(self)
        self.port = port
        self.live = live

    def run(self):
        safeprint("recipricator started")
        recipricate(self.port, self.live)
        safeprint("recipricator stopped")
