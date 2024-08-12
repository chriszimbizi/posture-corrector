import os

CALIBRATION_FRAMES = 30
SHOULDER_RANGE = 10
NECK_RANGE = 10
ALERT_COOLDOWN = 5  # in seconds
SOUND_FILE = os.path.join(os.path.dirname(__file__), "../sounds/alert.wav")
