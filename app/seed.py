from app.database import get_database

def add_fake_data():
    # 1. Veritabanı Bağlantısını Çağır (Anahtarı al)
    db = get_database()
    
    if db is None:
        print(" Database connection failed!")
        return

    # 2. Koleksiyonu (Tabloyu) Seç
    # MongoDB'de tabloya 'Collection' denir. 
    # 'clients' adında bir kutu açıyoruz.
    clients_collection = db['clients']

    # 3. İngilizce Test Verisi Hazırla
    # Python'da buna 'Dictionary' (Sözlük) denir.
    fake_clients = [
        {
            "full_name": "John Doe",
            "phone": "+1 555 0199",
            "email": "johndoe@example.com",
            "gender": "Male",
            "notes": "Diabetes patient"
        },
        {
            "full_name": "Jane Smith",
            "phone": "+1 555 0200",
            "email": "janesmith@example.com",
            "gender": "Female",
            "notes": "Vegan diet"
        },
        {
            "full_name": "Ali Yılmaz",
            "phone": "+90 555 123 45 67",
            "email": "ali@example.com",
            "gender": "Male",
            "notes": "Gluten intolerant"
        }
    ]
    
    # Hepsini birden ekle:
    clients_collection.insert_many(fake_clients)
    print(f"{len(fake_clients)} müşteri eklendi!")

    
    print("SUCCESS: Dummy clients added to MongoDB!")

if __name__ == "__main__":
    add_fake_data()