import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

# 1. Load Environment Variables
# This searches for the .env file and loads the variables inside it.
load_dotenv()

# 2. Get the Password safely
# We fetch the 'MONGO_URI' variable from the loaded environment.
# This way, your password is never written explicitly in the code.
uri = os.getenv("MONGO_URI")

# Security Check: If the .env file is missing or empty, stop the app.
if not uri:
    print("ERROR: 'MONGO_URI' not found! Please check your .env file.")
    sys.exit(1)

def get_database():
    """
    Establishes a connection to the MongoDB Atlas cluster securely.
    Returns the database object to be used in the app.
    """
    try:
        # 3. Connect using the secure URI
        client = MongoClient(uri)
        
        # 4. Test the connection (Ping)
        client.admin.command('ping')
        print("SUCCESS: Connected to MongoDB Atlas successfully!")
        
        # 5. Select your specific database
        db = client['diet_app'] 
        return db
        
    except Exception as e:
        print(f"FAILED: Could not connect to MongoDB. Error: {e}")
        return None