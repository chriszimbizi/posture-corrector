import mediapipe as mp
from utils import get_landmark_coordinates


class PoseEstimator:
    def __init__(self):
        self.mp_pose = mp.solutions.pose  # pose estimation tools
        self.mp_drawing = mp.solutions.drawing_utils  # for visualization
        self.pose = self.mp_pose.Pose(  # pose estimation model
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            smooth_landmarks=True,
        )

    def estimate_pose(self, image):
        """
        :return: The pose of the image.
        """
        return self.pose.process(image)

    def extract_key_body_landmarks(self, image, landmarks) -> tuple:
        """
        Extract key body landmarks from the pose results.

        :param image: The image to draw on.
        :param landmarks: List of Pose landmarks.

        :return: Tuple of (left_shoulder, right_shoulder, left_ear).
        """
        left_shoulder = get_landmark_coordinates(
            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value], image.shape
        )
        right_shoulder = get_landmark_coordinates(
            landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value], image.shape
        )
        left_ear = get_landmark_coordinates(
            landmarks[self.mp_pose.PoseLandmark.LEFT_EAR.value], image.shape
        )

        return left_shoulder, right_shoulder, left_ear

    def draw_landmarks(self, image, pose_landmarks):
        """
        Draws landmarks and connections on the image.

        :param image: The image to draw on.
        :param pose_landmarks: The landmarks to draw (list of PoseLandmark objects - landmarks, connections).

        :return: None
        """
        self.mp_drawing.draw_landmarks(
            image,
            pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS,
        )
