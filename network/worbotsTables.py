import time
from networktables import NetworkTables
from config import WorbotsConfig

class WorbotsTables:
    number = 0
    sd = None
    config = WorbotsConfig()
    def __init__(self, teamNum):
        if self.config.getKey('TeamNumber'):
            NetworkTables.initialize(server="127.0.0.1")
        else:
            NetworkTables.startClientTeam(teamNum)
            NetworkTables.initialize()
        NetworkTables.setNetworkIdentity("WorbotsVision")
        self.sd = NetworkTables.getTable("SmartDashboard")
    
    def sendNumber(self):
        while True:
            self.sd.putNumber("pyTest", self.number)
            self.number += 1
            time.sleep(1.0)