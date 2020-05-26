from engine.tick_generator import RunLoopMember
import cv2
import cv.constants as constants


class CameraFrameUpdater(RunLoopMember):
    def __init__(self, frame_receiver, renderer):
        RunLoopMember.__init__(self)
        self.frame_receiver = frame_receiver
        self.renderer = renderer

    def tick(self):
        frame = self.frame_receiver.last_processed_frame
        if frame is not None:
            self.renderer.set_camera_frame(frame)


class CameraFrameUpdaterWithDebugBlending(CameraFrameUpdater):
    def __init__(self, frame_receiver, renderer, debug_info_source):
        CameraFrameUpdater.__init__(self, frame_receiver, renderer)
        self.debug_info_source = debug_info_source

    def __transform_frame(self, frame):
        new_frame = cv2.resize(frame, (constants.UI_WINDOW_WIDTH, constants.UI_WINDOW_HEIGHT))
        recolored_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGB)
        recolored_frame = recolored_frame.swapaxes(0, 1)
        return recolored_frame

    def tick(self):
        debug_frame = self.debug_info_source.debug_frame
        frame = self.frame_receiver.last_processed_frame

        if debug_frame is None:
            if frame is not None:
                self.renderer.set_camera_frame(frame)
            return

        debug_frame = self.__transform_frame(debug_frame)

        target_shape_side = int(constants.UI_WINDOW_WIDTH * constants.ROI_SIZE)
        debug_frame = cv2.resize(debug_frame, (target_shape_side, target_shape_side))

        begin_recognition_frame_x = int(constants.ROI_Y_START * frame.shape[1])
        begin_recognition_frame_y = int(frame.shape[0] * constants.ROI_X_START)

        under_frame = frame[begin_recognition_frame_y:begin_recognition_frame_y + debug_frame.shape[0],
            begin_recognition_frame_x:begin_recognition_frame_x + debug_frame.shape[1]]

        debug_frame = cv2.multiply(debug_frame, debug_frame)
        under_frame = cv2.subtract(under_frame, debug_frame)

        frame[begin_recognition_frame_y:begin_recognition_frame_y + debug_frame.shape[0],
        begin_recognition_frame_x:begin_recognition_frame_x + debug_frame.shape[1]] = under_frame

        if frame is not None:
            self.renderer.set_camera_frame(frame)


