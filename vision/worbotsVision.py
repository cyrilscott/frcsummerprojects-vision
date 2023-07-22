from threading import Thread
import cv2

index = 0
for i in range(-1, 50):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        index = i
    cap.release()
print(index)
cap = cv2.VideoCapture(index)


class WorbotsVision:
    def openMain():
        index = 0
        for i in range(50):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                index = i
        print(index)
        while True:
            cap = cv2.VideoCapture(index)
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
