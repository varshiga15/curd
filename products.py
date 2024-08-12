from flask import Flask,request,jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

products = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
db = client["product"]
collection = db["item"]


@products.route("/addproduct" , methods = ['POST'])
def addproduct():
    data = request.json
    productname =data.get("productname")
    itemname1 = data.get("itemname 1")

    existing_item = collection.find_one({"productname":productname,"itemname 1":itemname1})

    if existing_item:
        return jsonify({"error":"item1 already exists in this product"})
    else:
        result = collection.insert_one(data)
    return jsonify({'id':str(result.inserted_id)})
    

@products.route("/getproduct", methods = ['GET'])
def getproduct():
    result = list(collection.find())
    for results in result:
        results['_id'] = str(results['_id'])
    return jsonify(result)

@products.route("/putproduct/<_id>" , methods = ['PUT'])
def putproduct(_id):
    data = request.json
    productname = data.get("productname")
    itemname = data.get("itemname")
    object_id = ObjectId(_id)
    
    existing_item = collection.find_one({
        '_id':{'$ne':object_id},
        'productname':productname,
        'itemname':itemname
    })

    if existing_item:
        return jsonify({"MESSAGE":"PRODUCT UPDATED"})
        
    else:
        result = collection.update_one({'_id': object_id} ,{'$set':data})
    return jsonify({"error":"there are empty item"})

@products.route("/deleteproduct/<_id>" , methods = ['DELETE'])
def deleteproduct(_id):
    data = request.json
    object_id = ObjectId(_id)
    result = collection.delete_one({'_id': object_id})
    return jsonify({"MESSAGE":"PRODUCT DELETE"})

@products.route("/getsname/<_id>" , methods = ['GET'])
def getsname(_id):
    object_id = ObjectId(_id)
    result = collection.find_one({'_id':object_id})
    result['_id'] = str(result['_id'])
    return jsonify(result)

if __name__ == "__main__":
    products.run(debug=True)