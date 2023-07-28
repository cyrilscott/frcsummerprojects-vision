import time
import ntcore
from config import WorbotsConfig

class WorbotsTables:
    config = WorbotsConfig()
    ntInstance = None

    def __init__(self):
        self.ntInstance = ntcore.NetworkTableInstance.getDefault()
        if self.config.SIM_MODE:
            self.ntInstance.setServer("127.0.0.1")
            self.ntInstance.startClient4(f"VisionModule{self.config.MODULE_ID}")
        else:
            self.ntInstance.setServerTeam(self.config.TEAM_NUMBER)
            self.ntInstance.startClient4(f"VisionModule{self.config.MODULE_ID}")

        topic = self.ntInstance.getTable(f"/module{self.config.MODULE_ID}/output")
        yeye = topic.putNumber("yeye", 0.1)

    def sendVisionMeasurement(self, ids, returnArray):
        topics = []
        for i in range(ids.size):
            topic[i] = self.ntInstance.getTable(f"/module{self.config.MODULE_ID}/output/{i}")
        
        for id in ids:
            print(id)
    
    
    def sendRobotPose(self):
        print(self.number)