import threading
import json
import time
import cv2
from wpimath.geometry import *
from vision import WorbotsVision, PoseCalculator
from network import WorbotsTables
from config import WorbotsConfig

def main():
    config = WorbotsConfig()
    network = WorbotsTables()
    vision = WorbotsVision()
    calc = PoseCalculator()
    print(f"Optimized used?: {cv2.useOptimized}")
    # vision.calibrateCameraImages("./images")
    # vision.calibrateCamLive()

    while True:
        start = time.time()
        # frame, tvec, rvec = vision.mainPnPSingleFrame()
        # vision.mainPnP()

        frame, poseDetection = vision.processFrame()
        network.sendPoseDetection(poseDetection)
        
        cv2.imshow("out", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print(f"FPS: {1 / (time.time() - start)}")

if __name__ == '__main__':
    main()
