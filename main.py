import threading
import json
from vision import WorbotsVision
from network import WorbotsTables
from config import WorbotsConfig

def main():
    config = WorbotsConfig()

    while True:
        vision = WorbotsVision(0)
        # vision.openCharuco()
        vision.mainPnP()

if __name__ == "__main__":
    main()
