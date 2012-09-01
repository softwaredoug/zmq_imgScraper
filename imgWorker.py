import zmq
import zmqUtils
import thread
import htmlPuller

ctx = zmq.Context()


def __imgWorker(ctx, workerCnt):
    """ I'm going to scrape some img tags from the URL I'm given"""
    # context is the only thing thats threadsafe!!
    sock = ctx.socket(zmq.REP)
    sock.connect("tcp://localhost:6768")
    
    print "New Worker started.."
    
    print "Worker receiving"
    allParts = zmqUtils.recvAll(sock)
    clientId = allParts[0]
    url = allParts[-1]
    allParts[-1] += " from worker %i" %  workerCnt
    print "Received %s" % url
    # Grab all the IMGs
    (imgs, links) = htmlPuller.getAllImgTagsAndLinks(url)
    allParts[-1] = imgs + "!-!" + links
    zmqUtils.sendAll(sock, allParts)
    print "WORKER DEAD!!!"
        
        
def startWorkers(ctx, workerCnt):
    # Make 3 workers
    __imgWorker(ctx, workerCnt)
    workerCnt += 1
    
if __name__ == "__main__":
    startWorkers(ctx, 0)