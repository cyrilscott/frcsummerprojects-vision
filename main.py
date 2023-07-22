from flask import Flask, render_template, Response, request
from vision import WorbotsVision
import numpy as np
from web import VisionServer
from threading import Thread
import cv2


def main():
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
    board = cv2.aruco.CharucoBoard((11,8), 0.024, 0.019, dictionary)
    image = board.generateImage((640*3, 480*3))
    cv2.imwrite("board.jpg", image)
    # cv2.aruco.CharucoBoard.generateImage(outSize=(600, 500), img=image, marginSize=10, borderBits=1)

    vision = WorbotsVision()

    server = VisionServer()
    server.runServer()


if __name__ == "__main__":
    main()
