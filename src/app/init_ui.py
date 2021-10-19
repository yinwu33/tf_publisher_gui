from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets

from app.ui import Ui_MainWindow

def clicked_pushButton_update(ui: Ui_MainWindow):
    base_frame_id: str = ui.lineEdit_base_frame_id.text()
    child_frame_id: str = ui.lineEdit_child_frame_id.text()
    x: float = ui.horizontalSlider_x.value()

def clicked_pushbutton_publish(ui: Ui_MainWindow):
    ui.lineEdit_base_frame_id.setText("fuck you")
    print('fk you')

def initUiFunctions(ui: Ui_MainWindow):
    ui.pushButton_publish.clicked.connect(partial(clicked_pushbutton_publish, ui))
    