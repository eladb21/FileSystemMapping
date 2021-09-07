import os
import mongoDbConnection as mdc

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
                query = self.mongoClient.createQuery(root, file)
                if self.mongoClient.addInstance(query):
                    print("1 row inserted")

                else:
                    print("Failed to insert row")

    def deleteScan(self):
        self.mongoClient.cleanCol()

    def printAll(self):
        self.mongoClient.printDb()




#ssm = slowScannerModule()
#ssm.scanToDb()
#ssm.printAll()
#ssm.deleteScan()
