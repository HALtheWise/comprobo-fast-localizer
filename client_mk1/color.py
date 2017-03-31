class Color(object):
    def __init__(self, minimum, maximum, colorspace='HSV'):
        if colorspace != 'HSV':
            raise Exception("Invalid colorspace, only HSV supported")

        self.min = minimum
        self.max = maximum

    def matches(self, color):
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
