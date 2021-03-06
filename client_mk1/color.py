import numpy as np


class Color(object):
    """
    A Color represents a range of colors, used as a boolean condition
    to match against templates.
    For the hue component, if the minimum is greater than the maximum,
    the range wraps around to accommodate.
    """

    def __init__(self, val=None, tol=10, minimum=None, maximum=None, colorspace='HSV'):
        if colorspace != 'HSV':
            # TODO: allow black and white color space
            raise Exception("Invalid colorspace, only HSV supported")

        if minimum is None:
            minimum = np.array(val) - tol
        if maximum is None:
            maximum = np.array(val) + tol
        self.min = minimum
        self.max = maximum

    def matches(self, color):
        """
        Checks whether a given color matches the range.
        Args:
            color (list): An indexable color vector

        Returns:
            matches (bool): Does the given color match the range?

        """
        # Check hue condition
        if self.min[0] > self.max[0]:
            # The hue range wraps past the edge
            if self.max[0] < color[0] < self.min[0]:
                return False
        else:
            if color[0] > self.max[0] or color[0] < self.min[0]:
                return False

        # Check saturation and value conditions
        for i in (1, 2):
            if color[i] > self.max[i] or color[i] < self.min[i]:
                return False

        return True
