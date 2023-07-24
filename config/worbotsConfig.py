import json
import numpy as np

class WorbotsConfig:
    data = None

    def __new__(cls):
        if cls.data is None:
            with open("config.json", "r") as read_file:
                cls.data = json.load(read_file)
        return super(WorbotsConfig, cls).__new__(cls)

    def __init__(self):
        pass

    def getKey(self, key) -> any:
        return WorbotsConfig.data[key]

    def saveCameraIntrinsics(self, cameraMatrix, cameraDist, rvecs, tvecs):
        intrinsics = {
            "cameraMatrix": cameraMatrix.tolist(),
            "cameraDist": cameraDist.tolist(),
            "rvecs": [r.tolist() for r in rvecs],
            "tvecs": [t.tolist() for t in tvecs]
        }

        with open("calibration.json", "w") as f:
            json.dump(intrinsics, f)

    def getCameraIntrinsicsFromJSON(self):
        try:
            with open("calibration.json", "r") as f:
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
