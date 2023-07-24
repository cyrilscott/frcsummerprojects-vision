import threading
import cv2
import numpy as np
from imutils.video import VideoStream
import time

class WorbotsVision:
    mtx = None
    dist = None

    allCharucoCorners = np.array([])
    allCharucoIds = np.array([])

    def __init__(self, cameraNumber):
        self.cap = cv2.VideoCapture(cameraNumber)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 60)
        print("done init")

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
            cv2.imshow("out",frameCopy)
            if (cv2.waitKey(1) & 0xFF == ord('q')):
                break

    def openCharuco(self):
        while True:
            ret, frame = self.cap.read()
            frameCopy = frame.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            #Define the board
            dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
            board = cv2.aruco.CharucoBoard((11,8), 0.024, 0.019, dictionary)

            #Detect corners as well as markers
            charucoParams = cv2.aruco.CharucoParameters()
            detectorParams = cv2.aruco.DetectorParameters()
            detector = cv2.aruco.CharucoDetector(board=board, charucoParams=charucoParams, detectorParams=detectorParams)
            (charucoCorners, charucoIds, markerCorners, markerIds) = detector.detectBoard(gray)

            #Draw the corners and markers
            cv2.aruco.drawDetectedCornersCharuco(frameCopy, charucoCorners, charucoIds, (0, 0, 255))
            cv2.aruco.drawDetectedMarkers(frameCopy, markerCorners, markerIds, (0, 255, 0))

            if (np.size(self.allCharucoCorners) == 0):
                self.allCharucoCorners = charucoCorners
                self.allCharucoIds = charucoIds 
            # else:
            #     self.allCharucoCorners = np.append(self.allCharucoCorners, charucoCorners, 0)
            #     self.allCharucoIds = np.append(self.allCharucoIds, charucoIds, 0)
            
            # while (self.allImagePoints):
            #     if(charucoCorners is not None):
            #         (objPoints, imgPoints) = board.matchImagePoints(charucoCorners, charucoIds)

            # if (objPoints is not None and imgPoints is not None):
            #     ret, self.mtx, self.dist, rvecs, tvecs = cv2.calibrateCamera([objPoints], [imgPoints], gray.shape[::-1], self.mtx, self.dist)
            # if(np.size(self.allCharucoIds) >200):
            #     ret, self.mtx, self.dist, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(self.allCharucoCorners, self.allCharucoIds, board, gray.shape[::1], self.mtx, self.dist)
            #     print(self.mtx)

            cv2.imshow("out",frameCopy)
            if (cv2.waitKey(1) & 0xFF == ord('q')):
                break

        def getCameraMatrix(self):
            return self.mtx

        def getDistMatrix(self):
            return self.dist
