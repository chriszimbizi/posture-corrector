# system imports
import os
import time

# local imports
from utils import get_landmark_coordinates, draw_angle, calculate_angle

# third party imports
import cv2
import numpy as np
import mediapipe as mp

# from playsound import playsound

# mediapipe initialization
mp_pose = mp.solutions.pose  # pose estimation tools
mp_drawing = mp.solutions.drawing_utils  # for visualizing landmarks
pose = mp_pose.Pose(  # pose estimation model
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    smooth_landmarks=True,
)

# parameters
calibration_frames = 0
calibration_shoulder_angles = []
calibration_neck_angles = []
is_calibrated = False
shoulder_range = 10
neck_range = 10
last_alert_time = 0
alert_cooldown = 5  # in seconds
sound_file = os.path.join(os.path.dirname(__file__), "../sounds/alert.mp3")

# start video capture
cap = cv2.VideoCapture(1)  # 0 for default webcam

while cap.isOpened():
    ret, frame = (
        cap.read()
    )  # read the webcam frame, returns boolean (success/failure) and frame

    frame_height, frame_width = frame.shape[:2]

    if not ret:
        break

    # convert the frame color from BGR to RG for mediapipe
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False  # make the frame immutable to optimize performance

    results = pose.process(image)  # process the frame

    # convert the frame color from RGB back to BGR for opencv
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        landmarks = (
            results.pose_landmarks.landmark
        )  # list of Landmark objects (contains x,y coordinates normalized to range [0,1])
        print(landmarks)

        # extract key body landmarks
        left_shoulder = get_landmark_coordinates(
            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value], image.shape
        )
        right_shoulder = get_landmark_coordinates(
            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value], image.shape
        )
        left_ear = get_landmark_coordinates(
            landmarks[mp_pose.PoseLandmark.LEFT_EAR.value], image.shape
        )
        right_ear = get_landmark_coordinates(
            landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value], image.shape
        )

        # === angle calculation === #
        shoulder_angle = calculate_angle(
            left_shoulder, right_shoulder, (right_shoulder[0], 0)
        )
        neck_angle = calculate_angle(left_ear, left_shoulder, (left_shoulder[0], 0))

        # === calibration === #
        if not is_calibrated and calibration_frames < 30:
            calibration_shoulder_angles.append(shoulder_angle)
            calibration_neck_angles.append(neck_angle)
            calibration_frames += 1

            cv2.putText(
                image,  # image to draw on
                f"Calibrating... {calibration_frames}/30",  # text to draw
                (10, 30),  # position of the text
                cv2.FONT_HERSHEY_SIMPLEX,  # font
                1,  # font scale
                (0, 255, 255),  # color in BGR
                2,  # thickness
                cv2.LINE_AA,  # line type
            )
        elif not is_calibrated:
            avg_shoulder_angle = np.mean(calibration_shoulder_angles)
            avg_neck_angle = np.mean(calibration_neck_angles)

            # upper and lower bounds
            shoulder_lower_bound = avg_shoulder_angle - shoulder_range
            shoulder_upper_bound = avg_shoulder_angle + shoulder_range
            neck_lower_bound = avg_neck_angle - neck_range
            neck_upper_bound = avg_neck_angle + neck_range

            is_calibrated = True
            print(
                f"Calibration complete. Shoulder bounds: {shoulder_lower_bound:.1f}-{shoulder_upper_bound:.1f}, "
                f"Neck bounds: {neck_lower_bound:.1f}-{neck_upper_bound:.1f}"
            )

        # draw skeleton and angles
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
        )
        midpoint = (
            (left_shoulder[0] + right_shoulder[0]) // 2,
            (left_shoulder[1] + right_shoulder[1]) // 2,
        )
        # shoulder angle
        draw_angle(
            image,
            left_shoulder,
            right_shoulder,
            (right_shoulder[0], 0),
            shoulder_angle,
            (255, 0, 0),
        )

        # neck angle
        draw_angle(
            image,
            left_ear,
            left_shoulder,
            (left_shoulder[0], 0),
            neck_angle,
            (0, 255, 0),
        )

        # === feedback === #
        if is_calibrated:
            current_time = time.time()
            if not (
                shoulder_lower_bound <= shoulder_angle <= shoulder_upper_bound
            ) or not (neck_lower_bound <= neck_angle <= neck_upper_bound):
                status = "Poor Posture"  # red
                if current_time - last_alert_time > alert_cooldown:
                    print("Poor posture detected! Please sit up straight.")
                    # if os.path.exists(sound_file):
                    # playsound(sound_file)
                    last_alert_time = current_time
            else:
                status = "Good Posture"  # green

            # status text
            cv2.putText(
                image,
                status,
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 255, 0) if status == "Good Posture" else (0, 0, 255),
                3,
                cv2.LINE_AA,
            )

            # shoulder angle text
            cv2.putText(
                image,
                f"Shoulder Angle: {shoulder_angle:.1f} (Bounds: {shoulder_lower_bound:.1f} - {shoulder_upper_bound:.1f})",
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 0),
                2,
                cv2.LINE_AA,
            )

            # neck angle text
            cv2.putText(
                image,
                f"Neck Angle: {neck_angle:.1f} (Bounds: {neck_lower_bound:.1f} - {neck_upper_bound:.1f})",
                (10, 150),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 0),
                2,
                cv2.LINE_AA,
            )

    # show the frame with angles and text
    cv2.imshow("Posture Corrector", image)

    if cv2.waitKey(1) & 0xFF == ord("q"):  # if q is pressed, break
        break

cap.release()  # release the webcam
cv2.destroyAllWindows()  # destroy all the windows opened by `cv2.imshow()`
