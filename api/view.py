# Vercel serverless function to retrieve the latest image from MongoDB
import os
from pymongo import MongoClient
import json

# Initialize MongoDB client using Vercel environment variable
MONGO_URI = os.environ.get("MONGODB_URI")
client = MongoClient(MONGO_URI)
db = client.get_database("proctoring_db")
collection = db.get_collection("live_stream")

def handler(request):
    try:
        # Find the single document with the latest frame
        doc_id = "latest_frame"
        latest_frame = collection.find_one({"_id": doc_id})

        if latest_frame and "image_data" in latest_frame:
            return {"image": latest_frame["image_data"]}, 200
        else:
            return {"error": "No image available"}, 404
            
    except Exception as e:
        return {"error": str(e)}, 500
