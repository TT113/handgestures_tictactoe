import cv2
import cv.constants as constants
import copy

def flip_frame(frame):
    """Flips the frame horizontally for usability"""
    return cv2.flip(frame, 1)


def crop_frame(frame, x_range, y_range):
    return frame[x_range[0]: x_range[1], y_range[0]:y_range[1]]


def show_frame(frame, caption):
    cv2.imshow(caption, frame)


def convert_frame_to_gray_scale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def perform_gaussian_blur(frame, constant):
    return cv2.GaussianBlur(frame, (constant, constant), 0)


def smooth_frame(frame):
    # smoothing for noise removing
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