from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor


class StatsCard(QWidget):
    """Single stats card showing a metric with change indicator"""
   
    def __init__(self, title, current_value, change_value, unit="", parent=None):
        super().__init__(parent)
        self.title = title
        self.current_value = current_value
        self.change_value = change_value
        self.unit = unit
       
        self.setup_ui()
   
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(5)
       
        # Title label
        title_label = QLabel(self.title)
        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #333;")
       
        # Current value label
        value_label = QLabel(f"{self.current_value}{self.unit}")
        value_font = QFont()
        value_font.setPointSize(18)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setStyleSheet("color: #2c3e50;")
       
        # Change label (with arrow)
        if self.change_value > 0:
            arrow = "↑"
            change_text = f"{arrow} {abs(self.change_value)}{self.unit}"
            # Green for positive changes (gains in muscle, etc - context dependent)
            color = "#27ae60"
        elif self.change_value < 0:
            arrow = "↓"
            change_text = f"{arrow} {abs(self.change_value)}{self.unit}"
            # Red for negative (but context matters - weight loss is good!)
            color = "#e74c3c"
        else:
            change_text = "→ No change"
            color = "#95a5a6"
       
        change_label = QLabel(change_text)
        change_font = QFont()
        change_font.setPointSize(11)
        change_font.setBold(True)
        change_label.setFont(change_font)
        change_label.setStyleSheet(f"color: {color};")
       
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(change_label)
       
        # Set card style with background
        self.setStyleSheet("""
            StatsCard {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
            }
        """)
       
        self.setLayout(layout)


class StatsCardContainer(QWidget):
    """Container for multiple stats cards"""
   
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
   
    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
       
        self.setLayout(layout)
   
    def add_stats_card(self, title, current_value, change_value, unit=""):
        """Add a new stats card to the container"""
        card = StatsCard(title, current_value, change_value, unit)
        self.layout().addWidget(card)
   
    def clear_cards(self):
        """Remove all cards"""
        while self.layout().count():
            widget = self.layout().takeAt(0).widget()
            if widget:
                widget.deleteLater()