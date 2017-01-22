import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QtWidgets.QMenu(parent)
        exitAction = self.menu.addAction("Exit")
        self.setContextMenu(self.menu)

def main():
    app = QtWidgets.QApplication(sys.argv)
    style = app.style()
    icon = QtGui.QIcon(QtGui.QPixmap("images/logo_tray.png"))
    trayIcon = SystemTrayIcon(icon)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()