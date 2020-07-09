import pymongo



client = pymongo.MongoClient("mongodb://genadi:1234@cluster0.smdfw.gcp.mongodb.net:27017/linuxpolls")
db = client.linuxpolls
collection = db['linuxpolls']
print(collection)