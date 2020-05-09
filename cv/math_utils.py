import numpy as np
import math

#pi in degrees
PI_D = 180

def get_angle_between_vectors(a, b, c):
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    c_norm = np.linalg.norm(c)
    return np.degrees(np.arccos((a_norm**2+b_norm**2-c_norm**2)/2/a_norm/b_norm))


def distance_beetwen_points(a, b):
    return np.linalg.norm(a - b)