import pymongo
import os
import win32api
import win32con
import datetime

class mongoModule:
    def __init__(self):
        self.mClient = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.mClient['fileSystemDb']
        self.fileSystemCollection = self.db["fileSystemCollection"]

    def addInstance(self, query):
        ans = self.fileSystemCollection.insert_one(query)
        print(query)
        return ans.acknowledged

    def printDb(self):
        doc = self.fileSystemCollection.find()
        for instance in doc:
            print(instance)

    def searchByExtension(self, ext):
        query = { "File extension": ext }
        doc = self.fileSystemCollection.find(query).limit(50)
        return doc

    def searchByFilename(self, fn):
        query = { "Filename": fn }
        doc = self.fileSystemCollection.find(query, { "Full file path": 1 })
        return doc

    def searchByAttribute(self, attr):
        query = {"File attributes": { "$in": [attr] } }
        doc = self.fileSystemCollection.find(query, { "Filename": 1, "Full file path": 1 })
        return doc

    def searchFromModifyDate(self, lmd):###########################################
        query = {"File extension": lmd}
        doc = self.fileSystemCollection.find(query)
        return doc

    def cleanCol(self):
        self.fileSystemCollection.drop()
        self.fileSystemCollection = self.db["fileSystemCollection"]

    def createInstance(self, path, file):
        splittedFile = os.path.splitext(file)
        filepath = os.path.join(path, file)
        statFile = os.stat(filepath)
        attributes = []
        attribute = win32api.GetFileAttributes(filepath)
        if (attribute & win32con.FILE_ATTRIBUTE_ARCHIVE):
            attributes.append("archive")
        if (attribute & win32con.FILE_ATTRIBUTE_COMPRESSED):
            attributes.append("compressed")
        if (attribute & win32con.FILE_ATTRIBUTE_DEVICE):
            attributes.append("device")
        if (attribute & win32con.FILE_ATTRIBUTE_ENCRYPTED):
            attributes.append("encrypted")
        if (attribute & win32con.FILE_ATTRIBUTE_NORMAL):
            attributes.append("normal")
        if (attribute & win32con.FILE_ATTRIBUTE_NOT_CONTENT_INDEXED):
            attributes.append("not content indexed")
        if (attribute & win32con.FILE_ATTRIBUTE_OFFLINE):
            attributes.append("offline")
        if (attribute & win32con.FILE_ATTRIBUTE_REPARSE_POINT):
            attributes.append("reparse point")
        if (attribute & win32con.FILE_ATTRIBUTE_SPARSE_FILE):
            attributes.append("sparse file")
        if (attribute & win32con.FILE_ATTRIBUTE_VIRTUAL):
            attributes.append("virtual")
        if (attribute & win32con.FILE_ATTRIBUTE_HIDDEN):
            attributes.append("hidden")
        if (attribute & win32con.FILE_ATTRIBUTE_READONLY):
            attributes.append("readOnly")
        if (attribute & win32con.FILE_ATTRIBUTE_SYSTEM):
            attributes.append("system")
        if (attribute & win32con.FILE_ATTRIBUTE_TEMPORARY):
            attributes.append("temporary")
        return {"Filename": splittedFile[0], "Full file path": filepath, "File extension": splittedFile[1],
                "File size": statFile.st_size,
                "Creation date": datetime.datetime.fromtimestamp(statFile.st_ctime).strftime('%Y-%m-%d-%H:%M'),
                "Last modified date": datetime.datetime.fromtimestamp(statFile.st_mtime).strftime('%Y-%m-%d-%H:%M'),
                "File attributes": attributes}
