import sys
import urllib.request
import cv2
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QMessageBox, QFileDialog, QGraphicsScene
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer, QRectF, QThread, Qt
from ui_mainwindow import Ui_MainWindow
sys.path.append("D:/data/Python/")          # needed to import 'pythonOnvifDomecam' if not in the same directory
from pythonOnvifDomecam import MegapixelDomeCamera as cam, config

class Thread(QThread):
    ''' Thread to capture the individual frames which are then passed as QImage to the interrupt routine. ''' 
    changePixmap = pyqtSignal(QImage)

    def run(self):
        # cap = cv2.VideoCapture(0)                                           # To read built-in web cam
        cap = cv2.VideoCapture('rtsp://192.168.178.99:554/1/h264major')   # To read stream of IP camera
        while True:
            ret, frame = cap.read()
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            myImage = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
            myImage = myImage.scaled(640*2, 480*2, Qt.KeepAspectRatio)
            self.changePixmap.emit(myImage)

class MyWindow(Ui_MainWindow,QWidget):      # Inheritage from QWidget is important for pyqtSignal
    timer = QTimer()

    def myModifications(self):
        self.pushButton1.clicked.connect(self.onPushButton1)
        self.pushButton2.clicked.connect(self.onPushButton2)
        self.pushButton3.clicked.connect(self.onPushButton3)
        self.pushButton4.clicked.connect(self.onPushButton4)
        self.pushButtonSnapshot.clicked.connect(self.onPushButtonSnapshot)
        self.actionSave_as.triggered.connect(self.onActionFilename)
        self.actionAbout.triggered.connect(self.onActionAbout)
        # self.actionHelp.triggered.connect(self.onActionCommands)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)      # Defining interrupt routine for QImage data
        th.start()


    def onPushButton1(self):
        self.camera.moveToPositionPreset(1)

    def onPushButton2(self):
        self.camera.moveToPositionPreset(2)

    def onPushButton3(self):
        self.camera.moveToPositionPreset(3)

    def onPushButton4(self):
        self.camera.moveToPositionPreset(4)

    def onPushButtonSnapshot(self):
        # password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        # password_mgr.add_password(None, 'http://'+config.host, config.user, config.password)
        # handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        # opener = urllib.request.build_opener(handler)
        # opener.open(self.camera.getSnapshot())
        # urllib.request.install_opener(opener)
        # data = urllib.request.urlopen(self.camera.getSnapshot()).read()
        # self.pixMap = QPixmap()
        # self.pixMap.loadFromData(data)
        # self.labelFrame.setPixmap(self.pixMap)
        self.snapshot = self.pixMap

    def onActionFilename(self):    
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        jpgFile, _ = QFileDialog.getSaveFileName(self,"Select file:" , "D:\\Daten\\*.jpg", options=options)
        if jpgFile:
            self.snapshot.save(jpgFile)
    
    def onActionAbout(self):
        print("About ...")
        QMessageBox.about(self, "About",
        """Testing routines to control an IP camera.
        (@MLU-WFW)""")

    @pyqtSlot(QImage)
    def setImage(self, image):
        ''' Interrupt routine to accept QImage data and to push them to a label.'''
        self.pixMap = QPixmap.fromImage(image)
        self.labelFrame.setPixmap(self.pixMap)


    def setupCam(self):
        self.camera = cam.MegapixelDomeCamera(config.host, config.port, config.user, config.password)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyWindow()
    ui.setupUi(MainWindow)
    ui.setupCam()
    ui.myModifications()
    MainWindow.show()
    sys.exit(app.exec_())