import os
import mongoDbConnection as mdc
import time

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
                instance = self.mongoClient.createInstance(root, file)
                if self.mongoClient.addInstance(instance):
                    print("1 row inserted")

                else:
                    print("Failed to insert row")

    def deleteScan(self):
        self.mongoClient.cleanCol()

    def printAll(self):
        self.mongoClient.printDb()



a = time.time()
ssm = slowScannerModule()
ssm.scanToDb()
ssm.printAll()
ssm.deleteScan()
print(time.time() - a)