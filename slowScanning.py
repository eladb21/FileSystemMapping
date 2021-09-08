import os
import mongoDbConnection as mdc

class slowScannerModule():
    '''
    Regular filesystem scanner using os.walk - scan files one by one in hierarchical order.
    '''
    def __init__(self, path=None):
        # mongoDB custom API
        self.mongoClient = mdc.mongoModule()
        if path:
            self.scanPath = path
        else:
            self.scanPath = os.path.abspath(os.sep)  # - path to the root

    def scanToDb(self):
        # run hierarchical on filesystem and write to mongoDB
        for root, dirs, files in os.walk(self.scanPath):
            for file in files:
                instance = self.mongoClient.createInstance(root, file)
                if self.mongoClient.addInstance(instance):
                    pass
                else:
                    print("Failed to insert row")

    def deleteScan(self):
        # delete DB collection
        self.mongoClient.cleanCol()

    def printAll(self):
        # print DB collection
        self.mongoClient.printDb()
