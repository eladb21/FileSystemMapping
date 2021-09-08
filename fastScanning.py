from multiprocessing import Lock
from multiprocessing.pool import Pool
from multiprocessing import JoinableQueue as Queue
import mongoDbConnection as mdc
import os


class fastScannerModule():
    # os.path.abspath(os.sep) - From root
    def __init__(self, path=None):
        self.unsearched = Queue()  # queue for hold the next directories for the processes
        self.mongoClient = mdc.mongoModule()  # mongoDB custom API
        if path:
            self.scanPath = path
        else:
            self.scanPath = os.path.abspath(os.sep)  # - path to the root

    def addPaths(self, paths):
        # add paths into queue
        for path in paths:
            self.unsearched.put(path)

    def explorePath(self, path):
        # explore files and directories
        directories = []
        for filename in os.listdir(path):
            fullname = os.path.join(path, filename)
            if os.path.isdir(fullname):
                directories.append(fullname)
            else:
                # add new instance to DB
                instance = self.mongoClient.createInstance(path, filename)
                if self.mongoClient.addInstance(instance):
                    pass
                else:
                    print("Failed to insert row")
        return directories

    def parallelWorker(self):
        # manage the queue for parallel processing
        while not self.unsearched.empty():
            path = self.unsearched.get()
            dirs = self.explorePath(path)
            for newdir in dirs:
                self.unsearched.put(newdir)
            self.unsearched.task_done()

    def start(self, numProcesses=8):
        # start few processes, default is 8
        dirs = self.explorePath(self.scanPath)
        self.addPaths(dirs)
        with Pool(numProcesses) as pool:
            for i in range(numProcesses):
                pool.apply_async(self.parallelWorker())
        self.unsearched.join()

    def printAll(self):
        #  print collection
        self.mongoClient.printDb()

    def deleteScan(self):
        # delete collection
        self.mongoClient.cleanCol()


