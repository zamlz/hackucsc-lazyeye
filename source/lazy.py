import sys
import find_face
import const
from PyQt5 import QtCore, QtGui, QtWidgets


#######################
# SystemTrayIcon Class
#######################
class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    """
    SystemTrayIcon Constructor
    [desc]  Constructor for the SystemTrayIcon class

    [icon] Icon for the system tray.
    [parent] Parent for the system tray.
    """
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)

        self.cameraState = const.CAMERA_ACTIVE
        self.setToolTip(const.TRAY_TOOLTIP[const.CAMERA_ACTIVE])

        self.menu = QtWidgets.QMenu(parent)
        exitAction = self.menu.addAction("Exit")
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(sys.exit)
        self.setContextMenu(self.menu)


    """
    toggle()
    [desc]  Toggle the system tray icon to do the current
            primary task assigned (toggle lazy eye guard).

    [reason] Toggle event flag.
    """
    def toggle(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            # Toggle camera state and switch icon and tooltip
            self.cameraState = (self.cameraState + 1) % 2
            self.setToolTip(const.TRAY_TOOLTIP[self.cameraState])
            icon = QtGui.QIcon(QtGui.QPixmap(const.TRAY_ICON[self.cameraState]))
            self.setIcon(icon)


#######################
# Main Function
#######################
def main():
    app = QtWidgets.QApplication(sys.argv)
    style = app.style()
    icon = QtGui.QIcon(QtGui.QPixmap(const.TRAY_ICON[const.CAMERA_ACTIVE]))
    trayIcon = SystemTrayIcon(icon)
    trayIcon.activated.connect(trayIcon.toggle)
    trayIcon.show()
    find_face.main()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
