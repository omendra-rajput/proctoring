# Vercel serverless function to retrieve the latest image from MongoDB
import os
from pymongo import MongoClient
import json

# Initialize MongoDB client using Vercel environment variable
# This line now correctly fetches the environment variable named "MONGODB_URI"
MONGO_URI = os.environ.get("MONGODB_URI")
client = MongoClient(MONGO_URI)
db = client.get_database("proctoring_db")
collection = db.get_collection("live_stream")

def handler(request, response):
    try:
        # Find the single document with the latest frame
        doc_id = "latest_frame"
        latest_frame = collection.find_one({"_id": doc_id})

        if latest_frame and "image_data" in latest_frame:
            return response.json({"image": latest_frame["image_data"]}, status=200)
        else:
            return response.json({"error": "No image available"}, status=404)
            
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
