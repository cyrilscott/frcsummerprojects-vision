import cv2
import numpy as np
from config import WorbotsConfig
import os

class WorbotsVision:
    worConfig = None
    mtx = None
    dist = None
    rvecs = None
    tvecs = None

    def __init__(self):
        self.worConfig = WorbotsConfig()
        self.cap = cv2.VideoCapture(self.worConfig.CAMERA_ID)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.worConfig.RES_W)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.worConfig.RES_H)
        self.cap.set(cv2.CAP_PROP_FPS, self.worConfig.CAM_FPS)
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

    def calibrateCameraImages(self, folderName):
        images = os.listdir(folderName)

        # Define the board
        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
        board = cv2.aruco.CharucoBoard((11, 8), 0.024, 0.019, dictionary)

        allCharucoCorners: List[np.ndarray] = []
        allCharucoIds: List[np.ndarray] = []

        for fname in images:
            img = cv2.imread(os.path.join(folderName, fname))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
            # Detect corners as well as markers
            charucoParams = cv2.aruco.CharucoParameters()
            detectorParams = cv2.aruco.DetectorParameters()
            detector = cv2.aruco.CharucoDetector(board, charucoParams, detectorParams)
            (charucoCorners, charucoIds, markerCorners, markerIds) = detector.detectBoard(gray)

            if charucoCorners is not None and charucoIds is not None:
                if len(charucoCorners) == len(charucoIds):
                    allCharucoCorners.append(charucoCorners)
                    allCharucoIds.append(charucoIds)

        if len(allCharucoCorners) > 0:
            # Combine allCharucoCorners and allCharucoIds into single arrays

            ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.aruco.calibrateCameraCharuco(
                allCharucoCorners, allCharucoIds, board, gray.shape[::-1], None, None
            )
            self.worConfig.saveCameraIntrinsics(self.mtx, self.dist, self.rvecs, self.tvecs)
            print(ret)
        else:
            print("No Charuco corners were detected for calibration.")

        
    
    def mainPnP(self):
        mtx, dist, rvecs, tvecs = self.worConfig.getCameraIntrinsicsFromJSON()
        axis_len = 0.1
        tag_size = self.worConfig.TAG_SIZE_METERS
        while True:
            ret, frame = self.cap.read()
            frameCopy = frame.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_16h5)
            detectorParams = cv2.aruco.DetectorParameters()
            (corners, ids, rejected) = cv2.aruco.detectMarkers(image=gray, dictionary=dictionary, parameters=detectorParams)

            if ids is not None and len(ids) > 0:
                obj_1 = [-tag_size/2, tag_size/2, 0.0]
                obj_2 = [tag_size/2, tag_size/2, 0.0]
                obj_3 = [tag_size/2, -tag_size/2, 0.0]
                obj_4 = [-tag_size/2, -tag_size/2, 0.0]
                obj_all = obj_1 + obj_2 + obj_3 + obj_4
                objPoints = np.array(obj_all).reshape(4,3)
                for i in range(len(ids)):
                    ret, rvec, tvec = cv2.solvePnP(objPoints, corners[i], mtx, dist, flags=cv2.SOLVEPNP_IPPE_SQUARE)
                    print(tvec)
                    print(rvec)

                    frameCopy = cv2.drawFrameAxes(frameCopy, mtx, dist, rvec, tvec, axis_len)
                cv2.aruco.drawDetectedMarkers(frameCopy, corners, ids, (0, 0, 255))

            cv2.imshow("out", frameCopy)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


    def getCalibration(self) -> any:
        return (self.mtx, self.dist, self.rvecs, self.tvecs)

    def checkCalib(self):
        mtx, dist, rvecs, tvecs = self.worConfig.getCameraIntrinsicsFromJSON()
        while True:
            ret, frame = self.cap.read()
            cv2.undistort(frame, mtx, dist, None)

            cv2.imshow("out", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

