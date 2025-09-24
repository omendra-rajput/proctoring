# Vercel serverless function entry point for image upload to MongoDB
import os
from pymongo import MongoClient
import json
import base64

# Initialize MongoDB client using Vercel environment variable
MONGO_URI = os.environ.get("MONGODB_URI")
client = MongoClient(MONGO_URI)
db = client.get_database("proctoring_db")
collection = db.get_collection("live_stream")

def handler(request, response):
    try:
        data = json.loads(request.body)
        if "image" not in data:
            return response.json({"error": "No image provided"}, status=400)

        img_base64 = data["image"]
        doc_id = "latest_frame"

        # Update the document with the new image. `upsert=True` creates it if it doesn't exist.
        collection.update_one(
            {"_id": doc_id},
            {"$set": {"image_data": img_base64}},
            upsert=True
        )

        return response.json({"success": True, "message": "Image uploaded to MongoDB"}, status=200)

    except Exception as e:
        # It's important to provide a detailed error message for debugging
        return response.json({"error": str(e)}, status=500)
