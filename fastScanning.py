from multiprocessing import freeze_support, Lock
from multiprocessing.pool import Pool
from multiprocessing import JoinableQueue as Queue
import mongoDbConnection as mdc
import os
import time

class fastScannerModule():
    # os.path.abspath(os.sep) - From root
    def __init__(self, path=None):
        self.unsearched = Queue()
        self.mongoClient = mdc.mongoModule()
        if path:
            self.scanPath = path
        else:
            self.scanPath = os.path.abspath('.')

    def addPaths(self, paths):
        for path in paths:
            self.unsearched.put(path)

    def explorePath(self, path):
        directories = []
        for filename in os.listdir(path):
            fullname = os.path.join(path, filename)
            if os.path.isdir(fullname):
                directories.append(fullname)
            else:
                instance = self.mongoClient.createInstance(path, filename)
                if self.mongoClient.addInstance(instance):
                    print("1 row inserted")
                else:
                    print("Failed to insert row")
        return directories

    def parallelWorker(self):
        while not self.unsearched.empty():
            path = self.unsearched.get()
            dirs = self.explorePath(path)
            for newdir in dirs:
                self.unsearched.put(newdir)
            self.unsearched.task_done()

    def start(self, numProcesses=8):
        dirs = self.explorePath(self.scanPath)
        self.addPaths(dirs)
        with Pool(numProcesses) as pool:
            for i in range(numProcesses):
                pool.apply_async(self.parallelWorker())
        self.unsearched.join()
        print("Done")

    def printAll(self):
        self.mongoClient.printDb()

    def deleteScan(self):
        self.mongoClient.cleanCol()


if __name__ == '__main__':
    a = time.time()
    freeze_support()
    fsm = fastScannerModule()
    fsm.start()
    fsm.printAll()
    fsm.deleteScan()
    print(time.time() - a)
