import sys
import live_vid
import const
from PyQt5 import QtGui, QtWidgets

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
        exitAction = self.menu.addAction("Exit    ")
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

            # Toggle webcam
            if self.cameraState == const.CAMERA_INACTIVE:
                const.disableCamera = True
                self.showMessage(const.TEAM_NAME,
                                 const.TOGGLE_MESSAGE[self.cameraState],
                                 QtWidgets.QSystemTrayIcon.Information,
                                 const.TOGGLE_MESSAGE_TIME)
            else:
                const.disableCamera = False
                self.showMessage(const.TEAM_NAME,
                                 const.TOGGLE_MESSAGE[self.cameraState],
                                 QtWidgets.QSystemTrayIcon.Information,
                                 const.TOGGLE_MESSAGE_TIME)
                live_vid.main()



    """
    fireAlertMessage()
    [desc]  Fire the default lazy eye alert message.

    [time] Millisecs of the alert bubble.
    """
    def fireAlertMessage(self, msg, time):
        if self.supportsMessages():
            self.showMessage(const.ALERT_TITLE,
                             const.ALERT_MESSAGE[msg],
                             QtWidgets.QSystemTrayIcon.Information,
                             time)


#######################
# Main Function
#######################
def main():
    app = QtWidgets.QApplication(sys.argv)
    icon = QtGui.QIcon(QtGui.QPixmap(const.TRAY_ICON[const.CAMERA_ACTIVE]))
    trayIcon = SystemTrayIcon(icon)
    const.systemTrayIcon = trayIcon
    trayIcon.activated.connect(trayIcon.toggle)
    trayIcon.show()
    live_vid.main()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
