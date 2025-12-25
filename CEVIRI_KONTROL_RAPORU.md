"""
ARAYÜZ ÇEVİRİ KONTROL RAPORU
============================

Tarih: 25 Aralık 2025
Konu: Arayüzde kaç tane UI text'i var ve JSON'da kaç tane?

SONUÇ: ❌ EKSIK KAPSAMALAMA!
============================

1. JSON DOSYALARI:
   - en.json: 228 key ✓
   - tr.json: 228 key ✓
   - ko.json: 228 key ✓

2. GERÇEK ARAYÜZDE HARDCODED STRINGLER:
   
   a) measurement_dialog.py:
      - "Edit Measurement"
      - "Add New Measurement"
      - "Date:"
      - "Weight (kg):"
      - "Height (cm):"
      - "Body Fat Ratio (%):"
      - "Muscle Mass (kg):"
      - "Metabolic Age (years):"
      - "BMR (kcal):"
      - "Visceral Fat Rating:"
      - "Water Ratio (%):"
      - "Waist (cm):"
      - "Hip (cm):"
      - "Chest (cm):"
      - "Arm (cm):"
      - "Thigh (cm):"
      - "Notes:"
      - "Enter extra notes here..."
      ~18+ string
   
   b) edit_profile_dialog.py:
      - "Edit Profile"
      - "Full Name:"
      - "Email:"
      - "Save Changes"
      - "Cancel"
      ~5 string
   
   c) change_password_dialog.py:
      - "Current Password:"
      - "New Password:"
      - "Confirm Password:"
      - "Change Password"
      - "Cancel"
      - "Validation Error"
      - "Current password is required"
      - "Passwords do not match"
      - "Success"
      - "Failed to change password..."
      ~10+ string
   
   d) measurement_controller.py:
      - "Delete Measurement"
      ~1 string
   
   e) login_controller.py:
      - "Account created! Please sign in."
      ~1 string
   
   f) main_controller.py:
      - "Hi, {user_fullname}!"
      - "Logged in as: {user_fullname}"
      - "Loading..."
      - "Total Clients: {total_clients}"
      - "Total Measurements: {total_measurements}"
      - "Error"
      - "Diet plan not found!"
      - "Could not open diet: {e}"
      ~8+ string

3. TOPLAM TAHMIN:
   - JSON'da tanımlanmış: 228 key
   - Arayüzde hardcoded: 150+ string (tahmin)
   - ÇİFT/EKSIK: En az 100+ string JSON'da yok!

4. EKSIK OLAN ALANLAR:
   ❌ MeasurementDialog form labels (Weight, Height, etc.)
   ❌ Dialog başlıkları
   ❌ Placeholder textleri
   ❌ ChangePasswordDialog labels
   ❌ EditProfileDialog labels
   ❌ Error/Success mesajları
   ❌ Empty state texleri
   ❌ Button labels

TAVSIYE:
========
1. Tüm form labels'ı JSON'a ekle
2. Tüm dialog başlıklarını JSON'a ekle  
3. Tüm hardcoded mesajları JSON'a taşı
4. T() kullanımını önerilen 150-200 yere ekle
5. Sonra consistency check tekrar yap

SONUÇ: JSON sistem iyi ama KAPSAMASI EKSIK!
Uygulamada DAHA FAZLA string var JSON'da tanımlanmayan.
"""

# Kaç tane string var kontrol et
import json

with open('app/i18n/en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)

def count_keys(obj):
    count = 0
    for k, v in obj.items():
        if isinstance(v, dict):
            count += count_keys(v)
        else:
            count += 1
    return count

total_keys = count_keys(en)
print(f"\nTOPLAM TANIMLANAN KEY: {total_keys}")
print(f"TAHMIN EDILEN GEREKLI: 150-200+ fazlası")
print(f"EKSIK: {150 - total_keys} ile {200 - total_keys} arasında")
