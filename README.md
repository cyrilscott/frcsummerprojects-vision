# frcsummerprojects-vision

Vision projects for the 2023-2024 summer.

Dependencies:
- OpenCV `pip install opencv-contrib-python`
- Flask `pip install flask`

Installation:  
- Use `pip install -r requirements.txt` to automatically install all of the dependencies above.

Description:  
This code uses OpenCV's built in ArUco library for detecting AprilTags. This was chosen over other libraries due to its flexibility and customization abilities.  
The board.jpg is the ChArUco board that is used to calibrate the camera. The Checker width is 24mm, and the Marker width is 19mm. This is crucial to the calibration of the camera. It is also crucial to keep it flat while calibrating.