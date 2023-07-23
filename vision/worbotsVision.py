import threading
import cv2
from imutils.video import VideoStream
import time

class WorbotsVision:
    mtx = None
    dist = None
    outputFrame = None
    lock = threading.Lock()

    def __init__(self, cameraNumber):
        self.cap = cv2.VideoCapture(cameraNumber, cv2.CAP_ANY)
        time.sleep(2.0)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        # self.cap.set(cv2.CAP_PROP_FPS, 60)

    def openNewCam(self, num):
        self.cap.release()
        self.cap = None
        self.cap = cv2.VideoCapture(num, cv2.CAP_ANY)
        time.sleep(2.0)
        while not self.cap.isOpened():
            self.cap.grab()

    def mainFunc(self):
        while True:
            with self.lock:
                if self.outputFrame is None:
                    continue
                (flag, encodedImage) = cv2.imencode(".jpg", self.outputFrame)
                if not flag:
                    continue
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

    def setCamResolution(self, width, height):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def openMain(self):
        while True:
            ret, frame = self.cap.read()
            frameCopy = frame.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_16h5)
            detectorParams = cv2.aruco.DetectorParameters()
            (corners, ids, rejected) = cv2.aruco.detectMarkers(image=gray, dictionary=dictionary, parameters=detectorParams)
            cv2.aruco.drawDetectedMarkers(image=frameCopy, corners=corners, ids=ids)
            with self.lock:
                outputFrame = frameCopy.copy()

    def openCharuco(self):
        while True:
            ret, frame = self.cap.read()
            frameCopy = frame.copy()
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
                if (objPoints is not None and imgPoints is not None and objWidth > 8 and imgWidth > 8):
                    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objPoints, imgPoints, gray.shape[::-1], None, None)
            with self.lock:
                outputFrame = frameCopy.copy()

        def getCameraMatrix(self):
            return self.mtx

        def getDistMatrix(self):
            return self.dist
