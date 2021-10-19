import rospy

import tf2_ros
from tf.transformations import quaternion_from_euler
from geometry_msgs.msg import TransformStamped


class TFPublisher:
    def __init__(self,
                 base_frame_id,
                 child_frame_id,
                 x: float = 0,
                 y: float = 0,
                 z: float = 0,
                 roll: int = 0,
                 pitch: int = 0,
                 yaw: int = 0):

        self.transform = TransformStamped()
        self.update(base_frame_id,
                    child_frame_id,
                    x=x,
                    y=y,
                    z=z,
                    roll=roll,
                    pitch=pitch,
                    yaw=yaw)

        self.tf_publisher = tf2_ros.StaticTransformBroadcaster()

    def update(self,
               base_frame_id,
               child_frame_id,
               x: float = 0,
               y: float = 0,
               z: float = 0,
               roll: int = 0,
               pitch: int = 0,
               yaw: int = 0):
        self.transform.header.frame_id = base_frame_id
        self.transform.child_frame_id = child_frame_id

        self.transform.transform.translation.x = x
        self.transform.transform.translation.y = y
        self.transform.transform.translation.z = z

        q = quaternion_from_euler(roll, pitch, yaw)
        self.transform.transform.rotation.x = q[0]
        self.transform.transform.rotation.y = q[1]
        self.transform.transform.rotation.z = q[2]
        self.transform.transform.rotation.w = q[3]

    def publish(self):
        self.transform.header.stamp = rospy.Time.now()
        self.tf_publisher.sendTransform(self.transform)
