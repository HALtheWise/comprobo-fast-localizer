import numpy as np

import cv2

from searchers import do_binary_search


class Circle2D(object):
    """
    As a 2D object, Circle2D lives entirely in distorted pixel coordinates.
    """

    def __init__(self, center, radius, colorRange):
        self.center = np.array(center)
        self.radius = radius
        self.color = colorRange

        # TODO: this should be a scalar with more reasonable behavior
        self.confidence = True

    def draw(self, img):
        """
        Taking in a numpy array representing an OpenCV image,
        draws a visual debugging indication of this feature
        """
        try:
            drawColor = (128, 255, 0) if self.confidence else (0, 0, 255)
            cv2.circle(img, tuple(map(int, self.center)), int(self.radius), drawColor, thickness=5)
            cv2.circle(img, tuple(map(int, self.center)), 5, drawColor, thickness=-1)

        except IndexError:
            # Cannot draw features living outside the frame
            pass

    def distance(self, point):
        point = np.array(point)
        return point - self.center

    def refine(self, image, verbose=False, searchRange=200):
        """
        Taking in an Image object, updates this feature to better align
        with the observed pixels.

        searchRange represents the maximum pixel distance the target
            object could have moved.
        """

        def matchesAt(x, y):
            return self.color.matches(image.getHSV(x, y))

        try:
            if matchesAt(*self.center):
                self.confidence = True

            else:
                self.confidence = False
                if verbose:
                    print "Center point color is {}".format(
                        image.getHSV(*self.center))
                return

            # NOISE_DIST = 3

            maxDist = searchRange + self.radius

            ## Find the x-coordinate of the center of the circle

            left = np.array((-1, 0))
            leftPoint = do_binary_search(image, self.color,
                                         self.center, self.center - maxDist * left)

            right = np.array((1, 0))
            rightPoint = do_binary_search(image, self.color,
                                          self.center, self.center - maxDist * right)

            self.center = np.array((leftPoint + rightPoint) / 2, dtype=np.int32)

            ## Find the y-coordinate of the center
            up = np.array((0, 1))
            topPoint = do_binary_search(image, self.color,
                                        self.center, self.center - maxDist * up)

            down = np.array((0, -1))
            bottomPoint = do_binary_search(image, self.color,
                                           self.center, self.center - maxDist * down)

            self.center = np.array((topPoint + bottomPoint) / 2, dtype=np.int32)

            ## Calculate the radius
            self.radius = int(np.linalg.norm(topPoint - bottomPoint) / 2)

        except IndexError:
            self.confidence = False
            if verbose:
                print "Index out of bounds of image"

    def __repr__(self):
        return 'Circle(center={}, radius={})'.format(
            self.center,
            self.radius
        )
