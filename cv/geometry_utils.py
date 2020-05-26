import numpy as np
import cv.constants as constants
import cv.cv_utils as cv_utils
from model.input import Input
import math

PI_D = 180  # pi in degrees


def relax_convex_hull(hull, img_shape):
    """ sequential relaxing of convex hull points
    hull - np array, shape = (N,1,2)
    """
    hull_relaxed = np.array([hull[0]])
    for i in range(1, len(hull)):
        # print(img_shape, hull[i])
        if np.linalg.norm(hull_relaxed[-1]-hull[i][0]) > constants.CONVEX_HULL_RELAX_THRESHOLD:
            hull_relaxed = np.append(hull_relaxed, [hull[i]], axis=0)
    if len(hull_relaxed) > 2 and np.linalg.norm(hull_relaxed[0]-hull_relaxed[-1]) < constants.CONVEX_HULL_RELAX_THRESHOLD:
        hull_relaxed = np.delete(hull_relaxed, -1, 0)
    return hull_relaxed


def get_angle_between_vectors(a, b, c):
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    c_norm = np.linalg.norm(c)
    return np.degrees(np.arccos((a_norm**2+b_norm**2-c_norm**2)/2/a_norm/b_norm))


def distance_between_points(a, b):
    return np.linalg.norm(a - b)


def select_external_contour(contours):
    if contours is not None and len(contours) > 0:
        return max(contours, key=lambda contour: cv_utils.get_contour_area(contour))
    else:
        return None


def validate_convex_hull(hull, img_shape):
    roi_area = img_shape[0] * img_shape[1]
    if hull is None:
        return None
    else:
        hull = relax_convex_hull(hull, img_shape)
        hull_area = cv_utils.get_contour_area(hull)
        return hull if (hull.shape[0] > 3 and
                        0.15 * roi_area < hull_area < roi_area * 0.95) else None


def get_polygon_angles(polygon):
    angles = []
    polygon = np.append(np.array([polygon[-1]]), np.append(polygon, [polygon[0]], axis=0), axis=0)
    length = len(polygon)-1

    for i in range(1, length):
        a = polygon[i][0] - polygon[i-1][0]
        b = polygon[i + 1][0] - polygon[i][0]
        c = polygon[i + 1][0] - polygon[i-1][0]
        angles.append(round(get_angle_between_vectors(a, b, c), 2))
    return angles


def get_angle_between_vector_and_x_axis(vector):
    """return value between [0, 2pi]"""
    res =  PI_D + np.degrees(np.arctan2(vector[1], vector[0]))
    return res if res > 0 else np.degrees(math.pi*2)+res


def get_vector_direction(vector):
    angle = get_angle_between_vector_and_x_axis(vector)
    if angle <= constants.DIRECTION_ANGLES_OFFSET or 2*PI_D - angle <= constants.DIRECTION_ANGLES_OFFSET:
        return Input.LEFT_ARROW
    elif abs(PI_D / 2 - angle) <= constants.DIRECTION_ANGLES_OFFSET:
        return Input.TOP_ARROW
    elif abs(PI_D - angle) <= constants.DIRECTION_ANGLES_OFFSET:
        return Input.RIGHT_ARROW
    elif abs(3*PI_D/2 - angle) <= constants.DIRECTION_ANGLES_OFFSET:
        return Input.BOTTOM_ARROW

