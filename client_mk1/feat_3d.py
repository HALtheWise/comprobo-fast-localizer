import numpy as np

from feat_2d import Circle2D
from calibration import camera


class Sphere3D(object):
    """
    Sphere3D represents a sphere known to exist in 3D map-space.
    Note that we are using Sphere3D's to approximate disks, which works reasonably
    for the purposes of our demo.
    """

    def __init__(self, center, radius, colorRange):
        self.center = np.array(center)
        self.radius = radius
        self.color = colorRange

        # TODO: this should be a scalar with more reasonable behavior
        self.confidence = True

    def project(self, pos, orientation):
        """
        Returns a Circle2D representing the projection of the Sphere3D into
        the camera's field of view, were the camrea located at the given
        position and orientation (where orientation is a rotation matrix).
        """
        # Calculate the position of the sphere in camera-relative coordinates
        relative_center = self.center - pos
        # Transposing the rotation matrix is a cheap way of inverting it
        relative_center = np.dot(np.transpose(orientation), relative_center)

        # Calculate the pixel coordinates of the center of the circle
        center2D = camera.project3dToPixel(relative_center)

        # Calculate the radius by using the focal length of the camera
        x, y, w = relative_center
        radius2D = camera.fx() * self.radius / w

        return Circle2D(center2D, radius2D, self.color)
