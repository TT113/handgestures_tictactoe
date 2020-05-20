import cv2
import cv.constants as constants
import numpy as np


class ImageBackgroundRemover:

    def __init__(self):
        self.model = cv2.createBackgroundSubtractorMOG2(100, constants.BG_SUBTRACTION_THRESHOLD)
        self.calibrated = True

    def remove_background_from_image(self, image):
        mask = self.model.apply(image, learningRate=constants.BG_SUBTRACTION_MODEL_LEARNING_RATE)
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        # res = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        kernel = np.ones((5, 5), np.uint8)
        fgmask = cv2.erode(mask, kernel, iterations=1)
        image_without_bg = cv2.bitwise_and(image, image, mask=fgmask)
        return image_without_bg

    def set_need_calibration(self):
        self.calibrated = False