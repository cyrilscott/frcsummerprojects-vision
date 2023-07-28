import time
import ntcore
import numpy as np
from config import WorbotsConfig
from vision import Detection

class WorbotsTables:
    config = WorbotsConfig()
    ntInstance = None
    dataPublisher = None

    def __init__(self):
        self.ntInstance = ntcore.NetworkTableInstance.getDefault()
        if self.config.SIM_MODE:
            self.ntInstance.setServer("127.0.0.1")
            self.ntInstance.startClient4(f"VisionModule{self.config.MODULE_ID}")
        else:
            self.ntInstance.setServerTeam(self.config.TEAM_NUMBER)
            self.ntInstance.startClient4(f"VisionModule{self.config.MODULE_ID}")
        table = self.ntInstance.getTable(f"/module{self.config.MODULE_ID}/output")
        self.dataPublisher = table.getDoubleArrayTopic("data").publish(ntcore.PubSubOptions())

    def sendVisionMeasurement(self, detectionArray: np.array([], Detection)):
        outArray = []
        if detectionArray.size != 0:
            for i in range(detectionArray.size):
                outArray.append(detectionArray[i].tag_id)
                for num in detectionArray[i].tvec:
                    outArray.append(num)
                for num in detectionArray[i].rvec:
                    outArray.append(num)
        self.dataPublisher.set(outArray)
    
    
    def sendRobotPose(self):
        print(self.number)