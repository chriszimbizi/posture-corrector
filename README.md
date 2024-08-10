# Posture Corrector

Posture Corrector is a Python application designed to help monitor and correct poor posture using real-time webcam feed analysis. This project demonstrates proficiency in computer vision, real-time processing, and user feedback mechanisms.

## Project Overview

"Posture Corrector" is an interactive tool that tracks shoulder and neck angles using a webcam feed to detect and correct poor posture. The core functionality is powered by the `mediapipe` library, and the application provides real-time feedback, including visual alerts and sound notifications.

## Technologies Used

- **Python**: The programming language used to build the application.
- **OpenCV**: For real-time video capture and processing.
- **Mediapipe**: Leveraged for pose detection and landmark tracking.
- **Numpy**: Used for numerical computations.
- **Playsound**: Used to play alert sounds when poor posture is detected.

## Project Structure

- **main.py**: Entry point of the application that captures the webcam feed, processes the frames to calculate angles, and provides real-time feedback.
- **utils.py**: Contains utility functions for extracting landmark coordinates, calculating angles, and drawing angles on frames.
- **sounds/alert.wav**: Sound file used for audio notifications.

## Setup

### Prerequisites

- Python 3.12 or later
- Virtual environment (venv)
- OpenCV
- Mediapipe
- Playsound

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Ensure the sound file is in the correct location:

   Place the `alert.wav` sound file in the `sounds` directory.

### Usage

1. Run the application:

   ```bash
   python src/main.py
   ```

2. Calibration: The application will automatically calibrate for the first 30 frames.

3. Real-Time Feedback: The application will monitor your posture and provide real-time feedback through visual cues and sound alerts if poor posture is detected.
