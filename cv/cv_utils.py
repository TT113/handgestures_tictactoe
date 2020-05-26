import cv2
import cv.constants as constants
import copy
import math


def flip_frame(frame):
    """Flips the frame horizontally for usability"""
    return cv2.flip(frame, 1)


def crop_frame(frame, x_range, y_range):
    """Crops the frame by X, Y region"""
    return frame[y_range[0]:y_range[1], x_range[0]: x_range[1]]


def show_frame(frame, caption):
    cv2.imshow(caption, frame)


def convert_frame_to_gray_scale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def perform_gaussian_blur(frame, constant):
    return cv2.GaussianBlur(frame, (constant, constant), 0)


def smooth_frame(frame):
    """smoothing for noise removing"""
    return cv2.bilateralFilter(frame, 5, 90, 150)


def extract_contours_from_image(img):
    contours, hierarchy = cv2.findContours(copy.deepcopy(img), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def get_contour_area(contour):
    return cv2.contourArea(contour)


def get_polygon_center(polygon):
    M = cv2.moments(polygon)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return cX, cY
    else:
        return 0, 0


def draw_point(image, coordinates):
    cv2.circle(image, coordinates, radius=10, color=(0, 0, 255), thickness=10)


def draw_text(image, point, text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    offset = 10
    bottomLeftCornerOfText = (point[0]+offset, point[1]+offset)
    fontScale = 0.6
    fontColor = (255, 255, 255)
    lineType = 2

    cv2.putText(image, text,
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                lineType)


def get_convex_hull(points):
    if points is not None:
        return cv2.convexHull(points)
    else:
        return None


def calculate_fingers(res):
    hull = cv2.convexHull(res, returnPoints=False)
    if len(hull) > 3:
        defects = cv2.convexityDefects(res, hull)
        if defects is not None:
            cnt = 0
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i][0]
                start = tuple(res[s][0])
                end = tuple(res[e][0])
                far = tuple(res[f][0])
                a = math.sqrt((end[0] - start[0]) ** 2 +
                              (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 +
                              (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) /
                                  (2 * b * c))  # cosine theorem
                if angle <= math.pi * 0.5:  # angle less than 90 degree, treat as fingers
                    cnt += 1
            return cnt
    return 0
