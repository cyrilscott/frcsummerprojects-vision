from flask import Flask, render_template, Response, request
from vision import WorbotsVision
from web import VisionServer
from threading import Thread
import cv2


def main():
    vision = WorbotsVision()

    server = VisionServer()
    server.runServer()


if __name__ == "__main__":
    main()
