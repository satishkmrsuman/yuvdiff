from PIL import Image
import numpy as np
import cv2
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QFileDialog,QInputDialog,QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap,QImage
from PyQt5.QtCore import Qt
import time

remainingframe=0
def PIL2array(img,channel):
    return np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], channel)


#This function will overlay a grid on the input image
def overlayGrid(img,width,height,blocksize):
    halfblock=int(blocksize/2)
    numberof64pixelrow=int(width/blocksize)
    numberof64pixelcol=int(height/blocksize)
    numberof32pixelrow=int(width/halfblock)
    numberof32pixelcol=int(height/halfblock)
    for i in range(height):
        for j in range(0,(width),blocksize):
            img[:,:,1][i][j+1]=0
            img[:,:,2][i][j+1]=0
    
    for i in range(0,height,blocksize):
        for j in range(width):
            img[:,:,1][i+1][j]=0
            img[:,:,2][i+1][j]=0

    for i in range(height):
        for j in range(0,(width),halfblock):
            img[:,:,1][i][j]=0
            img[:,:,2][i][j]=0
    
    for i in range(0,height,halfblock):
        for j in range(width):
            img[:,:,1][i][j]=0
            img[:,:,2][i][j]=0
    return img

def readImageBytesFromFile(fileName,readsize,offset):
    try:
        #process refrence image
        with open(fileName,"rb") as inptr:
            inptr.seek(offset)        
            imgbytes = inptr.read(readsize)
            return imgbytes
    except:
        print("Unable to read bytes")
        return 0

#import PyQt5
def createImageFromByte(inbytes,width,height):
    img=np.zeros(shape=(height,width,3),dtype='uint8')
    PILimg=Image.frombytes("P",(width,height),inbytes,decoder_name='raw')
    cvimg=PIL2array(PILimg,1)
    img[:,:,0]=cvimg[:,:,0]
    img[:,:,1]=cvimg[:,:,0]
    img[:,:,2]=cvimg[:,:,0]
    return img

def cvmat2Qimg(frame):
    image = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
    return QPixmap(image)
 
class App(QWidget):
    def getint(self):
        width,okwidth = QInputDialog.getInt(self,"INT ONLY","Enter width")
        height,okheight = QInputDialog.getInt(self,"INT ONLY","Enter Height")
        frames,okframes = QInputDialog.getInt(self,"INT ONLY","Enter Frames")
    
        if okwidth and okheight and okframes:
            return width,height,frames
        else:
            sys.exit()

    def __init__(self):
        super().__init__()
        self.title="yuvDiff"
        self.left=10
        self.top=10
        self.width,self.height,self.frames = self.getint()
        self.initUI()
        
    
    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.label = QLabel(self)
        layout.addWidget(self.label)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def showimage(self,nextprev):
        global remainingframe
        framenumber=remainingframe+nextprev
        #check if we are underflowing
        if (framenumber)<0:
            return
        
        #check if we are overflowing
        if (framenumber)>self.frames:
            return

        remainingframe=remainingframe+nextprev

        refbytes=readImageBytesFromFile(self.reffile,(self.width*self.height),(self.width*self.height)*framenumber)
        img=createImageFromByte(refbytes,self.width,self.height)
        overlayedimg=overlayGrid(img,self.width,self.height,64)
        pixmap = cvmat2Qimg(overlayedimg)
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.reffile, _ = QFileDialog.getOpenFileName(self,"Please select reference yuv", "","All Files (*);;yuv files (*.yuv)", options=options)
        self.modfile, _ = QFileDialog.getOpenFileName(self,"Please select modified yuv", "","All Files (*);;yuv files (*.yuv)", options=options)
        if self.modfile=="" and self.reffile=="":
            return ""

    def keyPressEvent(self, event):
        key=event.key()
        if key==Qt.Key_N:
            #self.imagenumber=self.imagenumber+1
            self.showimage(1)
            # self.show()
        elif key==Qt.Key_P:
            self.showimage(-1)
        else:
            pass

 

if __name__ == '__main__':
    blocksize=64
    global framenumber
    app = QApplication(sys.argv)

    #get main windows object
    mainwindow = App()

    #get file name
    iffilepathcorrect=mainwindow.openFileNameDialog()
    if iffilepathcorrect=="":
        sys.exit()
    remainingframe=0
    
    #Read and display the very first frame here rest will be controlled by keyinputs
    refbytes=readImageBytesFromFile(mainwindow.reffile,(mainwindow.width*mainwindow.height),(mainwindow.width*mainwindow.height)*remainingframe)
    img=createImageFromByte(refbytes,mainwindow.width,mainwindow.height)
    overlayedimg=overlayGrid(img,mainwindow.width,mainwindow.height,64)
    pixmap = cvmat2Qimg(overlayedimg)
    mainwindow.label.setPixmap(pixmap)
    mainwindow.resize(pixmap.width(), pixmap.height())

    sys.exit(app.exec_())