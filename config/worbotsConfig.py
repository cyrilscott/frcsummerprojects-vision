import json
import numpy as np

class WorbotsConfig:
    CONFIG_FILENAME = "config.json"
    CALIBRATION_FILENAME = "calibration.json"

    CAMERA_ID = 0
    TEAM_NUMBER = 4145
    MODULE_ID = None
    SIM_MODE = False
    RES_W = 1280
    RES_H = 720
    CAM_FPS = 60
    TAG_SIZE_METERS = 0.1524

    def __new__(cls):
        with open(cls.CONFIG_FILENAME, "r") as read_file:
            data = json.load(read_file)
            cls.CAMERA_ID = data["CameraId"]
            cls.TEAM_NUMBER = data["TeamNumber"]
            cls.MODULE_ID = int(data["ModuleId"])
            cls.SIM_MODE = data["SimMode"]
            cls.RES_W = data["ResolutionW"]
            cls.RES_H = data["ResolutionH"]
            cls.CAM_FPS = data["CameraFPS"]
            cls.TAG_SIZE_METERS = data["TagSizeinMeters"]
        return super(WorbotsConfig, cls).__new__(cls)

    def __init__(self):
        pass

    def getKey(self, key) -> any:
        return WorbotsConfig.data[key]

    def update(cls):
        with open(cls.CONFIG_FILENAME, "r") as read_file:
            cls.CAMERA_ID = data["CameraId"]
            cls.TEAM_NUMBER = data["TeamNumber"]
            cls.MODULE_ID = data["ModuleId"]
            cls.SIM_MODE = data["SimMode"]
            cls.RES_W = data["ResolutionW"]
            cls.RES_H = data["ResolutionH"]
            cls.CAM_FPS = data["CameraFPS"]
            cls.TAG_SIZE_METERS = data["TagSizeinMeters"]

    def saveCameraIntrinsics(self, cameraMatrix, cameraDist, rvecs, tvecs):
        intrinsics = {
            "cameraMatrix": cameraMatrix.tolist(),
            "cameraDist": cameraDist.tolist(),
            "rvecs": [r.tolist() for r in rvecs],
            "tvecs": [t.tolist() for t in tvecs]
        }

        with open(self.CALIBRATION_FILENAME, "w") as f:
            json.dump(intrinsics, f)

    def getCameraIntrinsicsFromJSON(self):
        try:
            with open(self.CALIBRATION_FILENAME, "r") as f:
                data = json.load(f)

            cameraMatrix = np.array(data["cameraMatrix"])
            cameraDist = np.array(data["cameraDist"])
            rvecs = [np.array(r) for r in data["rvecs"]]
            tvecs = [np.array(t) for t in data["tvecs"]]

            return cameraMatrix, cameraDist, rvecs, tvecs

        except FileNotFoundError:
            print("Calibration file 'calibration.json' not found.")
            return None, None, None, None
        except (json.JSONDecodeError, KeyError):
            print("Error reading camera intrinsics from 'calibration.json'.")
            return None, None, None, None
