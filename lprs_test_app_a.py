#!/usr/bin/env python
# lprs_test_app_a.py
"""
Copyright (c) 2015 ContinuumBridge Limited
"""

import sys
import time
import json
from cbcommslib import CbApp
from cbconfig import *

class App(CbApp):
    def __init__(self, argv):
        self.appClass = "control"
        self.state = "stopped"
        self.devices = []
        self.idToName = {} 
        # Super-class init must be called
        CbApp.__init__(self, argv)

    def setState(self, action):
        self.state = action
        msg = {"id": self.id,
               "status": "state",
               "state": self.state}
        self.sendManagerMessage(msg)

    def reportRSSI(self, rssi):
        msg = {"id": self.id,
               "status": "user_message",
               "body": "LPRS RSSI: " + str(rssi)
              }
        self.sendManagerMessage(msg)

    def onAdaptorService(self, message):
        #self.cbLog("debug", "onAdaptorService, message: " + str(message))
        for p in message["service"]:
            if p["characteristic"] == "rssi":
                req = {"id": self.id,
                       "request": "service",
                       "service": [
                                   {"characteristic": "rssi",
                                    "interval": 0
                                   }
                                  ]
                      }
                self.sendMessage(req, message["id"])
        self.setState("running")

    def onAdaptorData(self, message):
        #self.cbLog("debug", "onAdaptorData, message: " + str(message))
        if message["characteristic"] == "rssi":
            self.reportRSSI(message["data"])

    def onConfigureMessage(self, managerConfig):
        self.setState("starting")

if __name__ == '__main__':
    App(sys.argv)
