import cv2
import numpy as np
import mediapipe as mp


def get_landmark_coordinates(landmark, frame_shape: tuple) -> tuple:
    """
    Convert normalized landmark coordinates to pixel coordinates.

    :param landmark: Landmark object with x and y attributes.
    :param frame_shape: Shape of the frame (height, width).
    :return: Tuple of (x, y) coordinates in pixels.
    """
    return (int(landmark.x * frame_shape[1]), int(landmark.y * frame_shape[0]))


def calculate_angle(p1, p2, p3):
    """
    Calculate the angle between three points.

    :param p1: First point (x, y).
    :param p2: Second point (x, y).
    :param p3: Third point (x, y).
    :return: Angle in degrees.
    """

    def vector(p1, p2):
        return np.array([p2[0] - p1[0], p2[1] - p1[1]])

    v1 = vector(p2, p1)
    v2 = vector(p2, p3)

    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    angle = np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))

    return angle


def draw_angle(image, p1, p2, p3, angle, color):
    """
    Draw an angle indicator on the image.

    :param image: The image to draw on.
    :param p1: First point (x, y).
    :param p2: Second point (x, y) - vertex of the angle.
    :param p3: Third point (x, y).
    :param angle: The angle to display.
    :param color: Color for the angle lines.
    """
    cv2.line(image, p1, p2, color, 2)
    cv2.line(image, p2, p3, color, 2)

    # calculate direction vectors for p1 -> p2 and p3 -> p2
    v1 = np.array(p1) - np.array(p2)
    v2 = np.array(p3) - np.array(p2)

    # normalize the vectors to get the bisector
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    bisector = v1 + v2

    # place the angle text along the bisector
    text_position = p2 + (50 * bisector)  # 50 pixels away from p2 along the bisector

    # Ensure the text_position is a tuple of integers
    text_position = tuple(text_position.astype(int))

    midpoint = (int((p1[0] + p2[0]) * 4), int((p1[1] + p3[1]) * 4))
    cv2.putText(
        image,
        f"{angle:.1f}",
        text_position,
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        3,
        cv2.LINE_AA,
    )
