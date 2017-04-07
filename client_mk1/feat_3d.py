import numpy as np

from client_mk1.feat_2d import Circle2D
from client_mk1.calibration import camera


class Sphere3D(object):
    """
    Sphere3D represents a sphere known to exist in 3D map-space.
    """

    def __init__(self, center, radius, colorRange):
        self.center = np.array(center)
        self.radius = radius
        self.color = colorRange

        # TODO: this should be a scalar with more reasonable behavior
        self.confidence = True

    def project(self, pos, orientation):
        """
        Returns the coordinates of the given point in the camera image
        """
        relative_center = self.center - pos
        relative_center = np.dot(np.transpose(orientation), relative_center)

        center2D = camera.project3dToPixel(relative_center)
        x, y, w = relative_center
        radius2D = camera.fx() * self.radius / w

        return Circle2D(center2D, radius2D, self.color)
