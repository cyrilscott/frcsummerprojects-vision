import numpy as np
import cv2
import tensorflow as tf
from wpimath.geometry import *
from robotpy_apriltag import *

class PoseCalculator:
    aprilTagLayout = AprilTagFieldLayout("2023-chargedup.json")
    aprilTagLayout.setOrigin(Pose3d(0, 0, 0, Rotation3d(np.array([[0], [0], [0]]))))

    def getWpifromOpenCV(tvec, rvec) -> Pose3d:
        return Pose3d(tvec[0], tvec[1], tvec[2], Rotation3d(rvec))
    
    def getPosefromTag(self, id, tvec, rvec) -> Pose3d:
        camToTag = np.array([[0, 0, 0, tvec[0][0]],
                            [0, 0, 0, tvec[1][0]],
                            [0, 0, 0, tvec[2][0]],
                            [0, 0, 0, 1]], dtype=float)
        camToTag[:3, :3], _ = cv2.Rodrigues(rvec)
        tagToWorld = self.getTMatrixFromID(1)
        print(tagToWorld)
    
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