import threading
import json
from vision import WorbotsVision
from network import WorbotsTables
from config import WorbotsConfig

def main():
    # vision = WorbotsVision(0)
    # vision.openCharuco()

    config = WorbotsConfig()

    network = WorbotsTables("127.0.0.1")
    network.sendNumber()


if __name__ == "__main__":
    main()
