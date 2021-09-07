import os
import pymongo
import multiprocessing as mp

def foo(q):
    q.put('hello')

if __name__ == '__main__':
    mp.set_start_method('spawn')
    q = mp.Queue()
    p = mp.Process(target=foo, args=(q,))
    p.start()
    print(q.get())
    p.join()
#import pymongo

#myclient = pymongo.MongoClient("mongodb://localhost:27017/")

#mydb = myclient["fileSystemDb"]
#print(myclient.list_database_names())


#dblist = myclient.list_database_names()
#if "mydatabase" in dblist:
#  print("The database exists.")
#client = pymongo.MongoClient('localhost', 27017)
#db = client.test_database
#collection = db.test_collection
#print()
#print(myclient.list_database_names())



#print(os.path.abspath(os.sep))
#for root, dirs, files in os.walk(os.path.abspath('.')):
#    print(root)
#    print(dirs)
#    print(files)
