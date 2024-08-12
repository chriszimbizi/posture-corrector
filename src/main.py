# local imports
import config
from calibrator import Calibrator
from feedback_manager import FeedbackManager
from pose_estimator import PoseEstimator
from utils import calculate_angle
from video_processor import VideoProcessor
from visualizer import Visualizer

# third party imports
import cv2


def main():
    video_processor = VideoProcessor()
    pose_estimator = PoseEstimator()
    calibrator = Calibrator()
    feedback_manager = FeedbackManager()
    visualizer = Visualizer()

    while True:
        success, image = video_processor.get_frame()
        if not success:
            break  # if the webcam is not available, break the loop

        # convert the frame color from BGR to RGB for mediapipe
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = (
            False  # make the frame immutable to optimize performance
        )

        # process the frame
        results = pose_estimator.estimate_pose(image_rgb)

        if results.pose_landmarks:
            pose_estimator.draw_landmarks(image, results.pose_landmarks)

            landmarks = (
                results.pose_landmarks.landmark
            )  # list of Landmark objects (contains x,y coordinates normalized to range [0,1])

            # === angle calculation === #
            left_shoulder, right_shoulder, left_ear = (
                pose_estimator.extract_key_body_landmarks(image, landmarks)
            )
            shoulder_angle = calculate_angle(
                left_shoulder, right_shoulder, (right_shoulder[0], 0)
            )
            neck_angle = calculate_angle(left_ear, left_shoulder, (left_shoulder[0], 0))

            # === calibration === #
            calibrator.calibrate(image, shoulder_angle, neck_angle)

            # === feedback === #
            if calibrator.is_calibrated:
                calibrator.show_calibration_result(image)

                status = feedback_manager.get_status(
                    shoulder_angle,
                    neck_angle,
                    calibrator.shoulder_bounds,
                    calibrator.neck_bounds,
                )
                feedback_manager.provide_feedback(image, status)

            # === visualization === #

            # shoulder angle
            visualizer.draw_angle(
                image,
                left_shoulder,
                right_shoulder,
                (right_shoulder[0], 0),
                shoulder_angle,
                (255, 0, 0),
            )

            # neck angle
            visualizer.draw_angle(
                image,
                left_ear,
                left_shoulder,
                (left_shoulder[0], 0),
                neck_angle,
                (0, 255, 0),
            )

        if not video_processor.show_frame(image):
            break


if __name__ == "__main__":
    main()
