#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Nov 7, 2015
Don't blink...
@author: Juan_Insuasti
'''

import sys
import datetime
from Shared import Logger
from Broker import Broker
import picamera
import threading

class Camera:

    actions = { "OFF":      0,
                "ON":       1,
                "TOGGLE":   2,
                "ERROR":    False,
                "IDLE":     False,
                "CAPTURE":  3,
                "START":    4,
                "STOP":     5 }

    def __init__(self, storage,broker, id, enabled, devicePath="", regTopic="/regActuator", logs=True):

        self.storage = storage
        self.id = id
        self.type = "CAM"
        self.enabled = enabled
        self.data = ""
        self.regTopic=devicePath+regTopic

        self.devicePath = devicePath
        self.path = self.devicePath + "/actuators/" + str(self.id)

        self.console = Logger.Logger(logName="Camera("+self.path+")", enabled=logs, printConsole=True)
        self.console.log("Initialization...")


        #camera settings
        self.camera = picamera.PiCamera()
        self.camera.hflip = True
        self.camera.vflip = True
        self.camera.sharpness = 0
        self.camera.contrast = 0
        self.camera.brightness = 80
        self.camera.saturation = 0
        self.camera.ISO = 0
        self.camera.video_stabilization = False
        self.camera.exposure_compensation = 0
        self.camera.exposure_mode = 'auto'
        self.camera.meter_mode = 'average'
        self.camera.awb_mode = 'auto'
        self.camera.image_effect = 'none'
        self.camera.color_effects = None
        self.camera.rotation = 0
        self.camera.crop = (0.0, 0.0, 0.0, 0.0)
        self.filename = self.path.replace("/","") + ".jpg"

        self.periodicUpdates = False
        self.timerInterval = 60


        #Initializing broker
        self.broker = broker

        #broker subscriptions
        self.broker.subscribeTopicWithCallback(self.path, self.actionsCallback )



    def actionsCallback(self, topic, payload):

        if payload == str(self.actions["CAPTURE"]):
            self.capture()
            self.broker.publishMessage( self.path + '/data', self.data )

        elif payload == str(self.actions["START"]):
            if not self.periodicUpdates:
                self.setPeriodicCaptures()
            self.broker.publishMessage( self.path + '/data', "START" )

        elif payload == str(self.actions["STOP"]):
            if self.periodicUpdates:
                self.stopPeriodicCaptures()
            self.broker.publishMessage( self.path + '/data', "STOP" )


    def registration(self):
        self.console.log("Sending registration...")
        self.broker.publishMessage( self.regTopic, self.getDeviceData() )

    def getDeviceData(self):
        data = "{'id': '" + (self.id) +"', 'type': '" + self.type + "', 'data': '" + self.data + "'}"
        return data

    def capture(self):
        self.console.log("Say Cheese!!!")
        self.camera.capture(self.filename)
        self.console.log("Uploading image file to storage.")

        path = self.path + '/' + self.filename
        self.console.log("Filepath = %s", self.filename)
        self.console.log("Uploading file...")
        self.data = self.storage.saveFile(path,self.filename)

        if self.periodicUpdates:
            threading.Timer(self.timerInterval, self.capture).start()

    def setUptateTime(self, seconds):
        self.timerInterval = seconds
        self.console.log("Setting Periodic updates to %s seconds", self.timerInterval)

    def setPeriodicCaptures(self):
        self.console.log("Starting periodic captures")
        self.periodicUpdates = True
        threading.Timer(self.timerInterval, self.capture).start()

    def stopPeriodicCaptures(self):
        self.console.log("Stopping periodic captures")
        self.periodicUpdates = False









if __name__ == '__main__':
    pass
