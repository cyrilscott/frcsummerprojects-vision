from threading import Thread
import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open webcam")


class WorbotsVision:
    def openMain():
        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ret, buffer = cv2.imencode('.jpg', cv2.flip(gray, 1))
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def getAndProcessFrame():
        while True:
            ret, frame = cap.read()

    def getFrame():
        ret, frame = cap.read()
        return frame
