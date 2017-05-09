#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import datetime
from Managers import DeviceManager
from Model import Device, Sensor
from Database import Database, Storage
from Shared import Logger
import time

# Waits for services to be ready in RPi
if sys.platform != "darwin":
    time.sleep(60)


#creates Application Logger
console = Logger.Logger(logName='Application', enabled=True, printConsole=True)

#DeviceSetup
#Database startup
    #initial setup
config = {
  "apiKey": "AIzaSyCeLjnaoNZ6c9BKkccXt5E0H74DGKJWXek",
  "authDomain": "testproject-cd274.firebaseapp.com",
  "databaseURL": "https://testproject-cd274.firebaseio.com",
  "storageBucket": "testproject-cd274.appspot.com"
}

DB = Database.Database(config)
store = Storage.Storage(config)

#create a device
devManager = DeviceManager.DeviceManager(DB,store)


#device = Device.Device(database=DB, storage=store, id="1", type="iplant", version="Beta", enabled=True)

#subscribe a sensor
#device.addSensor("1", "LIG", "beta", True)

#save device into db
#device.saveDeviceToDB()

#acivate filter run
#update sensor data
#device.sensors["1"].filterEnable(30)

# Listen for incoming connections
try:
    while True:
        pass

except Exception as e:
    console.log('ERROR: Exception')
    console.log('ERROR: "%s"', str(e) )

finally:
    # Clean up the connection
    console.log("ERROR: CLEANUP")
