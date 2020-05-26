from engine.tick_generator import RunLoopMember
from cv.camera import Camera
import cv2
import cv.constants as constants


class CameraFrameReceiver(RunLoopMember):
    def __init__(self, new_frame_callback):
        RunLoopMember.__init__(self)
        self.new_frame_callback = new_frame_callback
        self.camera = Camera()
        self.last_processed_frame = None
        self.is_started = False

    def start(self):
        if self.is_started:
            return
        self.is_started = True
        self.camera.start_recording()

    def stop(self):
        if not self.is_started:
            return
        self.is_started = False
        self.camera.stop_recording()

    def tick(self):
        if not self.is_started:
            return

        frame = self.camera.get_current_frame()
        self.new_frame_callback(frame)

        new_frame = cv2.resize(frame, (constants.UI_WINDOW_WIDTH, constants.UI_WINDOW_HEIGHT))
        recolored_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGB)
        recolored_frame = recolored_frame.swapaxes(0, 1)
        self.last_processed_frame = recolored_frame

