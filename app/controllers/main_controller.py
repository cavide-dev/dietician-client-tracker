from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi
import os
# Import our custom database module
from app.database import get_database

class MainController(QMainWindow):
    def __init__(self):
        """
        Initializes the Main Application Window.
        Loads the UI, connects to the database, and sets up event listeners.
        """
        super(MainController, self).__init__()
        
        # --- 1. UI LOADING ---
        # Locate and load the .ui file dynamically
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'views', 'main_window.ui')
        try:
            loadUi(ui_path, self)
        except Exception as e:
            print(f"UI Loading Error: {e}")
            return

        # --- 2. DATABASE CONNECTION ---
        # Establish connection on startup and store the db reference
        self.db = get_database()

        # --- 3. INITIAL SETUP ---
        # Set the default page to 'Dashboard'
        self.stackedWidget.setCurrentWidget(self.page_dashboard)
        
        # Populate the clients table immediately
        self.load_clients_table()

        # --- 4. SIGNAL & SLOT CONNECTIONS (Navigation) ---
        # Connect buttons to their respective pages in the stacked widget
        self.btn_dashboard.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_dashboard))
        self.btn_clients.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_clients))
        self.btn_diet_plans.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_diet_plans))
        self.btn_settings.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_settings))

    # --- CUSTOM METHODS ---

    def load_clients_table(self):
        """
        Fetches client data from MongoDB and populates the QTableWidget.
        """
        # Check database connection first
        if self.db is None:
            print("WARNING: No Database Connection! Cannot load table.")
            return

        # Access the 'clients' collection
        clients_collection = self.db['clients']
        
        # Fetch ALL documents from the collection
        all_clients = list(clients_collection.find())
        
        # --- Table Configuration ---
        # 1. Set row count based on number of clients found
        self.tableWidget.setRowCount(len(all_clients))
        
        # 2. Set column count (Name, Phone, Notes)
        self.tableWidget.setColumnCount(3)
        
        # 3. Set Header Labels
        self.tableWidget.setHorizontalHeaderLabels(["Full Name", "Phone", "Notes"])

        # --- Populate Data ---
        # Enumerate gives us both the index (row) and the data (client)
        for row_index, client in enumerate(all_clients):
            
            # Column 0: Full Name
            name_value = client.get("full_name", "-")
            name_item = QTableWidgetItem(name_value)
            self.tableWidget.setItem(row_index, 0, name_item)
            
            # Column 1: Phone
            phone_value = client.get("phone", "-")
            phone_item = QTableWidgetItem(phone_value)
            self.tableWidget.setItem(row_index, 1, phone_item)
            
            # Column 2: Notes
            notes_value = client.get("notes", "")
            note_item = QTableWidgetItem(notes_value)
            self.tableWidget.setItem(row_index, 2, note_item)