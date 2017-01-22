# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Lazy.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LazyEye(object):
    def setupUi(self, LazyEye):
        LazyEye.setObjectName("LazyEye")
        LazyEye.setEnabled(True)
        LazyEye.resize(270, 438)
        LazyEye.setMinimumSize(QtCore.QSize(270, 438))
        LazyEye.setMaximumSize(QtCore.QSize(270, 438))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(15)
        LazyEye.setFont(font)
        LazyEye.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(LazyEye)
        self.centralwidget.setObjectName("centralwidget")
        self.off_button = QtWidgets.QPushButton(self.centralwidget)
        self.off_button.setGeometry(QtCore.QRect(78, 200, 113, 32))
        self.off_button.setAutoDefault(False)
        self.off_button.setDefault(False)
        self.off_button.setFlat(False)
        self.off_button.setObjectName("off_button")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 30, 141, 71))
        self.label.setAutoFillBackground(True)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.on_button = QtWidgets.QPushButton(self.centralwidget)
        self.on_button.setGeometry(QtCore.QRect(80, 140, 113, 32))
        self.on_button.setAutoDefault(False)
        self.on_button.setDefault(False)
        self.on_button.setFlat(False)
        self.on_button.setObjectName("on_button")
        LazyEye.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LazyEye)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 270, 22))
        self.menubar.setObjectName("menubar")
        self.menuLazy_Eye = QtWidgets.QMenu(self.menubar)
        self.menuLazy_Eye.setObjectName("menuLazy_Eye")
        LazyEye.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LazyEye)
        self.statusbar.setObjectName("statusbar")
        LazyEye.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuLazy_Eye.menuAction())

        self.retranslateUi(LazyEye)
        self.off_button.pressed.connect(self.on_button.show)
        self.off_button.pressed.connect(self.off_button.hide)
        self.on_button.pressed.connect(self.pressOnButton)
        QtCore.QMetaObject.connectSlotsByName(LazyEye)

    def retranslateUi(self, LazyEye):
        _translate = QtCore.QCoreApplication.translate
        LazyEye.setWindowTitle(_translate("LazyEye", "Lazy Eye"))
        self.off_button.setText(_translate("LazyEye", "Off"))
        self.label.setText(_translate("LazyEye", "Lazy Eye Software Description"))
        self.on_button.setText(_translate("LazyEye", "On"))
        self.menuLazy_Eye.setTitle(_translate("LazyEye", "Lazy Eye"))

    def pressOnButton():
        if self.on_button.text == "On":
            self.on_button.setText(_translate("LazyEye", "Off"))
        else:
            self.on_button.setText(_translate("LazyEye","On"))
