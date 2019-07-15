#!/usr/bin/env python3
import sys
import time
import urllib.request
import cv2
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from collections import deque
sys.path.append("D:/data/Python/")          # needed to import 'pythonOnvifDomecam' if not in the same directory
from pythonOnvifDomecam import MegapixelDomeCamera as cam, config

class Thread(QtCore.QThread):
    ''' Thread(QtCore.QThread): Thread to capture the individual frames which are then passed as QtGui.QImage to the interrupt routine. 
    If record flag (self.record) is True, video will be recorded to file self.out''' 
    def __init__(self):
        super().__init__()
        # self.cap = cv2.VideoCapture(0)                    # To read built-in web cam
        self.cap = cv2.VideoCapture('rtsp://'+config.host+':'+str(config.rtsp_port)+config.rtsp_url)   # To read stream of IP camera
        fac = 0.5      # reduce image resolution for video file
        self.size = (int(self.cap.get(3)*fac), int(self.cap.get(4)*fac))

        # store the last maxlen frames in self.que
        self.que = deque(maxlen=100)

    changePixmap = QtCore.pyqtSignal(QtGui.QImage)

    def run(self):
        while (self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret:
                resized = cv2.resize(frame, self.size, interpolation = cv2.INTER_AREA)
                self.que.append(resized)
                rgbImage = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
                if self.record:
                    # write the video frame to file
                    self.out.write(resized)
                myImage = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QtGui.QImage.Format_RGB888)
                myImage = myImage.scaled(640*2, 480*2, QtCore.Qt.KeepAspectRatio)
                self.changePixmap.emit(myImage)
                self.countDown -= 1
                if self.countDown == 0:
                    self.writeVideoBuffer()

    def writeVideoBuffer(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        file = 'snap_'+time.strftime("%Y%m%d_%H%M%S")+'.avi'
        outSnap = cv2.VideoWriter(file,fourcc, 25.0, self.size)
        for i in range(min(100,len(self.que))):
            outSnap.write(self.que.popleft())
        outSnap.release()

class xxWindow(QtWidgets.QMainWindow, QtWidgets.QWidget):
    """ fill in some initial data """
    timer = QtCore.QTimer()
    def __init__(self):
        super(xxWindow, self).__init__()
        self.ui = self.ui = uic.loadUi("GUI_DomeCamera3.ui", self)

        # Setup the DomeCamera
        self.camera = cam.MegapixelDomeCamera(config.host, config.port, config.user, config.password)

        # label and specify buttons with their actions
        self.pushButton1.clicked.connect(self.onPushButton1)
        self.pushButton2.clicked.connect(self.onPushButton2)
        self.pushButton3.clicked.connect(self.onPushButton3)
        self.pushButton4.clicked.connect(self.onPushButton4)
        self.pushButton5.clicked.connect(self.onPushButtonReithalle)
        self.pushButton6.clicked.connect(self.onPushButtonParken1)
        self.pushButton7.clicked.connect(self.onPushButtonParken2)
        self.pushButtonU4.clicked.connect(self.onU4)
        self.pushButtonU3.clicked.connect(self.onTest)
        self.pushButtonU3.setText('Test')
        self.pushButtonU2.clicked.connect(self.onRecord)
        self.pushButtonU3.setText('Record')
        self.pushButtonU1.clicked.connect(self.onPushButtonSnapshot)
        self.pushButtonU3.setText('XXX')
        self.actionSave_as.triggered.connect(self.onActionFilename)
        self.actionAbout.triggered.connect(self.onActionAbout)
        self.tiltSlider.setRange(-20,20)
        self.tiltSlider.valueChanged.connect(self.onSliderValueChanged) 
        self.tiltSlider.sliderReleased.connect(self.onSliderReleased)       
        
        self.actionHelp.triggered.connect(self.onActionHelp)

        self.snapshot = QtGui.QPixmap()

        # Handling of video routine with the thread
        self.th = Thread()
        self.th.record = False
        self.th.countDown = -1      # If countDown is zero, the video buffer is written to file.
        self.th.changePixmap.connect(self.setImage)      # Defining interrupt routine for QtGui.QImage data
        self.th.start()

        # Mouse event over video
        self.labelFrame.mousePressEvent = self.onMousePressed
        self.labelFrame.mouseReleaseEvent = self.onMouseReleased


    def onPushButton1(self):
        self.camera.moveToPositionPreset(1)

    def onPushButton2(self):
        self.camera.moveToPositionPreset(2)

    def onPushButton3(self):
        self.camera.moveToPositionPreset(3)

    def onPushButton4(self):
        self.camera.moveToPositionPreset(4)

    def onPushButtonReithalle(self):
        self.camera.moveToPositionPreset(5)
        
    def onPushButtonParken1(self):
        self.camera.moveToPositionPreset(6)
        
    def onPushButtonParken2(self):
        self.camera.moveToPositionPreset(7)
        
    def onPushButtonSnapshot(self):
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, 'http://'+config.host, config.user, config.password)
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(handler)
        opener.open(self.camera.getSnapshot())
        urllib.request.install_opener(opener)
        data = urllib.request.urlopen(self.camera.getSnapshot()).read()
        self.snapshot.loadFromData(data)
        self.onActionFilename()

    def onU4(self):
        self.camera.relativeMove(pan=1, duration=1.0)

    def onActionFilename(self):    
        options = QtWidgets.QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        # jpgFile, _ = QFileDialog.getSaveFileName(self,"Select file:" , "D:\\Daten\\*.jpg", options=options)
        jpgFile = 'pic_'+time.strftime("%Y%m%d_%H%M%S")+'.jpg'
        if jpgFile:
            self.snapshot.save(jpgFile)
    
    def onActionAbout(self):
        print("About ...")
        QtWidgets.QMessageBox.about(self, "About",
        """This is the help file. \n
        (@MLU-WFW)""")

    def onActionHelp(self):
        print("Help ...")
        QtWidgets.QMessageBox.about(self, "Help",
        """Testing routines to control an IP camera.
        (@MLU-WFW)""")

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        '''Plots the QtGui.QImage argument on the label 'labelFrame'. 
        Interrupt routine to accept QtGui.QImage data and to push them to a label.'''
        self.pixMap = QtGui.QPixmap.fromImage(image)
        self.labelFrame.setPixmap(self.pixMap)

    def onMousePressed(self, event):
        self.mousePressed = [event.pos().x(),event.pos().y()]

    def onMouseReleased(self, event):
        x = event.pos().x()
        y = event.pos().y()
        self.mouseReleased = [x,y]
        vector = [x-self.mousePressed[0], y-self.mousePressed[1]]
        if vector[0]<0:
            pan = cam.Pan.RIGHT
        else:
            pan = cam.Pan.LEFT
        if vector[1]>0:
            tilt = cam.Tilt.UP
        else:
            tilt = cam.Tilt.DOWN
        self.camera.relativeMove(pan=pan, duration=abs(vector[0])/160.)
        self.camera.relativeMove(tilt=tilt, duration=abs(vector[1])/160.)

    def onRecord(self):
        if not self.th.record:
            self.saveVideoStart()
            self.pushButtonU2.setStyleSheet("background-color:yellow;")
            self.pushButtonU2.setText("Stop")
        else:
            self.saveVideoStopp()
            self.pushButtonU2.setText("Record")
            self.pushButtonU2.setStyleSheet("background-color:white;")

    def saveVideoStart(self):           
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        file = 'vid_'+time.strftime("%Y%m%d_%H%M%S")+'.avi'
        self.th.out = cv2.VideoWriter(file,fourcc, 25.0, self.th.size)
        self.th.record = True

    def saveVideoStopp(self):         
        self.th.record = False
        self.th.out.release()

    def onTest(self):
        self.th.countDown = 50      # Count the next 50 frames. Afterwards the video buffer is written to file.
    
    def onSliderValueChanged(self):
        print('Slider value:',self.tiltSlider.value())

    def onSliderReleased(self):
        print('Slider released:',self.tiltSlider.value())
        if self.tiltSlider.value()>0:
            zoom = cam.Zoom.IN
        else:
            zoom = cam.Zoom.OUT
        self.camera.relativeMove(zoom=zoom, duration=abs(self.tiltSlider.value())/10.)
        self.tiltSlider.setValue(0)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = xxWindow()
    ui.show()
    sys.exit(app.exec_())