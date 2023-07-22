from flask import Flask, render_template, Response, request, current_app
import numpy as np
import cv2
from vision import WorbotsVision

app = Flask("VisionServer")

mtx = None
dist = None

class VisionServer:
    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/video')
    def video():
        return Response(openCharuco(), mimetype='multipart/x-mixed-replace; boundary=frame')

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

def openCharuco():
    while True:
        frame = WorbotsVision.getFrame()
        frameCopy = WorbotsVision.getFrame()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
        board = cv2.aruco.CharucoBoard((11,8), 0.024, 0.019, dictionary)

        (corners, ids, rejected) = cv2.aruco.detectMarkers(gray, dictionary)
        cv2.aruco.drawDetectedMarkers(frameCopy, corners, ids)

        charucoParams = cv2.aruco.CharucoParameters()
        detectorParams = cv2.aruco.DetectorParameters()

        detector = cv2.aruco.CharucoDetector(board=board, charucoParams=charucoParams, detectorParams=detectorParams)

        (charucoCorners, charucoIds, markerCorns, markerIds) = detector.detectBoard(gray)
        cv2.aruco.drawDetectedCornersCharuco(frameCopy, charucoCorners, charucoIds, (0, 0, 255))

        if(charucoCorners is not None):
            (objPoints, imgPoints) = board.matchImagePoints(charucoCorners, charucoIds)
            objHeight, objWidth = objPoints.shape[:2]
            imgHeight, imgWidth = imgPoints.shape[:2]
            if (objPoints is not None and imgPoints is not None and objWidth > 5 and imgWidth > 5):
                ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objPoints, imgPoints, gray.shape[::-1], None, None)

        ret, buffer = cv2.imencode('.jpg', frameCopy)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def getCameraMatrix():
    return mtx

def getDistMatrix():
    return dist