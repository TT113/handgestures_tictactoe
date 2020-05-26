import cv2
import numpy as np
import cv.camera as camera
import cv.cv_utils as cv_utils
import cv.constants as constants
import cv.geometry_utils as geometry_utils
import cv.input_generator as input_generator
import cv.image_background_remove as image_background_remove
import math
from model.input import *
import time

class CvInputConroller:
    def __init__(self, scene, input_quantization_seconds, resource_loaer):
        self.camera = camera.Camera()
        self.imageBackgroundRemover = None
        self.scene = scene
        self.input_quantization_seconds = input_quantization_seconds
        self.last_input_submitted = time.time()
        self.last_processed_frame = None
        self.previous_command = None
        self.previous_frame = None
        self.background = None

        self.hatched_image = cv2.imread(resource_loaer.get_path_for_asset('hatch_texture.png'))
        self.hatched_image = cv2.resize(self.hatched_image, (220, 220))

    def start(self):
        self.camera.start_recording()

    def stop_and_destroy_windows(self):
        self.camera.stop_recording()

    def calibrate(self):
        self.imageBackgroundRemover = image_background_remove.ImageBackgroundRemover()
        self.background = self.previous_frame
        print('calibrated')

    def remember_camera_frame(self, new_frame):
        new_frame = cv2.resize(new_frame, (constants.UI_WINDOW_WIDTH, constants.UI_WINDOW_HEIGHT))
        recolored_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGB)
        recolored_frame = recolored_frame.swapaxes(0, 1)
        self.last_processed_frame = recolored_frame


    def tick(self):
        """
            Main CV gesture recognition process
            Calibration process without hand is needed at first
            Consecutive process of filtering and masking implemented
            Uses learning background subtraction model
        """
        frame = self.camera.get_current_frame()
        frame = cv2.resize(frame, (800, 450))
        if self.imageBackgroundRemover is not None and self.imageBackgroundRemover.calibrated:
            img = self.imageBackgroundRemover.remove_background_from_image(frame)
            img = cv_utils.crop_frame(img,
                                      (int(constants.ROI_X_START * img.shape[1]), int((constants.ROI_X_START + constants.ROI_SIZE) * img.shape[1])),
                      (int(img.shape[0]*constants.ROI_Y_START), int((constants.ROI_Y_START*img.shape[0] + constants.ROI_SIZE * img.shape[1]))))
            """ Uncomment for checking intermediate mask results"""
            # cv_utils.show_frame(img, "mask")
            gray = cv_utils.convert_frame_to_gray_scale(img)
            blur = cv_utils.perform_gaussian_blur(gray, constants.GAUSSIAN_BLUR_VAL)
            # cv2.imshow('blur', blur)
            _, thresh = cv2.threshold(blur, constants.BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)
            _, thresh2 = cv2.threshold(blur, constants.BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)
            # cv_utils.show_frame(thresh, "filtered")
            _, blured_frame = cv2.threshold(cv_utils.perform_gaussian_blur(cv_utils.convert_frame_to_gray_scale(frame), 55), constants.BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)
            contours = cv_utils.extract_contours_from_image(thresh)
            contours_fingers = cv_utils.extract_contours_from_image(thresh2)
            external_contour = geometry_utils.select_external_contour(contours)
            external_contour_fingers = geometry_utils.select_external_contour(contours_fingers)
            hull = cv_utils.get_convex_hull(external_contour)
            hull = geometry_utils.validate_convex_hull(hull, (img.shape[0], img.shape[1]))
            if hull is not None:
                offset = (int(constants.ROI_X_START * frame.shape[1]), int(constants.ROI_Y_START * frame.shape[0]))
                polygon_angles = geometry_utils.get_polygon_angles(hull)
                center1 = cv_utils.get_polygon_center(external_contour)
                input = input_generator.generate_input(center1, hull, polygon_angles, img.shape)
                if input is not None:
                    game_command = geometry_utils.get_vector_direction(input - np.array(center1))
                    command = str(game_command)
                    if game_command is not None:
                        if self.make_input(game_command):
                            cv_utils.draw_text(frame, (40, 40), command)
                    else:
                        print('set none command')
                        self.previous_command = None
                else:
                    finger_count = cv_utils.calculate_fingers(external_contour_fingers)
                    if finger_count >= 4:
                        self.make_input(Input.ENTER)
            self.hatch_detected_hand(frame, thresh)
            self.previous_frame = blur
        self.remember_camera_frame(frame)

    def hatch_detected_hand(self, frame, thresh):
        begin_recognition_frame_x = int(constants.ROI_X_START * frame.shape[1])
        begin_recognition_frame_y = int(frame.shape[0] * constants.ROI_Y_START)
        colored_tresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
        region = frame[begin_recognition_frame_y:begin_recognition_frame_y + thresh.shape[0],
                 begin_recognition_frame_x:begin_recognition_frame_x + thresh.shape[1]]
        g = cv2.bitwise_and(self.hatched_image, colored_tresh)
        g = cv2.multiply(g, g)
        region = cv2.subtract(region, g)
        frame[begin_recognition_frame_y:begin_recognition_frame_y + thresh.shape[0],
        begin_recognition_frame_x:begin_recognition_frame_x + thresh.shape[1]] = region

    def make_input(self, command):
        current_timestamp = time.time()
        if current_timestamp - self.last_input_submitted < self.input_quantization_seconds:
            return False

        self.last_input_submitted = current_timestamp
        print('input tick')

        if self.previous_command == command:
            print('inputting', command)
            self.scene.receive_input(command)
            return True

        self.previous_command = command
        return False

