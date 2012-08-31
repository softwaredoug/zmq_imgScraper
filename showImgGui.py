from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
import showImgGuiWorker


class ImgDisplay(QWidget):
    def __init__(self, url):
        super(ImgDisplay, self).__init__()
        
        vLayout = QVBoxLayout(self)
        self.webView = QWebView()
        self.currHtml = "<h1>Images!</h1>"
        self.webView.setHtml(self.currHtml)
        self.pauseWeb = QPushButton(self)
        vLayout.addWidget(self.webView)
        vLayout.addWidget(self.pauseWeb)
        self.setLayout(vLayout)
        
        
        self.pauseWeb.pressed.connect(self.stopDl)
        
        requester = showImgGuiWorker.ImgRequester(url)
        requester.moreImgs.connect(self.updateWithImgs)
        self.worker = showImgGuiWorker.createImgRequestWorker(requester)

    def updateWithImgs(self, urlWithImg):
        url = urlWithImg[0]
        img = urlWithImg[1]
        
        self.currHtml += "<h2>" + url + "</h2>" + img + "<br>"
        
        self.webView.setHtml(self.currHtml)
        
    def stopDl(self):
        #UNSAFE TERMINATION
        self.worker.terminate()
        
        #print "%s got %s" % (url, img)
        
if __name__ == "__main__":
    from sys import argv
    qApp = QApplication(argv)
    dialog = ImgDisplay(argv[1])
    dialog.show()
    qApp.exec_()