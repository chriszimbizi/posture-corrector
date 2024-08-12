import cv2


class VideoProcessor:
    def __init__(self):
        self.cap = cv2.VideoCapture(1)  # 0 for default webcam

    def get_frame(self):
        """
        :return: The frame and whether it was successfully retrieved
        """
        ret, frame = self.cap.read()
        return ret, frame

    def release(self):
        """
        Release the video capture.
        """
        self.cap.release()

    def show_frame(self, frame):
        """
        Show the frame.

        :param frame: The frame to show.

        :return: Whether the frame was successfully shown.
        """
        cv2.imshow("Posture Corrector", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            self.release()
            cv2.destroyAllWindows()
            return False
        return True
