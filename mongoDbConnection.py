import pymongo

class mongoModule:
    def __init__(self):
        self.mClient = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.mClient['fileSystemDb']
        self.fileSystemCollection = self.db["fileSystemCollection"]

    def addInstance(self, query):
        ans = self.fileSystemCollection.insert_one(query)
        return ans

    def printDb(self):
        doc = self.fileSystemCollection.find()
        for instance in doc:
            print(instance)

    def cleanCol(self):
        self.fileSystemCollection.drop()
        self.fileSystemCollection = self.db["fileSystemCollection"]



#mm = mongoModule()


#mydict = { "name": "Peter", "addr ess": "Lowstrsseet 27" }

#mm.addInstance(mydict)

#mm.printDb()

#mm.cleanCol()
