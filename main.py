import threading
import json
from vision import WorbotsVision
from network import WorbotsTables
from config import WorbotsConfig

def main():
    config = WorbotsConfig()
    network = WorbotsTables()
    vision = WorbotsVision()
    # vision.calibrateCameraImages("./images")

    while True:
        frame, tvec, rvec = vision.mainPnP()

        # vision.checkCalib()

if __name__ == '__main__':
    main()
