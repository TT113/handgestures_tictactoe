import cv.math_utils as math_utils

def invalid_point(point, angle, frame_shape):
    offset_dist = 40
    offset_angle = 35
    if (point[0][0] <= offset_dist or frame_shape[0] - point[0][1] <= offset_dist) and abs(angle-90)<=offset_angle:
        return True
    elif (point[0][1] <= offset_dist or frame_shape[1] - point[0][0] <= offset_dist) and abs(angle-90)<=offset_angle:
        return True
    else:
        return False


def generate_input(center, points, angles, frame_shape):
    center_dictances = [math_utils.distance_beetwen_points(point[0], center) for point in points]
    center_dictances_pairs = [(i, value) for i, value in enumerate(center_dictances)]
    angles_pairs = [(i, value) for i, value in enumerate(angles)]
    center_dictances_pairs_cor = []
    angles_pairs_cor = []
    for i in range(len(points)):
        if not invalid_point(points[i], angles[i], frame_shape):
            center_dictances_pairs_cor.append(center_dictances_pairs[i])
            angles_pairs_cor.append(angles_pairs[i])
    center_dictances_pairs_cor.sort(key=lambda x: x[1], reverse=True)
    angles_pairs_cor.sort(key=lambda x: x[1])
    if len(center_dictances_pairs_cor)> 0:
        pos_in_angles = angles_pairs_cor.index(min(angles_pairs_cor, key=lambda t: t[1]))
        pos_in_distances = center_dictances_pairs_cor.index(max(center_dictances_pairs_cor, key=lambda t: t[1]))
        min_ind1 = center_dictances_pairs_cor[pos_in_distances][0]
        min_ind2 = angles_pairs_cor[pos_in_angles][0]
        if min_ind1 == min_ind2 and angles[angles_pairs_cor[pos_in_angles][0]]<110:
            return points[min_ind2][0]
        else:
            return None
    else:
        return None
