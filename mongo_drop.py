import pymongo
import sys

if(len(sys.argv) != 2):
    print("Usage: python3 mongo_drop.py <collection to drop>")
    exit()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb[sys.argv[1]]

mycol.drop()
