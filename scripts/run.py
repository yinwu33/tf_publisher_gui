import sys
from functools import partial

import rospy

from PyQt5 import QtCore, QtGui, QtWidgets

import app.init_ui
from app.ui import Ui_MainWindow
from app.tf_publisher import TFPublisher
from app.my_ui import MyUiMainWindow


if __name__ == "__main__":
    rospy.init_node("tf_manager")
    tf_manager_app = QtWidgets.QApplication(sys.argv)
    ui = MyUiMainWindow()
    windows = QtWidgets.QMainWindow()
    ui.setupUi(windows)
    
    ui.setUiFunctions()
    
    windows.show()
    sys.exit(tf_manager_app.exec_())