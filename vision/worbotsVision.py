import cv2
import numpy as np
from config import WorbotsConfig

class WorbotsVision:
    worConfig = None
    mtx = None
    dist = None
    rvecs = None
    tvecs = None

    allObjPoints = np.array([])
    allImgPoints = np.array([])

    def __init__(self, cameraNumber):
        self.cap = cv2.VideoCapture(cameraNumber)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 60)
        self.worConfig = WorbotsConfig()
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

            #Make sure there are charuco corners before trying to match
            objPoints = None
            if (charucoCorners is not None):
                (objPoints, imgPoints) = board.matchImagePoints(charucoCorners, charucoIds)

            #Keep adding to the total array of objPoints and imPoints
            if (objPoints is not None and imgPoints is not None and np.size(self.allImgPoints) == 0):
                self.allObjPoints = objPoints
                self.allImgPoints = imgPoints
            if (objPoints is not None and imgPoints is not None):
                self.allObjPoints = np.append(self.allObjPoints, objPoints, 0)
                self.allImgPoints = np.append(self.allImgPoints, imgPoints, 0)
                print(np.size(self.allImgPoints))

            #When a certain  threshold is reached, calibrate the camera, save the config, and exit
            if (np.size(self.allImgPoints) > 100000):
                ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera([self.allObjPoints], [self.allImgPoints], gray.shape[::-1], self.mtx, self.dist)
                self.worConfig.saveCameraIntrinsics(self.mtx, self.dist, self.rvecs, self.tvecs)
                break

            cv2.imshow("out",frameCopy)
            if (cv2.waitKey(1) & 0xFF == ord('q')):
                break
    
    def mainPnP(self):
        mtx, dist, rvecs, tvecs = self.worConfig.getCameraIntrinsicsFromJSON()
        axis_len = 0.1
        tag_size = 0.1524
        while True:
            ret, frame = self.cap.read()
            frameCopy = frame.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_16h5)
            detectorParams = cv2.aruco.DetectorParameters()
            (corners, ids, rejected) = cv2.aruco.detectMarkers(image=gray, dictionary=dictionary, parameters=detectorParams)

            if ids is not None and len(ids) > 0:
                obj_1 = [-tag_size/2, -tag_size/2, 0.0]
                obj_2 = [tag_size/2, -tag_size/2, 0.0]
                obj_3 = [tag_size/2, tag_size/2, 0.0]
                obj_4 = [-tag_size/2, tag_size/2, 0.0]
                obj_all = obj_1 + obj_2 + obj_3 + obj_4
                objPoints = np.array(obj_all).reshape(4,3)
                for i in range(len(ids)):
                    ye, rvecs, tvecs = cv2.solvePnP(objPoints, corners[i][0], mtx, dist)

                    img_points, _ = cv2.projectPoints(objPoints, rvecs, tvecs, mtx, dist)

                    frameCopy = cv2.drawFrameAxes(frameCopy, mtx, dist, rvecs, tvecs, axis_len)
                cv2.aruco.drawDetectedMarkers(frameCopy, corners, ids, (0, 0, 255))

            cv2.imshow("out", frameCopy)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


    def getCalibration(self) -> any:
        return (self.mtx, self.dist, self.rvecs, self.tvecs)
