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
        self.text_label = QtWidgets.QLabel(self.centralwidget)
        self.text_label.setGeometry(QtCore.QRect(10, 150, 251, 111))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.text_label.setFont(font)
        self.text_label.setAutoFillBackground(False)
        self.text_label.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"color: rgb(200, 200, 200);")
        self.text_label.setTextFormat(QtCore.Qt.AutoText)
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)
        self.text_label.setWordWrap(True)
        self.text_label.setObjectName("text_label")
        self.bg_color = QtWidgets.QWidget(self.centralwidget)
        self.bg_color.setGeometry(QtCore.QRect(0, -1, 271, 421))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.bg_color.sizePolicy().hasHeightForWidth())
        self.bg_color.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.bg_color.setFont(font)
        self.bg_color.setAutoFillBackground(False)
        self.bg_color.setStyleSheet("background-color: rgb(59, 59, 59);")
        self.bg_color.setObjectName("bg_color")
        self.logo_frame = QtWidgets.QFrame(self.bg_color)
        self.logo_frame.setGeometry(QtCore.QRect(60, 20, 151, 141))
        self.logo_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.logo_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.logo_frame.setObjectName("logo_frame")
        self.on_off_button = QtWidgets.QPushButton(self.bg_color)
        self.on_off_button.setGeometry(QtCore.QRect(90, 350, 81, 32))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.on_off_button.sizePolicy().hasHeightForWidth())
        self.on_off_button.setSizePolicy(sizePolicy)
        self.on_off_button.setBaseSize(QtCore.QSize(100, 100))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.on_off_button.setFont(font)
        self.on_off_button.setStyleSheet("background-color: rgb(60, 205, 235);")
        self.on_off_button.setAutoDefault(False)
        self.on_off_button.setDefault(False)
        self.on_off_button.setFlat(False)
        self.on_off_button.setObjectName("on_off_button")
        self.bg_color.raise_()
        self.text_label.raise_()
        LazyEye.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(LazyEye)
        self.statusbar.setObjectName("statusbar")
        LazyEye.setStatusBar(self.statusbar)

        self.retranslateUi(LazyEye)
        self.on_off_button.pressed.connect(self.on_off_button.hide)
        QtCore.QMetaObject.connectSlotsByName(LazyEye)

    def retranslateUi(self, LazyEye):
        _translate = QtCore.QCoreApplication.translate
        LazyEye.setWindowTitle(_translate("LazyEye", "Lazy Eye"))
        self.text_label.setText(_translate("LazyEye", "Leave this program running while watching videos to train your lazy eye ;)"))
        self.on_off_button.setText(_translate("LazyEye", "On"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LazyEye = QtWidgets.QMainWindow()
    ui = Ui_LazyEye()
    ui.setupUi(LazyEye)
    LazyEye.show()
    sys.exit(app.exec_())

