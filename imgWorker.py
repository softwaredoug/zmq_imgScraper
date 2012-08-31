import zmq
import zmqUtils
import thread
import htmlPuller


def __imgWorker(ctx, workerCnt):
    """ I'm going to scrape some img tags from the URL I'm given"""
    # context is the only thing thats threadsafe!!
    sock = ctx.socket(zmq.REP)
    sock.connect("inproc://imgwork")
    
    print "Worker started.."
    
    while True:
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
        
def startWorkers(ctx, workerCnt):
    # Make 3 workers
    thread.start_new_thread(__imgWorker, (ctx, workerCnt))
    workerCnt += 1
    thread.start_new_thread(__imgWorker, (ctx, workerCnt))
    workerCnt += 1
    thread.start_new_thread(__imgWorker, (ctx, workerCnt))
    workerCnt += 1