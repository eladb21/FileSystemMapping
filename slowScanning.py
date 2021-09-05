import os
import mongoDbConnection as mdc
import win32api, win32con

class slowScannerModule():
    # os.path.abspath(os.sep) - From root
    def __init__(self, path=None):
        self.mongoClient = mdc.mongoModule()
        if path:
            self.scanPath = path
        else:
            self.scanPath = os.path.abspath('.')

    def scanToDb(self):
        for root, dirs, files in os.walk(self.scanPath):
            for file in files:
                splittedFile = os.path.splitext(file)
                path = root + os.sep + file
                statFile = os.stat(path)
                attributes = {}
                attribute = win32api.GetFileAttributes(path)
                if (attribute & win32con.FILE_ATTRIBUTE_HIDDEN):
                    attributes["hidden"] = 1
                if (attribute & win32con.FILE_ATTRIBUTE_READONLY):
                    attributes["readOnly"] = 1
                if (attribute & win32con.FILE_ATTRIBUTE_SYSTEM):
                    attributes["system"] = 1
                if (attribute & win32con.FILE_ATTRIBUTE_TEMPORARY):
                    attributes["temporary"] = 1
                if(self.mongoClient.addInstance({ "Filename": splittedFile[0], "Full file path": path,
                                 "File extension": splittedFile[1], "File size": statFile.st_size,
                                 "Creation date": statFile.st_ctime, "Last modified date": statFile.st_mtime,
                                 "File attributes": attributes }).acknowledged):

                    print("1 row inserted")

                else:
                    print("Failed to insert row")


    def deleteScan(self):
        self.mongoClient.cleanCol()

    def printAll(self):
        self.mongoClient.printDb()




ssm = slowScannerModule()
ssm.scanToDb()
ssm.printAll()
ssm.deleteScan()
