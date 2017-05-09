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

class Logger:
    def __init__(self, logName="Log", file="log.txt", enabled=True, printConsole=True, saveFile=False, saveCloud=False):
        self.logName = logName
        self.file = file
        self.enabled = enabled
        self.printConsole = printConsole
        self.saveFile = saveFile
        self.saveCloud = saveCloud

        self.saveRecord('===== ' + datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + " +0000 " + '=====')

    def log(self, action, data=None):
        if (self.enabled):

            record = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            record += " +0000 : "
            record += self.logName + " >> "
            if(data):
                record += action % data
            else:
                record += action
            self.printLog(record)
            self.saveRecord(record)

    def printLog(self, record):
        if(self.printConsole):
            print(record, file=sys.stderr)

    def saveRecord(self, record):
        if(self.saveFile):
            fileData = record
            fileData +=  "\n"
            file = open(self.file,"a")
            file.write(fileData)
            file.close()




if __name__ == '__main__':
    print('Starting Program')
    console = Logger(logName='device0', file='test.log', enabled=True, printConsole=True, saveFile=True)
    console.log('testing with data = %s',222)
    console.log('testing without data')

    pass
