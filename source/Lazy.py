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
        self.quit_button = QtWidgets.QPushButton(self.centralwidget)
        self.quit_button.setGeometry(QtCore.QRect(78, 200, 113, 32))
        self.quit_button.setAutoDefault(False)
        self.quit_button.setDefault(False)
        self.quit_button.setFlat(False)
        self.quit_button.setObjectName("quit_button")
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
        self.quit_button.pressed.connect(self.exit)
        self.quit_button.pressed.connect(self.quit_button.hide)
        self.on_button.pressed.connect(self.pressOnButton)
        QtCore.QMetaObject.connectSlotsByName(LazyEye)

    def retranslateUi(self, LazyEye):
        _translate = QtCore.QCoreApplication.translate
        LazyEye.setWindowTitle(_translate("LazyEye", "Lazy Eye"))
        self.quit_button.setText(_translate("LazyEye", "Quit"))
        self.label.setText(_translate("LazyEye", "Lazy Eye Software Description"))
        self.on_button.setText(_translate("LazyEye", "On"))
        self.menuLazy_Eye.setTitle(_translate("LazyEye", "Lazy Eye"))

    def pressOnButton(self):
        if self.on_button.text() == "On":
            self.on_button.setText("Off")
        else:
            self.on_button.setText("On")

    def exit(self):
        import sys
        sys.exit()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LazyEye = QtWidgets.QMainWindow()
    ui = Ui_LazyEye()
    ui.setupUi(LazyEye)
    LazyEye.show()
    sys.exit(app.exec_())




