import cv2
import cv.constants as constants
import numpy as np


class ImageBackgroundRemover:
    def __init__(self):
        self.model = cv2.createBackgroundSubtractorMOG2(constants.BACKGROUND_REMOVER_MODEL_HISTORY_SIZE,
                                                        constants.BG_SUBTRACTION_THRESHOLD)
        self.calibrated = True

    def remove_background_from_image(self, image):
        mask = self.model.apply(image, learningRate=constants.BG_SUBTRACTION_MODEL_LEARNING_RATE)
        kernel = np.ones((constants.BACKGROUND_REMOVER_KERNEL_SIZE, constants.BACKGROUND_REMOVER_KERNEL_SIZE), np.uint8)
        masktmp = cv2.erode(mask, kernel, iterations=1)
        image_without_bg = cv2.bitwise_and(image, image, mask=masktmp)
        return image_without_bg

    def set_need_calibration(self):
        self.calibrated = False
