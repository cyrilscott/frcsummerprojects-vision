import threading
from vision import WorbotsVision

def main():
    vision = WorbotsVision(0)
    vision.openCharuco()


if __name__ == "__main__":
    main()
