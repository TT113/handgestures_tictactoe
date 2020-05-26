import cv.geometry_utils as geometry_utils
from cv.constants import *


def is_invalid_point(point, angle, frame_shape):
    if (point[0][0] <= MIN_GESTURE_OFFSET_FROM_FRAME or
        frame_shape[0] - point[0][1] <= MIN_GESTURE_OFFSET_FROM_FRAME) \
            and abs(angle-90) <= MIN_GESTURE_ANGLE_OFFSET:
        return True
    elif (point[0][1] <= MIN_GESTURE_OFFSET_FROM_FRAME or
          frame_shape[1] - point[0][0] <= MIN_GESTURE_OFFSET_FROM_FRAME) \
            and abs(angle-90) <= MIN_GESTURE_ANGLE_OFFSET:
        return True
    else:
        return False


def generate_input(center, points, angles, frame_shape):
    """
    Iterates over all convex hull points and selects one that could indicate direction
    Selection is based on two parameters: corresponding to point angle and
    distance between point and convex hull polygon center

    !!! Points that are close to the border is considered invalid

    !!! Input could be not indicated (sometimes return None)
    """
    center_distances = [geometry_utils.distance_between_points(point[0], center) for point in points]
    center_distances_pairs = [(i, value) for i, value in enumerate(center_distances)]
    angles_pairs = [(i, value) for i, value in enumerate(angles)]
    center_distances_pairs_cor = []
    angles_pairs_cor = []
    for i in range(len(points)):
        if not is_invalid_point(points[i], angles[i], frame_shape):
            center_distances_pairs_cor.append(center_distances_pairs[i])
            angles_pairs_cor.append(angles_pairs[i])
    center_distances_pairs_cor.sort(key=lambda elem: elem[1], reverse=True)
    angles_pairs_cor.sort(key=lambda elem: elem[1])
    if len(center_distances_pairs_cor) > 0:
        pos_in_angles = angles_pairs_cor.index(min(angles_pairs_cor, key=lambda t: t[1]))
        pos_in_distances = center_distances_pairs_cor.index(max(center_distances_pairs_cor, key=lambda t: t[1]))
        min_ind1 = center_distances_pairs_cor[pos_in_distances][0]
        min_ind2 = angles_pairs_cor[pos_in_angles][0]
        if min_ind1 == min_ind2 and angles[angles_pairs_cor[pos_in_angles][0]]<110:
            return points[min_ind2][0]
        else:
            return None
    else:
        return None
