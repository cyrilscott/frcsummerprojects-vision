import threading
import json
from vision import WorbotsVision
from network import WorbotsTables
from config import WorbotsConfig

def main():
    config = WorbotsConfig()
    vision = WorbotsVision(0)
    vision.calibrateCameraImages("./images")
    # while True:
    #     vision.mainPnP()
        # vision.checkCalib()

if __name__ == '__main__':
    main()