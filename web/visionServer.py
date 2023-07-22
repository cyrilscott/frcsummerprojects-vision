from flask import Flask, render_template, Response, request, current_app
import cv2
from vision import WorbotsVision

app = Flask("VisionServer")


class VisionServer:
    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/video')
    def video():
        return Response(openMain(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def runServer(self):
        app.run(debug=True, host='0.0.0.0', port=80)


def openMain():
    while True:
        frame = WorbotsVision.getFrame()
        frameCopy = WorbotsVision.getFrame()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_16h5)
        detectorParams = cv2.aruco.DetectorParameters()
        (corners, ids, rejected) = cv2.aruco.detectMarkers(image=gray, dictionary=dictionary, parameters=detectorParams)

        cv2.aruco.drawDetectedMarkers(image=frameCopy, corners=corners, ids=ids)

        ret, buffer = cv2.imencode('.jpg', cv2.flip(frameCopy, 1))
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
