import threading
from vision import WorbotsVision

def main():
    vision = WorbotsVision(0)
    vision.openMain()


if __name__ == "__main__":
    main()
