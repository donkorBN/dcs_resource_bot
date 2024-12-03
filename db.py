from pymongo import MongoClient

# Connect to MongoDB (Replace <connection_string> with your MongoDB connection string)
client = MongoClient('mongosh "mongodb+srv://resource-bot.36rxl.mongodb.net/" --apiVersion 1 --username emmanuelaltitude89')  # Use 'mongodb://localhost:27017/' for local MongoDB
db = client['resource_bot']  # Database name
resources_collection = db['resources']  # Collection name

# Insert sample resources (Run this only once to populate the collection)
sample_resources = [
    {"name": "Math PPT", "file_path": "math_presentation.pptx"},
    {"name": "Physics PDF", "file_path": "physics_notes.pdf"},
    {"name": "Chemistry PPT", "file_path": "chemistry_intro.pptx"}
]
resources_collection.insert_many(sample_resources)  # Add resources to the database

print("Sample resources added successfully!")
print("Sample resources removed o")