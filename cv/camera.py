import cv2
import cv.cv_utils as cv_utils


class Camera:
    def __init__(self):
        self.camera = None
        self.origin_resolution_width = -1
        self.origin_resolution_height = -1
        pass

    def start_recording(self):
        self.camera = cv2.VideoCapture(0)
        self.origin_resolution_width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.origin_resolution_height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def stop_recording(self):
        self.camera.release()
        cv2.destroyAllWindows()

    def is_recording(self):
        return self.camera.isOpened()

    def get_current_frame(self):
        _, frame = self.camera.read()
        return cv_utils.flip_frame(frame)

