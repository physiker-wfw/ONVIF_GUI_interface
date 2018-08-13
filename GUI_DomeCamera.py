import sys
import urllib.request
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QMessageBox, QFileDialog, QGraphicsScene
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer, QRectF
from ui_mainwindow import Ui_MainWindow
sys.path.append("D:/data/Python/")          # needed to import 'pythonOnvifDomecam' if not in the same directory
from pythonOnvifDomecam import MegapixelDomeCamera as cam, config

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

    def onPushButton1(self):
        self.camera.moveToPositionPreset(1)

    def onPushButton2(self):
        self.camera.moveToPositionPreset(2)

    def onPushButton3(self):
        self.camera.moveToPositionPreset(3)

    def onPushButton4(self):
        self.camera.moveToPositionPreset(4)

    def onPushButtonSnapshot(self):
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, 'http://'+config.host, config.user, config.password)
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(handler)
        opener.open(self.camera.getSnapshot())
        urllib.request.install_opener(opener)
        data = urllib.request.urlopen(self.camera.getSnapshot()).read()
        self.pixMap = QPixmap()
        self.pixMap.loadFromData(data)
        self.labelFrame.setPixmap(self.pixMap)

    def onActionFilename(self):    
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        jpgFile, _ = QFileDialog.getSaveFileName(self,"Select file:" , "D:\\Daten\\*.jpg", options=options)
        if jpgFile:
            self.pixMap.save(jpgFile)
    
    def onActionAbout(self):
        print("About ...")
        QMessageBox.about(self, "About",
        """Testing routines to control an IP camera.
        (@MLU-WFW)""")

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