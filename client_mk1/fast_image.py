import cv2


class Image(object):
    """
    Image is an object that allows lazy access to pixel data
    while tracking statistics about which pixels have been accessed.
    """
    pixelsAccessed = []

    def __init__(self, img):
        self.img = img

    def getHSV(self, x, y):
        x = int(x)
        y = int(y)
        rgb = self.img[y:y + 1, x:x + 1]
        hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)

        self.pixelsAccessed.append((x, y))

        if hsv is None:
            raise IndexError

        return hsv[0, 0]

    def draw(self, img):
        """
        Colors the accessed pixels red in an image, intended for visualization
        purposes.
        Args:
            img (np.array): an image to draw on
        Returns:
            None
        """
        color = (0, 0, 255)
        for p in self.pixelsAccessed:
            try:
                img[p[1], p[0]] = color
            except IndexError:
                # Out of bounds
                pass

