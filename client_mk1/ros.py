import numpy as np

import quaternion
import rospy
import tf
from geometry_msgs.msg import PoseStamped, Pose, Vector3, Quaternion
from std_msgs.msg import Header


class RosHandler(object):
    def __init__(self):
        rospy.init_node('fast_localization_client')
        try:
            self.pose_pub.unregister()
        except:
            pass
        self.pose_pub = rospy.Publisher('/pose', PoseStamped, queue_size=10)

    def publish_pose(self, pos, quat):
        # Convert the position and quaternion from OpenCV coordinates to ROS coordinates
        pos = [pos[2], -pos[0], -pos[1]]

        quat = np.quaternion(0, 0, 0, 1) * quat
        quatList = quaternion.as_float_array(quat.normalized()).flatten()
        quatList[1], quatList[2] = quatList[2], quatList[1]

        quatList[2] *= -1
        quatList[3] *= -1

        # Pulish the result as a Pose in map frame
        self.pose_pub.publish(PoseStamped(
            header=Header(frame_id='map'),
            pose=Pose(
                position=Vector3(*pos),
                orientation=Quaternion(*quatList))))

        # Publish the result as a transform from map frame to camera frame
        br = tf.TransformBroadcaster()
        br.sendTransform(pos,
                         quatList,
                         rospy.Time.now(),
                         'camera',
                         'map')
