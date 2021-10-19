import math
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets

import rospy
import tf2_ros
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from geometry_msgs.msg import TransformStamped

from app.ui import Ui_MainWindow
# from app.tf_publisher import TFPublisher

PI = math.pi

class MyUiMainWindow(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        
        # consider only one tf
        self.online = True
        self.tf_msg_list = []
        
        self.current_select_row = -1
        self.current_tf: TransformStamped = None
        
        self.tf_publisher = tf2_ros.StaticTransformBroadcaster()
        
        self.protect = False

    @staticmethod
    def value_slider2spinbox(value: int, scale: int = 100, offset: int = 500) -> float:
        return (value - offset) / scale
    
    @staticmethod
    def value_spinbox2slider(value: float, scale: int = 100, offset: int = 500) -> int:
        return value * scale + offset
    
    def setUiFunctions(self):
        # create new tf and publish it
        self.pushButton_publish.clicked.connect(self.clicked_pushbutton_publish)
        
        # delete tf from table, no change to published tf
        self.pushButton_delete.clicked.connect(self.clicked_pushButton_delete)
        
        # reset parameters
        self.pushButton_reset_all.clicked.connect(self.clicked_pushButton_reset_all)
        self.pushButton_reset_x.clicked.connect(self.clicked_pushButton_reset_x)
        self.pushButton_reset_y.clicked.connect(self.clicked_pushButton_reset_y)
        self.pushButton_reset_z.clicked.connect(self.clicked_pushButton_reset_z)
        self.pushButton_reset_roll.clicked.connect(self.clicked_pushButton_reset_roll)
        self.pushButton_reset_pitch.clicked.connect(self.clicked_pushButton_reset_pitch)
        self.pushButton_reset_yaw.clicked.connect(self.clicked_pushButton_reset_yaw)
        
        # xyz slots
        self.horizontalSlider_x.valueChanged.connect(self.valueChanged_horizentalSlider_x)
        self.horizontalSlider_y.valueChanged.connect(self.valueChanged_horizentalSlider_y)
        self.horizontalSlider_z.valueChanged.connect(self.valueChanged_horizentalSlider_z)
        self.doubleSpinBox_x.valueChanged.connect(self.valueChanged_spinBox_x)
        self.doubleSpinBox_y.valueChanged.connect(self.valueChanged_spinBox_y)
        self.doubleSpinBox_z.valueChanged.connect(self.valueChanged_spinBox_z)
        
        # roll pitch yaw slots
        self.horizontalSlider_roll.valueChanged.connect(self.valueChanged_horizentalSlider_roll)
        self.horizontalSlider_pitch.valueChanged.connect(self.valueChanged_horizentalSlider_pitch)
        self.horizontalSlider_yaw.valueChanged.connect(self.valueChanged_horizentalSlider_yaw)
        self.spinBox_roll.valueChanged.connect(self.valueChanged_spinBox_roll)
        self.spinBox_pitch.valueChanged.connect(self.valueChanged_spinBox_pitch)
        self.spinBox_yaw.valueChanged.connect(self.valueChanged_spinBox_yaw)
        
        # table widget
        self.tableWidget.setHorizontalHeaderLabels(['base_frame_id', 'child_frame_id'])
        self.tableWidget.clicked.connect(self.clicked_tableWidget_item)    

    def online_update(self):
        self.update_tf()            
        # self.refresh_display()
        self.refresh_text_current_tf()
        self.refresh_text_info()

    # tablewidget
    def clicked_tableWidget_item(self, item: QtWidgets.QTableWidgetItem):
        self.protect = True
        
        self.current_select_row = item.row()
        self.current_tf = self.tf_msg_list[self.current_select_row]

        self.refresh_display()   
             
        self.protect = False
                
    # spinBox - roll, pitch, yaw
    def valueChanged_spinBox_roll(self):
        value = self.spinBox_roll.value()
        self.horizontalSlider_roll.setValue(value+180)
        self.online_update()
        
    def valueChanged_spinBox_pitch(self):
        value = self.spinBox_pitch.value()
        self.horizontalSlider_pitch.setValue(value+180)
        self.online_update()
    
    def valueChanged_spinBox_yaw(self):
        value = self.spinBox_yaw.value()
        self.horizontalSlider_yaw.setValue(value+180)
        self.online_update()
    
    # horizentalSlider - roll, pitch, yaw
    def valueChanged_horizentalSlider_roll(self):
        value = self.horizontalSlider_roll.value() - 180
        self.spinBox_roll.setValue(value)
        self.online_update()
    
    def valueChanged_horizentalSlider_pitch(self):
        value = self.horizontalSlider_pitch.value() - 180
        self.spinBox_pitch.setValue(value)
        self.online_update()
    
    def valueChanged_horizentalSlider_yaw(self):
        value = self.horizontalSlider_yaw.value() - 180
        self.spinBox_yaw.setValue(value)
        self.online_update()
    
    # doubleSpinBox - xyz
    def valueChanged_spinBox_x(self):
        value = self.doubleSpinBox_x.value()
        self.horizontalSlider_x.setValue(self.value_spinbox2slider(value))
        self.online_update()
        
    def valueChanged_spinBox_y(self):
        value = self.doubleSpinBox_y.value()
        self.horizontalSlider_y.setValue(self.value_spinbox2slider(value))
        self.online_update()
        
    def valueChanged_spinBox_z(self):
        value = self.doubleSpinBox_z.value()
        self.horizontalSlider_z.setValue(self.value_spinbox2slider(value))
        self.online_update()
    
    # horizentalSlider - xyz
    def valueChanged_horizentalSlider_x(self):
        value = self.value_slider2spinbox(self.horizontalSlider_x.value())
        self.doubleSpinBox_x.setValue(value)
        self.online_update()
    
    def valueChanged_horizentalSlider_y(self):
        value = self.value_slider2spinbox(self.horizontalSlider_y.value())
        self.doubleSpinBox_y.setValue(value)
        self.online_update()
    
    def valueChanged_horizentalSlider_z(self):
        value = self.value_slider2spinbox(self.horizontalSlider_z.value())
        self.doubleSpinBox_z.setValue(value)
        self.online_update()
    
    # button
    def clicked_pushButton_reset_all(self):
        self.doubleSpinBox_x.setValue(0)
        self.doubleSpinBox_y.setValue(0)
        self.doubleSpinBox_z.setValue(0)
        self.spinBox_roll.setValue(0)
        self.spinBox_pitch.setValue(0)
        self.spinBox_yaw.setValue(0)
        
        self.online_update()
    
    def clicked_pushButton_reset_x(self):
        self.doubleSpinBox_x.setValue(0)
        self.online_update()
    
    def clicked_pushButton_reset_y(self):
        self.doubleSpinBox_y.setValue(0)
        self.online_update()
    
    def clicked_pushButton_reset_z(self):
        self.doubleSpinBox_z.setValue(0)
        self.online_update()
        
    def clicked_pushButton_reset_roll(self):
        self.spinBox_roll.setValue(0)
        self.online_update()
    
    def clicked_pushButton_reset_pitch(self):
        self.spinBox_pitch.setValue(0)
        self.online_update()
        
    def clicked_pushButton_reset_yaw(self):
        self.spinBox_yaw.setValue(0)
        self.online_update()
    
    def clicked_pushButton_delete(self):
        self.tableWidget.removeRow(self.current_select_row) # delete from table
        del self.tf_msg_list[self.current_select_row] # delete from list
        
        self.current_select_row = -1
        self.current_tf = None
        self.publish()
        
        self.refresh_display()

    def clicked_pushbutton_publish(self):
        # self.update_distance_text() #! delete
        transform = self.create_new_tf()
        self.tf_msg_list.append(transform)
        self.publish()
        
        self.table_item_insert(transform)
        
    def update_tf(self): 
        if self.protect:
            return
        if self.current_select_row == -1:
            assert self.current_tf == None
        else:
            self.current_tf.transform.translation.x = self.doubleSpinBox_x.value()
            self.current_tf.transform.translation.y = self.doubleSpinBox_y.value()
            self.current_tf.transform.translation.z = self.doubleSpinBox_z.value()
            
            roll: float = self.spinBox_roll.value() * PI / 180
            pitch: float = self.spinBox_pitch.value() * PI / 180
            yaw: float = self.spinBox_yaw.value() * PI / 180
            q = quaternion_from_euler(roll, pitch, yaw)
            
            self.current_tf.transform.rotation.x = q[0]
            self.current_tf.transform.rotation.y = q[1]
            self.current_tf.transform.rotation.z = q[2]
            self.current_tf.transform.rotation.w = q[3]
        self.publish()
    
    def publish(self):
        self.tf_publisher.sendTransform(self.tf_msg_list)
    
    def create_new_tf(self) -> TransformStamped:
        """create a empty tf with specific base_frame_id and child_frame_id

        Returns:
            TransformStamped: [description]
        """
        transform = TransformStamped()
        
        transform.header.frame_id = self.lineEdit_base_frame_id.text()
        transform.child_frame_id = self.lineEdit_child_frame_id.text()
        transform.transform.translation.x = 0
        transform.transform.translation.y = 0
        transform.transform.translation.z = 0
        transform.transform.rotation.x = 0
        transform.transform.rotation.y = 0
        transform.transform.rotation.z = 0
        transform.transform.rotation.w = 1    
        
        return transform

    
    def table_item_insert(self, transform: TransformStamped()):
        base_frame_id = transform.header.frame_id
        child_frame_id = transform.child_frame_id
        
        self.tableWidget.insertRow((self.tableWidget.rowCount()))
        self.tableWidget.setItem(self.tableWidget.rowCount()-1, 0, QtWidgets.QTableWidgetItem(base_frame_id))
        self.tableWidget.setItem(self.tableWidget.rowCount()-1, 1, QtWidgets.QTableWidgetItem(child_frame_id))
    
    # * Refresh all display
    def refresh_display(self):
        self.protect = True
        
        self.refresh_control_panel()
        self.refresh_text_current_tf()
        self.refresh_text_info()
        
        self.protect = False
    
    def refresh_control_panel(self):
        if self.current_select_row == -1:
            # select nothing
            assert self.current_tf == None
            self.doubleSpinBox_x.setValue(0)
            self.doubleSpinBox_y.setValue(0)
            self.doubleSpinBox_z.setValue(0)
            
            self.spinBox_roll.setValue(0)
            self.spinBox_pitch.setValue(0)
            self.spinBox_yaw.setValue(0)
        else:
            # select a tf
            # update 6 spinbox values
            self.doubleSpinBox_x.setValue(self.current_tf.transform.translation.x)
            self.doubleSpinBox_y.setValue(self.current_tf.transform.translation.y)
            self.doubleSpinBox_z.setValue(self.current_tf.transform.translation.z)
            
            q = [self.current_tf.transform.rotation.x,
                self.current_tf.transform.rotation.y,
                self.current_tf.transform.rotation.z,
                self.current_tf.transform.rotation.w]
            euler = euler_from_quaternion(q)
            self.spinBox_roll.setValue(euler[0]*180/PI)
            self.spinBox_pitch.setValue(euler[1]*180/PI)
            self.spinBox_yaw.setValue(euler[2]*180/PI)

    def refresh_text_current_tf(self):
        if self.current_select_row == -1:
            # select nothing
            assert self.current_tf == None
            self.label_info.setText("Nothing selected")
        else:
            base_frame_id = self.current_tf.header.frame_id
            child_frame_id = self.current_tf.child_frame_id
            text = f"Current select TF:  {self.current_select_row}  [ {base_frame_id} - {child_frame_id} ]"
            self.label_info.setText(text)

    def refresh_text_info(self):
        if self.current_select_row == -1:
            # select nothing
            assert self.current_tf == None
            self.textBrowser_info.setText("Nothing selected")
        else:
            q = [self.current_tf.transform.rotation.x,
                self.current_tf.transform.rotation.y,
                self.current_tf.transform.rotation.z,
                self.current_tf.transform.rotation.w]
            euler = euler_from_quaternion(q)
            x = self.current_tf.transform.translation.x
            y = self.current_tf.transform.translation.y
            z = self.current_tf.transform.translation.z
            text = f'''base_frame_id: &nbsp;&nbsp;{self.current_tf.header.frame_id}<br/>
                    child_frame_id: &nbsp;&nbsp;{self.current_tf.child_frame_id}<br/>
                    translation: <br/>&nbsp;&nbsp;&nbsp;&nbsp;{self.current_tf.transform.translation}<br/>
                    quaternion: <br/>&nbsp;&nbsp;&nbsp;&nbsp;{self.current_tf.transform.rotation}<br/>
                    euler (radio): <br/>&nbsp;&nbsp;&nbsp;&nbsp;{[euler[0], euler[1], euler[2]]}<br/>
                    euler (degree): <br/>&nbsp;&nbsp;&nbsp;&nbsp;{[euler[0]*180/PI, euler[1]*180/PI, euler[2]*180/PI]}<br/>
                    distance: &nbsp;&nbsp;{math.sqrt(x**2 + y**2 + z**2)} m'''
                    # todo add more info
                    
            self.textBrowser_info.setText(text)

