from web import VisionServer
import threading

def main():
    # dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
    # board = cv2.aruco.CharucoBoard((11,8), 0.024, 0.019, dictionary)
    # image = board.generateImage((3300, 2550))
    # cv2.imwrite("board.jpg", image)


    server = VisionServer()
    server.runServer()


if __name__ == "__main__":
    main()
