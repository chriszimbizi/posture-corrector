import numpy as np


def get_landmark_coordinates(landmark, frame_shape: tuple) -> tuple:
    """
    Convert normalized landmark coordinates to pixel coordinates.

    :param landmark: Landmark object with x and y attributes.
    :param frame_shape: Shape of the frame (height, width).

    :return: Tuple of (x, y) coordinates in pixels.
    """
    return (int(landmark.x * frame_shape[1]), int(landmark.y * frame_shape[0]))


def calculate_angle(p1, p2, p3) -> float:
    """
    Calculate the angle between three points.

    :param p1: First point (x, y).
    :param p2: Second point (x, y).
    :param p3: Third point (x, y).

    :return: Angle in degrees.
    """

    def vector(p1, p2) -> np.ndarray:
        """
        Calculate the vector between two points.
        :param p1: First point (x, y).
        :param p2: Second point (x, y).

        :return: The vector.
        """
        return np.array([p2[0] - p1[0], p2[1] - p1[1]])

    v1 = vector(p2, p1)
    v2 = vector(p2, p3)

    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    angle = np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))

    return angle
