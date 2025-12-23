"""
Login Window Controller
Handles user authentication and login/signup logic
"""

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from pymongo import MongoClient
import hashlib
import os

class LoginController(QMainWindow):
    def __init__(self, db_connection_string=None):
        super(LoginController, self).__init__()
        
        # Load UI from login_window.ui
        ui_path = os.path.join(os.path.dirname(__file__), "views", "login_window.ui")
        loadUi(ui_path, self)
        
        # Setup database connection
        self.db = None
        self.init_database(db_connection_string)
        
        # Connect buttons to functions
        self.btn_login.clicked.connect(self.handle_login)
        self.btn_signup_link.clicked.connect(self.open_signup)
        
        # Allow Enter key to login
        self.input_password.returnPressed.connect(self.handle_login)
        
        # Store current user (for later)
        self.current_user = None
        
    def init_database(self, connection_string=None):
        """
        Initialize MongoDB connection
        """
        try:
            # Default connection string (update with your MongoDB connection)
            if connection_string is None:
                connection_string = "mongodb+srv://abdulkadirizmir:sifre123@cluster0.0fstc.mongodb.net/dietician_db?retryWrites=true&w=majority"
            
            client = MongoClient(connection_string)
            self.db = client['dietician_db']
            
            # Test connection
            self.db.command('ping')
            print("Database connected successfully!")
            
        except Exception as e:
            print(f"Database connection failed: {e}")
            self.label_error.setText("Database connection failed!")
            self.db = None
    
    def hash_password(self, password):
        """
        Hash password using SHA256 (for security)
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def handle_login(self):
        """
        Handle login button click
        Validate username and password
        """
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()
        
        # Clear previous error
        self.label_error.setText("")
        
        # Validation
        if not username or not password:
            self.label_error.setText("Please enter username and password")
            return
        
        if self.db is None:
            self.label_error.setText("Database connection error")
            return
        
        try:
            # Check in database
            dieticians = self.db['dieticians']
            user = dieticians.find_one({"username": username})
            
            if not user:
                self.label_error.setText("Username not found")
                return
            
            # Check password
            hashed_password = self.hash_password(password)
            if user['password'] != hashed_password:
                self.label_error.setText("Invalid password")
                return
            
            # Login successful! 
            self.current_user = user
            self.label_error.setText("Login successful!")
            
            # Emit signal or call main window
            # For now, we'll close this window
            self.close()
            
        except Exception as e:
            self.label_error.setText(f"Error: {str(e)}")
    
    def open_signup(self):
        """
        Open signup window
        """
        # We'll implement this in the next step
        print("Opening signup window...")
        # TODO: Implement signup window
