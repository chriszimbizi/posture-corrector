# system imports
import time
import os
import config

# third party imports
import cv2
import simpleaudio as sa


class FeedbackManager:
    def __init__(self):
        self.last_alert_time = 0
        self.sound = None  # Store the sound object for playback
        self.alert_start_time = None  # To track when the alert process starts

        # Load the sound file if it exists
        if os.path.exists(config.SOUND_FILE):
            self.sound = sa.WaveObject.from_wave_file(config.SOUND_FILE)

    def get_status(self, shoulder_angle, neck_angle, shoulder_bounds, neck_bounds):
        """
        Gets the status message based on the shoulder and neck angles.

        :param shoulder_angle: The shoulder angle in degrees.
        :param neck_angle: The neck angle in degrees.
        :param shoulder_bounds: The shoulder bounds in degrees.
        :param neck_bounds: The neck bounds in degrees.

        :return: The status message as a string.
        """
        current_time = time.time()
        if not (shoulder_bounds[0] <= shoulder_angle <= shoulder_bounds[1]) or not (
            neck_bounds[0] <= neck_angle <= neck_bounds[1]
        ):
            if current_time - self.last_alert_time > config.ALERT_COOLDOWN:
                print("Poor posture detected! Please sit up straight.")

                # Start timing the alert delivery process
                self.alert_start_time = time.time()

                if self.sound:
                    self.sound.play()  # Play the sound using simpleaudio

                # Calculate the time taken to deliver the alert
                alert_delivery_time = time.time() - self.alert_start_time
                print(f"Alert delivery time: {alert_delivery_time * 1000:.2f} ms")

                self.last_alert_time = current_time
            return "Poor Posture"
        return "Good Posture"  # green

    def provide_feedback(self, image, status):
        """
        Provides feedback based on the shoulder and neck angles.

        :param image: The image to draw on.
        :param status: The status message.

        :return: None
        """
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
