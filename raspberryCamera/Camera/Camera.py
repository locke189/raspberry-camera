#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Nov 7, 2015
Don't blink...
@author: Juan_Insuasti
'''
import os.path
import sys
import datetime
from Shared import Logger
from Broker import Broker
import json
from apscheduler.schedulers.background import BackgroundScheduler

if sys.platform != "darwin":
    import picamera



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
        self.settings = {}
        self.devicePath = devicePath
        self.path = self.devicePath + "/actuators/" + str(self.id)

        self.console = Logger.Logger(logName="Camera("+self.path+")", enabled=logs, printConsole=True)
        self.console.log("Initialization...")

        #camera settings
        if sys.platform != "darwin":
            self.camera = picamera.PiCamera()

        #Settings
        self.settingsFilename = self.path.replace("/","") + ".conf"

        if(not os.path.exists(self.settingsFilename)):
            self.console.log("Config file does not exist")
            self.console.log("Creting init file -> %s", self.settingsFilename)
            self.setDefaultSettings()
            self.loadSettingsToCamera()
            self.saveFile(self.settings)
        else:
            self.settings = self.loadFile(self.settingsFilename)
            self.loadSettingsToCamera()



        self.filename = self.path.replace("/","") + ".jpg"

        # Scheduler
        self.jobId = self.path.replace("/","")
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.job = self.scheduler.add_job(self.capture, 'interval', minutes=self.timerInterval, id=self.jobId, replace_existing=True)
        if not self.settings["periodicUpdates"]:
            self.job.pause()
        self.jobIdPing = self.path.replace("/","") + "ping"
        self.jobPing = self.scheduler.add_job(self.registration, 'interval', minutes=2, id=self.jobIdPing, replace_existing=True)


        #Initializing broker
        self.broker = broker

        #broker subscriptions
        self.broker.subscribeTopicWithCallback(self.path, self.actionsCallback)
        self.broker.subscribeTopicWithCallback(self.path+"/settings/#", self.settingsCallback)


    def settingsCallback(self, topic, payload):
        key = topic.replace((self.path+"/settings/"), "")
        if(key in self.settings.keys()):
            self.console.log("New setting %s = %s", (key, payload))

            self.settings[key] = self.valueCheck(self.settings[key], payload)
            self.loadSettingsToCamera()

            if key == "periodicUpdates":
                if self.settings["periodicUpdates"]:
                    self.setPeriodicCaptures()
                else:
                    self.stopPeriodicCaptures()

            self.saveFile(self.settings)
            self.broker.publishMessage( self.path + "/ack", self.settings[key])
        else:
            self.console.log("Setting %s not recognized", key)


    def setDefaultSettings(self):
        self.settings = { "hflip": True,
                          "vflip": True,
                          "sharpness": 0,
                          "contrast": 0,
                          "brightness": 80,
                          "saturation": 0,
                          "iso": 0,
                          "timer": 60,
                          "periodicUpdates": False
                }

    def loadSettingsToCamera(self):
        if sys.platform != "darwin":
            self.camera.hflip = self.settings["hflip"]
            self.camera.vflip = self.settings["vflip"]
            self.camera.sharpness = self.settings["sharpness"]
            self.camera.contrast = self.settings["contrast"]
            self.camera.brightness = self.settings["brightness"]
            self.camera.saturation = self.settings["saturation"]
            self.camera.iso = self.settings["iso"]
        self.timerInterval = self.settings["timer"]

    def saveFile(self, data):
        self.console.log("Saving data to local disk => %s", self.settingsFilename)
        with open(self.settingsFilename, 'w') as outfile:
            json.dump(data, outfile)

    def loadFile(self, file):
        self.console.log("Loading data from local disk => %s", self.settingsFilename)
        if(os.path.exists(self.settingsFilename)):
            with open(self.settingsFilename) as data_file:
                return json.load(data_file)
        self.console.log("File does not exist")


    def actionsCallback(self, topic, payload):

        if payload == str(self.actions["CAPTURE"]):
            self.capture()


    def registration(self):
        self.console.log("Sending registration...")
        self.broker.publishMessage( self.regTopic, self.getDeviceData() )

    def getDeviceData(self):
        data = "{'id': '" + (self.id) +"', 'type': '" + self.type + "', 'data': '" + self.data + "', 'settings': " + json.dumps(self.settings) + "}"
        return data

    def capture(self):
        self.console.log("Say Cheese!!!")
        if sys.platform != "darwin":
            self.camera.capture(self.filename)
        else:
            self.console.log("Mocking an image :P ")
            with open(self.filename, 'w') as outfile:
                json.dump(self.settings, outfile)

        self.console.log("Uploading image file to storage.")

        path = self.path + '/' + self.filename
        self.console.log("Filepath = %s", self.filename)
        self.console.log("Uploading file...")
        self.data = self.storage.saveFile(path,self.filename)
        self.broker.publishMessage( self.path + '/data', self.data )


    def setUptateTime(self, seconds):
        self.timerInterval = seconds
        self.console.log("Setting Periodic captures to %s minutes", self.timerInterval)
        self.job.reschedule(trigger='interval', minutes=self.timerInterval)


    def setPeriodicCaptures(self):
        self.console.log("Starting periodic captures")
        self.settings["periodicUpdates"] = True
        self.job.resume()

    def stopPeriodicCaptures(self):
        self.console.log("Stopping periodic captures")
        self.settings["periodicUpdates"] = False
        self.job.pause()

    def valueCheck(self, object, value):
        self.console.log("type %s", type(object))
        if (isinstance(object, bool)):
            if (value.upper() == "TRUE" ):
                return True
            else:
                return False
        if (isinstance(object, int)):
            return int(value)

        if (isinstance(object, float)):
            return float(value)





    def __del__(self):
        self.scheduler.shutdown(wait=False)







if __name__ == '__main__':
    pass
