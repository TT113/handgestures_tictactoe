import cv2
import cv.camera as camera
import cv.constants as constants
import cv.cv_utils as cv_utils
from keras.models import load_model
import numpy as np
from model.input import *
import time
from collections import Counter
from cv.cv_input_model import *


class NNInputController(CvInputModel):
    def __init__(self, scene, resource_loader):
        CvInputModel.__init__(self, scene)
        self.CATEGORY_MAP = {
            0: Input.TOP_ARROW,
            1: Input.LEFT_ARROW,
            2: Input.BOTTOM_ARROW,
            3: Input.RIGHT_ARROW,
            4: Input.ENTER,
            5: None
        }
        self.model = load_model(resource_loader.get_path_for_asset(constants.NN_MODEL_WEIGHTS_PATH))
        self.last_input_submitted = time.time()
        self.last_commands = []

    def mapper(self, val):
        return self.CATEGORY_MAP[val]

    def process_frame(self, frame):
        frame = cv2.resize(frame, (800, 450))
        img = cv_utils.crop_frame(frame,
                                  (int(constants.ROI_X_START * frame.shape[1]),
                                   int((constants.ROI_X_START + constants.ROI_SIZE) * frame.shape[1])),
                                  (int(frame.shape[0] * constants.ROI_Y_START),
                                   int((constants.ROI_Y_START * frame.shape[0] + constants.ROI_SIZE * frame.shape[1]))))

        img = cv2.resize(img, (constants.NN_IMAGE_INPUT_SIZE, constants.NN_IMAGE_INPUT_SIZE))
        prediction = self.model.predict(np.array([img]))
        gesture_numeric = np.argmax(prediction[0])
        gesture_name = self.mapper(gesture_numeric)
        cv_utils.draw_text(frame, (40, 40), str(gesture_name))
        self.process_gesture(gesture_name)

    def process_gesture(self, input):
        if input is None:
            self.last_commands = []
            return
        print(input)
        if len(self.last_commands) >= constants.NN_GESTURE_CONFIRMATION_SEQUENCE_LENGTH:
            ctr = Counter(self.last_commands)
            for command in ctr:
                count = ctr[command]
                if count > constants.NN_GESTURE_CONFIRMATION_COUNT \
                        and command is not None:
                    self.scene.receive_input(command)
            self.last_commands = []
        self.last_commands.append(input)