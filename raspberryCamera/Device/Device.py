#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Nov 7, 2015
Don't blink...
@author: Juan_Insuasti
'''

import sys
import datetime
import os.path
import json
from Shared import Logger
from Broker import Broker
from Camera import Camera
import threading


class Device:

    def __init__(self, database, storage, id, type, enabled, basePath="", regTopic="regDevice",logs=True, logName="Device", pingTimer = 600, pingPath='ping'):
        self.sensors = []
        self.actuator = []

        #Initializing loger
        self.console = Logger.Logger(logName=logName, enabled=logs, printConsole=True)
        self.db = database
        self.storage = storage

        self.id = id
        self.type = type
        self.enabled = enabled
        self.devicePath = basePath + "/devices/" + str(self.id)
        self.regTopic = regTopic

        #Initializing broker
        self.broker = Broker.Broker(topic=topic, logs = True, logName=logName, connectFunction=self.connectFunction, willTopic=self.path, willPayload="disconnected")
        self.broker.setCallbacks()
        self.broker.start()

        #subscripion to topics
        self.broker.subscribeTopicWithCallback("ping", self.registration )

        #adding camera
        self.sensors.append(Camera.Camera(storage=self.storage, broker=self.broker, id=0, enabled=True))

    def registration(self):
        self.console.log("Sending registration...")
        self.broker.publishMessage( self.regTopic, self.getDeviceData() )

        for sensor in self.sensors:
            sensor.registration()

        for actuator in self.actuators:
            actuator.registration()

    def connectFunction(self):
        self.console.log("Sending connected message...")
        self.broker.publishMessage(self.path, 'connected')


    def getDeviceData(self):
        data = "{'id': '" + self.id +"', 'type': '" + self.type + "'}"
        return data


if __name__ == '__main__':

    # Main Loop
    pass
