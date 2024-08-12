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

## Usage

1. Run the application:

   ```bash
   python src/main.py
   ```

2. Calibration: The application will automatically calibrate for the first 30 frames.

3. Real-Time Feedback: The application will monitor your posture and provide real-time feedback through visual cues and sound alerts if poor posture is detected.

### Camera Index Configuration

In the current implementation, the `VideoProcessor` class in `video_processor.py` initializes the camera with index 1. This is done because index 0 defaults to connecting to the iPhone via Continuity Camera. If this is not the case for you, you should set the camera index to 0 to use your default camera.

#### To Configure the Camera Index:

1. Initialize the VideoCapture object with the desired camera index:

   `0` - Connects to the default camera on your system (usually the webcam, but can be a USB camera or other video source, in my case, the iPhone).

   `1` - Connects to the secondary camera on your system (in my case, the MacBook's built-in camera).

   ```python
   self.capture = cv2.VideoCapture(0)
   ```

## Performance Considerations

In the current implementation, the code responsible for playing a sound when poor posture is detected is commented out due to performance issues. Specifically, enabling this feature can cause the application to freeze momentarily whenever poor posture is detected.

**If you wish to enable sound notifications**:

- Simply uncomment the relevant code in the `feedback_manager.py` file. However, please be aware that this may introduce noticeable lag in the application's performance.

### Profiling and Optimizing the Code

To help you understand and potentially improve the performance of this application, you can profile the code to identify bottlenecks.

#### Steps to Profile the Code:

1. **Import the Profiler:**

   Add the following lines at the beginning of your script to enable profiling:

   ```python
   import cProfile
   import pstats
   ```

2. **Profile the Main Function:**

   Wrap the `main()` function call with the profiler:

   ```python
   if __name__ == "__main__":
       profiler = cProfile.Profile()
       profiler.enable()

       main()

       profiler.disable()
       stats = pstats.Stats(profiler).sort_stats('cumtime')
       stats.print_stats(10)  # Print the 10 most time-consuming functions
   ```

3. **Run the Script:**

   Execute your script as usual. The profiler will output a list of functions and the time spent in each.

4. **Analyze the Output:**

   Look for functions with the highest cumulative time (`cumtime`). These are the areas where your code spends most of its time and may be the best targets for optimization.
