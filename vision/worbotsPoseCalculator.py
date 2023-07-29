import numpy as np
import cv2
import tensorflow_graphics.geometry.transformation as tfg
from config import WorbotsConfig
from wpimath.geometry import *
from robotpy_apriltag import *

class PoseCalculator:
    config = WorbotsConfig()
    aprilTagLayout = AprilTagFieldLayout("2023-chargedup.json")

    def getWpifromOpenCV(tvec, rvec) -> Pose3d:
        return Pose3d(tvec[0], tvec[1], tvec[2], Rotation3d(rvec))
    
    def getPosefromTag(self, id, tvec, rvec) -> Pose3d:
        camToTag = np.array([[0, 0, 0, tvec[0][0]],
                            [0, 0, 0, tvec[1][0]],
                            [0, 0, 0, tvec[2][0]],
                            [0, 0, 0, 1]], dtype=float)
        camToTag[:3, :3], _ = cv2.Rodrigues(rvec)
        tagToWorld = self.getTMatrixFromID(1)
        camToRobot = self.getCameraToRobotMatrix()
        finalPose = np.matmul(np.matmul(tagToWorld, np.linalg.inv(camToTag)), camToRobot)
        return self.pose3dFromMatrix(finalPose)

    def pose3dFromMatrix(self, matrix) -> Pose3d:
        euler = tfg.euler.from_rotation_matrix(matrix[:3, :3])
        return Pose3d(matrix[0,3], matrix[1,3], matrix[2,3], Rotation3d(np.array([[euler[0].numpy()], [euler[1].numpy()], [euler[2].numpy()]])))
        
    
    def getTMatrixFromID(self, id) -> np.array:
        pose = self.aprilTagLayout.getTagPose(id)
        rotation = pose.rotation()
        tvec = np.array([[pose.x], [pose.y], [pose.z]])
        rvec = np.array([[rotation.x], [rotation.y], [rotation.z]])

        return self.RvecTvecToMatrix(rvec, tvec)

    def RvecTvecToMatrix(self, rvec, tvec) -> np.array:
        matrix = np.array([[0, 0, 0, tvec[0][0]],
                            [0, 0, 0, tvec[1][0]],
                            [0, 0, 0, tvec[2][0]],
                            [0, 0, 0, 1]], dtype=float)
        matrix[:3, :3], _ = cv2.Rodrigues(rvec)
        return matrix

    def getCameraToRobotMatrix(self) -> np.array:
        tvec = np.array([[self.config.CAM_TO_ROBOT_X], [self.config.CAM_TO_ROBOT_Y], [self.config.CAM_TO_ROBOT_Z]])
        rvec = np.array([[np.deg2rad(self.config.CAM_TO_ROBOT_ROLL)], [np.deg2rad(self.config.CAM_TO_ROBOT_PITCH)], [np.deg2rad(self.config.CAM_TO_ROBOT_YAW)]])
        return self.RvecTvecToMatrix(rvec, tvec)