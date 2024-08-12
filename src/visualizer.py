import cv2
import numpy as np


class Visualizer:

    def __init__(self):
        pass

    def draw_angle(self, image, p1, p2, p3, angle, color) -> None:
        """
        Draw an angle indicator on the image.

        :param image: The image to draw on.
        :param p1: First point (x, y).
        :param p2: Second point (x, y) - vertex of the angle.
        :param p3: Third point (x, y).
        :param angle: The angle to display.
        :param color: Color for the angle lines.

        :return: None
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
        text_position = p2 + (
            50 * bisector
        )  # 50 pixels away from p2 along the bisector

        # Ensure the text_position is a tuple of integers
        text_position = tuple(text_position.astype(int))

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
