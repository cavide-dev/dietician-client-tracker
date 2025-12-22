import sys
from PyQt5.QtWidgets import QApplication
from app.controllers.main_controller import MainController

def main():
    """
    Application Entry Point
    -----------------------
    Initializes the QApplication, creates the main controller,
    and starts the event loop.
    """
    # 1. Create the Application instance (The Core Motor)
    app = QApplication(sys.argv)
    
    # 2. Load the Light Theme Stylesheet
    # ====================================================
    # Neden bu 3 satır?
    # - QSS dosyasını oku: open() ile light_theme.qss dosyasını açarız
    # - read(): Dosyanın tüm içeriğini string olarak oku
    # - setStyleSheet(qss): Tüm widget'lere bu stili uygula
    # 
    # Sonuç: Buttons yeşil, inputs taraflı border, tables professional görünür
    # ====================================================
    with open("assets/styles/light_theme.qss", "r", encoding="utf-8") as qss_file:
        qss = qss_file.read()
    app.setStyleSheet(qss)
    
    # 3. Initialize the Main Controller (The Window)
    main_window = MainController()
    
    # 4. Show the Window
    # Without this call, the application would run in the background invisible
    main_window.resize(1200, 700)
    main_window.show()
    
    # 5. Start the Event Loop
    # Ensures the application stays open until the user closes it
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()