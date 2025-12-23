"""
Seed dietician data to MongoDB
Creates test dietician account for login testing
"""

from pymongo import MongoClient
import hashlib

def seed_dieticians():
    """
    Add test dietician to database
    """
    # Connect to MongoDB
    connection_string = "mongodb+srv://abdulkadirizmir:sifre123@cluster0.0fstc.mongodb.net/dietician_db?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
    db = client['dietician_db']
    
    dieticians = db['dieticians']
    
    # Check if already exists
    if dieticians.find_one({"username": "admin"}):
        print("✅ Admin user already exists")
        return
    
    # Hash password
    password = "admin123"  # Default password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Create admin user
    admin_user = {
        "username": "admin",
        "password": hashed_password,
        "email": "admin@dietician.com",
        "full_name": "Administrator",
        "created_at": None  # Will be set by MongoDB
    }
    
    result = dieticians.insert_one(admin_user)
    print(f"✅ Admin user created with ID: {result.inserted_id}")
    print(f"   Username: admin")
    print(f"   Password: admin123")

if __name__ == "__main__":
    seed_dieticians()
