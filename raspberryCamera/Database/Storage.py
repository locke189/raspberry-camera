#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Nov 7, 2015
Don't blink...
@author: Juan_Insuasti
'''

import pyrebase
from Shared import Logger


class Storage:
    def __init__(self,options,logs=True, debug=False):
        self.console = Logger.Logger(logName='Storage', enabled=logs, printConsole=True)
        self.firebase = pyrebase.initialize_app(options)
        self.storage = self.firebase.storage()
        self.console.log("Initialization...")
        self.debug = debug

    def saveFile(self, path, file):
        self.console.log("Uploading: %s -> %s" ,(str(file),path) )
        info = self.storage.child(str(path)).put(file)
        # print("Saving: " + str(file) + " -> " + path )
        if self.debug:
            self.console.log("Uploading: %s ",(str(info)) )

        url = self.storage.child(path).get_url(1)
        # print("URL: " + str(url) )
        self.console.log("%s URL: %s", (path, url) )

        return url

    def downloadFile(self, path, file):
        info = self.storage.child(str(path)).download(file)
        #print("Downloading: " + path + " -> "  + str(file))
        self.console.log("Downloading: %s -> %s",(path,str(file)))
        if self.debug:
            self.console.log("Downloading: %s ",(str(info)) )


    def getUrl(self, path):
        url = self.storage.child(path).get_url(1)
        self.console.log("%s URL: %s", (path, url) )
        return url





if __name__ == '__main__':
    #initial setup
    config = {
      "apiKey": "AIzaSyCeLjnaoNZ6c9BKkccXt5E0H74DGKJWXek",
      "authDomain": "testproject-cd274.firebaseapp.com",
      "databaseURL": "https://testproject-cd274.firebaseio.com",
      "storageBucket": "testproject-cd274.appspot.com"
    }

    #storage startup
    store = Storage(config)

    #save a file
    print("Testing file save...")
    url = store.saveFile("test/testfile.txt","test.txt")
    print("Returned URL... " + url)
    #get url
    print("Testing getting url...")
    url2 = store.getUrl("test/testfile.txt")
    print("Returned URL2... " + url2)

    pass
