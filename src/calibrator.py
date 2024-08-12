import config
import cv2
import numpy as np


class Calibrator:
    def __init__(
        self,
    ):
        self.is_calibrated = False
        self.calibration_frames = 0
        self.calibration_shoulder_angles = []
        self.calibration_neck_angles = []
        self.shoulder_bounds = (0, 0)
        self.neck_bounds = (0, 0)

    def calibrate(self, image, shoulder_angle, neck_angle):
        """ "
        Calibrates the shoulder and neck angles for proper posture.

        :param shoulder_angle: The shoulder angle.
        :param neck_angle: The neck angle.

        :return: None
        """
        if (
            not self.is_calibrated
            and self.calibration_frames < config.CALIBRATION_FRAMES
        ):
            self.calibration_shoulder_angles.append(shoulder_angle)
            self.calibration_neck_angles.append(neck_angle)
            self.calibration_frames += 1

            cv2.putText(
                image,
                f"Calibrating... {self.calibration_frames}/{config.CALIBRATION_FRAMES}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2,
                cv2.LINE_AA,
            )

        elif not self.is_calibrated:
            avg_shoulder_angle = np.mean(self.calibration_shoulder_angles)
            avg_neck_angle = np.mean(self.calibration_neck_angles)

            # upper and lower bounds
            self.shoulder_bounds = (
                avg_shoulder_angle - config.SHOULDER_RANGE,
                avg_shoulder_angle + config.SHOULDER_RANGE,
            )
            self.neck_bounds = (
                avg_neck_angle - config.NECK_RANGE,
                avg_neck_angle + config.NECK_RANGE,
            )

            self.is_calibrated = True
            print(
                f"Calibration complete. Shoulder bounds: {self.shoulder_bounds[0]:.1f}-{self.shoulder_bounds[1]:.1f}, "
                f"Neck bounds: {self.neck_bounds[0]:.1f}-{self.neck_bounds[1]:.1f}"
            )

    def show_calibration_result(self, image):
        """
        Shows the calibration result.
        """
        cv2.putText(
            image,
            f"Shoulder bounds: {self.shoulder_bounds[0]:.1f}-{self.shoulder_bounds[1]:.1f}",
            (10, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 0),
            2,
            cv2.LINE_AA,
        )

        cv2.putText(
            image,
            f"Neck bounds: {self.neck_bounds[0]:.1f}-{self.neck_bounds[1]:.1f}",
            (10, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 0),
            2,
            cv2.LINE_AA,
        )
