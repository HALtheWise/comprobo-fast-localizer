import image_geometry
from camera_calibration_parsers import readCalibration

_, calibration = readCalibration("../calibration/unstabilized_pixel.yaml")
camera = image_geometry.PinholeCameraModel()
camera.fromCameraInfo(calibration)
