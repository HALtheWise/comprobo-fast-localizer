import numpy as np

import quaternion
import rospy
import tf
from geometry_msgs.msg import PoseStamped, Pose, Vector3, Quaternion
from std_msgs.msg import Header


class RosHandler(object):
    """
    The RosHandler is responsible for connecting to ROS and performing
    the coordinate transformations necessary to convert OpenCV coordinates
    which operate on an z-forward convention to ROS coordinates, which
    are x-forward.
    """
    def __init__(self):
        rospy.init_node('fast_localization_client')
        try:
            # In case the publisher is already registered, unregister it.
            self.pose_pub.unregister()
        except AttributeError:
            # "has no attribute pose_pub"
            pass

        self.pose_pub = rospy.Publisher('/pose', PoseStamped, queue_size=10)

    def publish_pose(self, pos, quat):
        """
        publish_pose converts a position and orientation in OpenCV coordinates
        into ROS coordinates, then publishes the result as a transform and as
        a PoseStamped.

        Args:
            pos (np.array): A length-3 np array representing (x,y,z) of camera
            quat (np.quaternion): The orientation of the camera

        Returns: None
        """

        # Convert the position and quaternion from OpenCV coordinates to ROS coordinates
        pos = [pos[2], -pos[0], -pos[1]]

        quat = np.quaternion(0, 0, 0, 1) * quat
        quatList = quaternion.as_float_array(quat.normalized()).flatten()
        quatList[1], quatList[2] = quatList[2], quatList[1]

        quatList[2] *= -1
        quatList[3] *= -1

        # Publish the result as a Pose in map frame
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
