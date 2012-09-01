from imgWorker import startWorkers
import zmq
from zmqUtils import recvAll, sendAll
import signal

interrupted = False
def signal_handler(signum, frame):
    global interrupted
    print "INTERRUPTED"
    interrupted = True

signal.signal(signal.SIGINT, signal_handler)

def processRequests():
    global interrupted
    from copy import copy
    ctx = zmq.Context()
    
  
    frontend = ctx.socket(zmq.ROUTER)
    frontend.bind("tcp://*:6767")
    
    backend = ctx.socket(zmq.DEALER)
    backend.bind("tcp://*:6768")
    
    workerCnt = 0
    # Notice these workers connect before hand
    
    poller = zmq.Poller()
    poller.register(frontend, zmq.POLLIN)
    poller.register(backend, zmq.POLLIN)
    
    while True:
        # Receive something from the frontend (requests)
        # or the backend (completed work)
        
        socks = dict(poller.poll(timeout = 1000))
        
        if frontend in socks:
            allParts = recvAll(frontend)      
            # Send something to a worker
            sendAll(backend, allParts)
        elif backend in socks:
            
            # Get result of work from a worker
            allParts = recvAll(backend)
            
            # Give more work to the workers from the URLs we got back if any
            #subParts = allParts[-1].split(";")
            #for url in subParts[1:]:
            #    newWork = copy(allParts)
            #    newWork[-1] = url
            #    sendAll(backend, newWork)
            #allParts[-1] = subParts[0]
            
            # Receive parts back
            sendAll(frontend, allParts)
            
        if interrupted:
            return


if __name__ == "__main__":
    processRequests()