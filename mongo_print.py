import pymongo
import sys

if(len(sys.argv) != 3):
    print("Usage: python3 mongo_print.py <collection> <key>")
    exit()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb[sys.argv[1]]
#for x in mycol.find({},{ "_id": 0, "owner": 0, "name": 0, "wread": 0,  "path": 1,  "lastmod": 0,  "group": 0,  "used-b": 0,  "used-p": 0,  "perms": 0,  "zone": 0,  "fstype": 0,  "capacity": 0,  "quota": 0, "fcount": 0 }):
for x in mycol.find({},{ "_id": 0, sys.argv[2]: 1,}):
      print(x[sys.argv[2]])
