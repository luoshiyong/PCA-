# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\pythoncode\PCAface\pca.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from PIL import Image, ImageQt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from compute import PCA
import os
import numpy as pd 
import sys
train_path = 'D:/pythoncode/PCAface/TrainDatabase/'
test_path = 'D:/pythoncode/PCAface/TestDatabase/'
filename1 = os.listdir(train_path)
filename1.remove('Thumbs.db')
filename1.sort(key= lambda x:int(x[:-4]))
filename2 = os.listdir(test_path)
filename2.remove('Thumbs.db')
filename2.sort(key= lambda x:int(x[:-4]))
class Ui_MainWindow(QtWidgets.QMainWindow):
    pca = PCA()
    img_path = ''
    def __init__(self):
        super(Ui_MainWindow,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
    def setupUi(self,MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1083, 630)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(50, 90, 929, 405))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(27)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(43)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView = QtWidgets.QGraphicsView(self.widget)
        self.graphicsView.setMinimumSize(QtCore.QSize(441, 311))
        self.graphicsView.setMaximumSize(QtCore.QSize(441, 311))
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.widget)
        self.graphicsView_2.setMinimumSize(QtCore.QSize(441, 311))
        self.graphicsView_2.setMaximumSize(QtCore.QSize(441, 311))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.horizontalLayout.addWidget(self.graphicsView_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(250)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setMinimumSize(QtCore.QSize(201, 61))
        self.pushButton.setMaximumSize(QtCore.QSize(201, 61))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(201, 61))
        self.pushButton_2.setMaximumSize(QtCore.QSize(201, 61))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1083, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.onClick1_Button)
        self.pushButton_2.clicked.connect(self.onClick2_Button)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "打开图片"))
        self.pushButton_2.setText(_translate("MainWindow", "识别"))
    def onClick1_Button(self):
        imagePath = QFileDialog.getOpenFileName(self,'选择文件')
        print(imagePath)
        for i in imagePath:
            print("11111",i)
        self.img_path = imagePath[0]
        image = QImage(imagePath[0])
        scene = QGraphicsScene()
        scene.addPixmap(QPixmap.fromImage(image))
        self.graphicsView.setScene(scene)
        self.graphicsView.resize(image.width() + 10, image.height() + 10)
        self.graphicsView.show()
    
    def onClick2_Button(self):
        Matrix = self.pca.CreateDataset(train_path,20)
        eigfaces = self.pca.eigenfaceCore(Matrix)
        index = self.pca.recognize(self.img_path,Matrix,eigfaces)
        print("index = ",index)
        res = train_path+str(index)+'.jpg'
        print(res)
        image = QImage(res)
        scene = QGraphicsScene()
        scene.addPixmap(QPixmap.fromImage(image))
        self.graphicsView_2.setScene(scene)
        self.graphicsView_2.resize(image.width() + 10, image.height() + 10)
        self.graphicsView_2.show()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Ui_MainWindow()
    #w.setWindowTitle("人脸识别")
    w.show()
    sys.exit(app.exec_())