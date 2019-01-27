import os
import re
import cv2
from datetime import datetime  
from datetime import timedelta 
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QMessageBox, QFileDialog, QGraphicsScene
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer, QRectF, QDateTime
from jpg2videoClass import jpg2video
from ui_snapshot import Ui_MainWindow

class MyWindow(Ui_MainWindow,QWidget):      # Inheritage from QWidget is important for pyqtSignal
    def myModifications(self):
        self.pushButton_previous.clicked.connect(self.onPrevious)
        self.pushButton_next.clicked.connect(self.onNext)
        self.pushButton_minus.clicked.connect(self.onMinus)
        self.pushButton_plus.clicked.connect(self.onPlus)
        self.pushButton_Video.clicked.connect(self.onVideo)
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime()) 
        self.dateTimeEdit.dateTimeChanged.connect(self.ondateTimeEdit)
        self.num = 0
        self.numMax = len(allFiles)
        print("Number of files:", self.numMax)

    def onPrevious(self):
        self.num -= 1
        if self.num < 0:
            self.num=0
        self.showPic(self.num)

    def onNext(self):
        self.num += 1
        if self.num > self.numMax-1:
            self.num=self.numMax-1
        self.showPic(self.num)

    def onMinus(self):
        self.num -= 8
        if self.num < 0:
            self.num=0
        self.showPic(self.num)

    def onPlus(self):
        self.num += 8
        if self.num > self.numMax-1:
            self.num=self.numMax-1
        self.showPic(self.num)

    def ondateTimeEdit(self):
        # print('Date and time changed:',self.dateTimeEdit.dateTime())
        selectDate = self.dateTimeEdit.dateTime().toPyDateTime()
        self.num = vi.getFileNumber(allFiles, selectDate)
        print("Select frame number", self.num, " --- ", allFiles[self.num])
        self.showPic(self.num)

    def showPic(self, num):
        self.num = num
        fname = allFiles[self.num]
        node, date, time,_ ,_,=re.split('\_',fname)
        fdate = datetime.strptime(date+time, "%Y-%m-%d%H-%M-%S")
        print(date+" "+time)        # 2019-01-03 00-03-14
        print(QDateTime.fromString(date+" "+time, "yyyy-MM-dd HH-mm-ss").toString())
        self.pixMap = QPixmap(vi.datapath+fname)
        self.Bild.setPixmap(self.pixMap)
        # self.Bild.resize(self.pixMap.width(),self.pixMap.height())
        self.dateTimeEdit.setDateTime(QDateTime.fromString(date+" "+time, "yyyy-MM-dd HH-mm-ss"))

    def onVideo(self):
        pass


class snapshot(jpg2video):
    pass

#############################################################################################
if __name__ == '__main__':
    vi = snapshot(datapath="D:\\Data\\Python\\DomeCam_GUI\\testdata\\")
    date = datetime.now()

    allFiles, n = vi.getFileList()
    print("Number of all saved frames:", n)
    print("First frame:", str(vi.getFirstDate(allFiles)))

    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyWindow()
    ui.setupUi(MainWindow)
    ui.myModifications()
    MainWindow.show()
    sys.exit(app.exec_())
