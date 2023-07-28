import numpy as np
from wpimath.geometry import *
from robotpy_apriltag import *

class PoseCalculator:
    def getPose3dfromOpenCV(tvec, rvec) -> Pose3d:
        # print(AprilTagFieldLayout("2023-chargedup.json").getTagPose(4))
        return Pose3d(tvec[0], tvec[1], tvec[2], Rotation3d(rvec))
    
    
        