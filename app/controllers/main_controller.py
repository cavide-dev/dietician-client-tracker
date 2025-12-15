from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.uic import loadUi
import os
from app.database import get_database

class MainController(QMainWindow):
    def __init__(self):
        """
        Main Application Logic.
        Initializes the UI, database connection, and event handlers.
        """
        super(MainController, self).__init__()
        
        # 1. Load UI File
        # We load the .ui file dynamically relative to this script's location.
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'views', 'main_window.ui')
        try:
            loadUi(ui_path, self)
        except Exception as e:
            print(f"UI Loading Error: {e}")
            return

        # 2. Database Connection
        # Establish connection to MongoDB Atlas.
        self.db = get_database()

        # 3. Initial Setup
        # Show the dashboard page by default on startup.
        self.stackedWidget.setCurrentWidget(self.page_dashboard)
        
        # Populate the clients table with data from the database.
        self.load_clients_table()

        # --- NAVIGATION BUTTONS (Menu) ---
        # lambda: Allows us to pass arguments to functions (switching pages).
        self.btn_dashboard.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_dashboard))
        self.btn_clients.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_clients))
        self.btn_diet_plans.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_diet_plans))
        self.btn_settings.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_settings))

        # --- CLIENT MANAGEMENT BUTTONS ---
        # Button to switch to the 'Add Client' form page.
        self.btn_add_new.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_add_client))
        
        # Cancel button returns the user to the client list without saving.
        self.btn_cancel.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_clients))
        
        # Save button triggers the data insertion logic.
        self.btn_save.clicked.connect(self.save_client)

    # --- CUSTOM FUNCTIONS ---

    def load_clients_table(self):
        """
        Fetches client data from MongoDB and populates the QTableWidget.
        Configures the table layout to stretch columns.
        """
        if self.db is None:
            return

        # Access the 'clients' collection in MongoDB
        clients_collection = self.db['clients']
        
        # Retrieve all documents as a list
        all_clients = list(clients_collection.find())
        
        # Configure Table Structure
        self.tableWidget.setRowCount(len(all_clients))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Full Name", "Phone", "Notes"])
        
        # UX Improvement: Stretch columns to fill the available width automatically
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Populate Rows
        for row_index, client in enumerate(all_clients):
            # Get data safely (use '-' if key is missing)
            name_item = QTableWidgetItem(client.get("full_name", "-"))
            phone_item = QTableWidgetItem(client.get("phone", "-"))
            note_item = QTableWidgetItem(client.get("notes", ""))
            
            # Place items in the correct cells
            self.tableWidget.setItem(row_index, 0, name_item)
            self.tableWidget.setItem(row_index, 1, phone_item)
            self.tableWidget.setItem(row_index, 2, note_item)

    def save_client(self):
        """
        Reads input fields, validates data, inserts into MongoDB,
        and refreshes the client list.
        """
        
        # 1. Get Data from Inputs
        # .strip() removes leading/trailing whitespace
        full_name = self.txt_name.text().strip()
        phone = self.txt_phone.text().strip()
        notes = self.txt_notes.toPlainText().strip()

        # 2. Validation
        # Prevent saving if the name field is empty
        if not full_name:
            QMessageBox.warning(self, "Warning", "Name cannot be empty!")
            return

        # 3. Insert into Database
        if self.db is not None:
            try:
                new_client = {
                    "full_name": full_name,
                    "phone": phone,
                    "notes": notes
                }
                
                # Perform the insertion
                self.db['clients'].insert_one(new_client)
                
                # Show Success Message
                QMessageBox.information(self, "Success", "Client added successfully!")
                
                # 4. Cleanup & Navigation
                # Clear the input fields for the next entry
                self.txt_name.clear()
                self.txt_phone.clear()
                self.txt_notes.clear()
                
                # Refresh the table to show the new client
                self.load_clients_table()
                
                # Navigate back to the client list
                self.stackedWidget.setCurrentWidget(self.page_clients)
                
            except Exception as e:
                # Handle database errors gracefully
                QMessageBox.critical(self, "Error", f"Could not save client: {e}")