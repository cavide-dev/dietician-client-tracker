from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
import os

class MainController(QMainWindow):
    def __init__(self):
        super(MainController, self).__init__()
        
        # 1. TASARIMI YÜKLE (Gövdeyi Giydir)
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'views', 'main_window.ui')
        try:
            loadUi(ui_path, self)
        except Exception as e:
            print(f"Hata: UI dosyası yüklenemedi! Detay: {e}")
            return

        # 2. BAŞLANGIÇ AYARLARI
        # Açılışta hemen Dashboard sayfasını gösterelim
        self.stackedWidget.setCurrentWidget(self.page_dashboard)

        # 3. SİNYAL - SLOT BAĞLANTILARI (Kablolama)
        # "Tıklanınca" (clicked) -> "Şunu Yap" (connect)
        self.btn_dashboard.clicked.connect(self.show_dashboard)
        self.btn_clients.clicked.connect(self.show_clients)
        self.btn_diet_plans.clicked.connect(self.show_diet_plans)
        self.btn_settings.clicked.connect(self.show_settings)

    # --- AKSİYON FONKSİYONLARI ---
    
    def show_dashboard(self):
        # Televizyonu 'page_dashboard' kanalına ayarla
        self.stackedWidget.setCurrentWidget(self.page_dashboard)

    def show_clients(self):
        self.stackedWidget.setCurrentWidget(self.page_clients)

    def show_diet_plans(self):
        self.stackedWidget.setCurrentWidget(self.page_diet_plans)

    def show_settings(self):
        self.stackedWidget.setCurrentWidget(self.page_settings)