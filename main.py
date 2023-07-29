import threading
import json
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
    # vision.calibrateCameraImages("./images")

    while True:
        # frame, tvec, rvec = vision.mainPnPSingleFrame()
        # vision.mainPnP()

        vision.processFrame()
        
        # cv2.imshow("out", frame)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

if __name__ == '__main__':
    main()
