from PySide.QtCore import *
import zmq

class ImgRequester(QThread):
    
    moreImgs = Signal(object)
    
    def __init__(self, startUrl):
        super(ImgRequester, self).__init__()
        self.ctx = zmq.Context()
        self.sock = self.ctx.socket(zmq.REQ)
        self.sock.connect("tcp://localhost:6767")
        self.currUrl = startUrl
        self.foundUrls = set()
        self.visitedUrls = set()


    def requestImgs(self): 
        while True:
            print "SENDING..."
            self.sock.send(self.currUrl)
            print "RECEIVING..."
            imgsAndUrls = self.sock.recv()     
            
            asList = imgsAndUrls.split("!-!")
            imgs = asList[0]
            
            self.moreImgs.emit( (self.currUrl, imgs) )
            
            #This is Depth first search afterall...
            self.foundUrls |= (set(asList[1:]) - self.visitedUrls)
            for url in self.foundUrls:
                if len(url) > 0:
                    print "Potential Url %s" % url
                    if url not in self.visitedUrls:
                        self.currUrl = url
                        self.foundUrls.remove(self.currUrl)
                        self.visitedUrls.add(self.currUrl)
                        break
            if self.currUrl == "":
                return
                
            print "Next get %s " % self.currUrl
        
        
def createImgRequestWorker(requester):
    imgWorker = QThread()
    
    pullTimer = QTimer()
    pullTimer.setSingleShot(True)
    pullTimer.timeout.connect(requester.requestImgs)
    pullTimer.start(1000)
    
    requester.moveToThread(imgWorker)
    pullTimer.moveToThread(imgWorker)
    
    imgWorker.requester = requester
    imgWorker.pullTimer = pullTimer
    
    imgWorker.start()
    return imgWorker
    
        