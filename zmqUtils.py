import zmq

def recvAll(sock):
    """ Receive all parts of the envelope"""
    parts = [sock.recv()]
    while sock.getsockopt(zmq.RCVMORE):
        parts.append(sock.recv())
    return parts

def sendAll(sock, parts):
    """ send all parts passed in"""
    if parts:
        for part in parts[:-1]:
            sock.send(part, zmq.SNDMORE)
        sock.send(parts[-1])
        
def timeoutRcvAll(sock,timeoutMsec):
    """ Timeout on work"""
    poller = zmq.Poller()
    poller.register(sock, zmq.POLLIN)
    socks = dict(poller.poll(timeout=timeoutMsec))
    if sock in socks:
        if socks[sock] == zmq.POLLIN:
            return sock.recv()
    else:
        raise TimeoutError