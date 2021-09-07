import pymongo
import os
import win32api, win32con

class mongoModule:
    def __init__(self):
        self.mClient = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.mClient['fileSystemDb']
        self.fileSystemCollection = self.db["fileSystemCollection"]

    def addInstance(self, query):
        ans = self.fileSystemCollection.insert_one(query)
        return ans.acknowledged

    def printDb(self):
        doc = self.fileSystemCollection.find()
        for instance in doc:
            print(instance)

    def cleanCol(self):
        self.fileSystemCollection.drop()
        self.fileSystemCollection = self.db["fileSystemCollection"]

    def createQuery(self, path, file):
        splittedFile = os.path.splitext(file)
        filepath = os.path.join(path, file)
        statFile = os.stat(filepath)
        attributes = {}
        attribute = win32api.GetFileAttributes(filepath)
        if (attribute & win32con.FILE_ATTRIBUTE_HIDDEN):
            attributes["hidden"] = 1
        if (attribute & win32con.FILE_ATTRIBUTE_READONLY):
            attributes["readOnly"] = 1
        if (attribute & win32con.FILE_ATTRIBUTE_SYSTEM):
            attributes["system"] = 1
        if (attribute & win32con.FILE_ATTRIBUTE_TEMPORARY):
            attributes["temporary"] = 1
        return {"Filename": splittedFile[0], "Full file path": filepath, "File extension": splittedFile[1],
                "File size": statFile.st_size, "Creation date": statFile.st_ctime,
                "Last modified date": statFile.st_mtime, "File attributes": attributes}

#mm = mongoModule()


#mydict = { "name": "Peter", "addr ess": "Lowstrsseet 27" }

#mm.addInstance(mydict)

#mm.printDb()

#mm.cleanCol()
