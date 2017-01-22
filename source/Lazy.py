import sys
import find_face
from PyQt5 import QtCore, QtGui, QtWidgets

# Tray Constants
TRAY_ICON = [
    "images/logo_tray_inactive.png",
    "images/logo_tray_active.png"
]
TRAY_TOOLTIP = [
    "Who's Lazy? Not Eye! (Inactive - Press to activate)",
    "Who's Lazy? Not Eye! (Active - Press to disable)"
]

# Camera Flags
CAMERA_INACTIVE = 0
CAMERA_ACTIVE = 1

# Globals
cameraState = CAMERA_ACTIVE

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QtWidgets.QMenu(parent)
        exitAction = self.menu.addAction("Exit")
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(sys.exit)
        self.setContextMenu(self.menu)
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    style = app.style()
    icon = QtGui.QIcon(QtGui.QPixmap(TRAY_ICON[CAMERA_ACTIVE]))
    trayIcon = SystemTrayIcon(icon)
    trayIcon.setToolTip(TRAY_TOOLTIP[CAMERA_ACTIVE])
    trayIcon.show()
    find_face.main()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
