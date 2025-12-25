from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor


class StatsCard(QWidget):
    """Single stats card showing a metric with change indicator"""
   
    def __init__(self, title, current_value, change_value, unit="", inverted=False, parent=None):
        super().__init__(parent)
        self.title = title
        self.current_value = current_value
        self.change_value = change_value
        self.unit = unit
        self.inverted = inverted
        
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
        title_label.setObjectName("stats_card_title")
       
        # Current value label
        value_label = QLabel(f"{self.current_value}{self.unit}")
        value_font = QFont()
        value_font.setPointSize(18)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setObjectName("stats_card_value")
       
        # Change label (with arrow) - inverted logic
        if not self.inverted:  # Normal: Muscle (pozitif yeşil)
            if self.change_value > 0:
                arrow = "↑"
                color = "#27ae60"  # Yeşil
            elif self.change_value < 0:
                arrow = "↓"
                color = "#e74c3c"  # Kırmızı
            else:
                arrow = "→"
                color = "#95a5a6"  # Gri
        else:  # Ters: Weight, Fat (negatif yeşil)
            if self.change_value < 0:
                arrow = "↓"
                color = "#27ae60"  # Yeşil
            elif self.change_value > 0:
                arrow = "↑"
                color = "#e74c3c"  # Kırmızı
            else:
                arrow = "→"
                color = "#95a5a6"  # Gri

        change_text = f"{arrow} {abs(self.change_value)}{self.unit}" if self.change_value != 0 else "→ No change"
                
       
        change_label = QLabel(change_text)
        change_font = QFont()
        change_font.setPointSize(11)
        change_font.setBold(True)
        change_label.setFont(change_font)
        change_label.setObjectName("stats_card_change")
       
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(change_label)
       
        # Set card object name for QSS styling
        self.setObjectName("StatsCard")
       
        self.setLayout(layout)


class StatsCardContainer(QWidget):
    """Container for multiple stats cards"""
   
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title_translator = None  # Function to translate titles
        self.setup_ui()
   
    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
       
        self.setLayout(layout)
   
    def set_title_translator(self, translator_func):
        """Set a function to translate card titles"""
        self.title_translator = translator_func
   
    def add_stats_card(self, title, current_value, change_value, unit=""):
        # Otomatik olarak hangi metriklerin inverted olduğunu belirle
        # Azalış iyi olanlara inverted=True de
        inverted_metrics = ["Weight", "Body Fat"]
        inverted = title in inverted_metrics
        
        # Translate title if translator function is set
        display_title = title
        if self.title_translator:
            display_title = self.title_translator(title)
        
        card = StatsCard(display_title, current_value, change_value, unit, inverted=inverted)
        self.layout().addWidget(card)
    
   
    def clear_cards(self):
        """Remove all cards"""
        while self.layout().count():
            widget = self.layout().takeAt(0).widget()
            if widget:
                widget.deleteLater()